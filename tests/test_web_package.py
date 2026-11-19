import hashlib, importlib.util, tempfile
from pathlib import Path
import unittest
P=Path(__file__).resolve().parents[1]/"scripts"/"package_web.py"
S=importlib.util.spec_from_file_location("package_web",P)
M=importlib.util.module_from_spec(S); S.loader.exec_module(M)

class WebPackageTests(unittest.TestCase):
    def test_source_validation_and_hash(self):
        raw=M.SOURCE.read_bytes()
        result=M.validate(raw)
        self.assertEqual(result["sha256"],hashlib.sha256(raw).hexdigest())
        self.assertEqual(result["product_status"],"NOT_READY")
        self.assertEqual(len(result["runtime_modules"]),8)
        self.assertTrue(any(x["path"].endswith("fixed-step-clock.mjs") for x in result["runtime_modules"]))
    def test_external_script_rejected(self):
        raw=b'<!doctype html><title>x</title><style></style><canvas id="world"></canvas><script src="https://cdn.example/x.js"></script>'
        with self.assertRaisesRegex(ValueError,"EXTERNAL_SCRIPT"): M.validate(raw)
    def test_external_stylesheet_rejected(self):
        raw=b'<!doctype html><title>x</title><link rel="stylesheet" href="https://cdn.example/x.css"><style></style><canvas id="world"></canvas><script></script>'
        with self.assertRaisesRegex(ValueError,"EXTERNAL_STYLESHEET"): M.validate(raw)
    def test_debug_hook_rejected(self):
        raw=b'<!doctype html><title>x</title><style></style><canvas id="world"></canvas><script>window.__QA={}</script>'
        with self.assertRaisesRegex(ValueError,"PRODUCTION_DEBUG_MUTATION_SURFACE"): M.validate(raw)
    def test_missing_canvas_rejected(self):
        raw=b'<!doctype html><title>x</title><style></style><script>let x=1</script>'
        with self.assertRaisesRegex(ValueError,"MISSING_WEB_RUNTIME_MARKERS"): M.validate(raw)
    def test_package_and_verify_include_runtime_modules(self):
        with tempfile.TemporaryDirectory() as tmp:
            original=M.OUTPUT
            try:
                M.OUTPUT=Path(tmp)/"dist"
                manifest=M.package()
                self.assertEqual(M.verify_output(),manifest)
                for module in manifest["runtime_modules"]:
                    self.assertTrue((M.OUTPUT/module["path"]).is_file())
                self.assertTrue((M.OUTPUT/"PLAY.bat").is_file())
                self.assertTrue((M.OUTPUT/"PLAY.sh").is_file())
                self.assertTrue((M.OUTPUT/"scripts"/"serve_web.py").is_file())
                self.assertEqual(manifest["launcher"]["default_host"],"127.0.0.1")
            finally: M.OUTPUT=original

    def test_local_server_is_loopback_only_and_launcher_opens_browser(self):
        server=(M.ROOT/"scripts"/"serve_web.py").read_text(encoding="utf-8")
        windows=(M.ROOT/"PLAY.bat").read_text(encoding="utf-8")
        unix=(M.ROOT/"PLAY.sh").read_text(encoding="utf-8")
        self.assertIn('("127.0.0.1", port)',server)
        self.assertIn("webbrowser.open_new_tab(url)",server)
        self.assertIn("scripts\\serve_web.py --open",windows)
        self.assertIn("python3 scripts/serve_web.py --open",unix)

if __name__=="__main__": unittest.main()
