import importlib.util, json
from pathlib import Path
import tempfile, unittest
P=Path(__file__).resolve().parents[1]/"scripts"/"verify_project_state.py"
S=importlib.util.spec_from_file_location("project_guard",P)
M=importlib.util.module_from_spec(S); S.loader.exec_module(M)

class GuardTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup); self.root=Path(self.tmp.name)
  (self.root/"docs").mkdir(); (self.root/"HANDOFF.md").write_text("checkpoint",encoding="utf-8")
  self.raw=b'<!doctype html><html><title>x</title><style></style><canvas id="world"></canvas><script>let x=1</script></html>'
  (self.root/"index.html").write_bytes(self.raw)
  self.state={"repository":"D1traverser-debug/game","active_production_branch":"full-game","branch":"full-game",
   "legacy_prototype_branch":"development","scope":dict(M.OWNER_SCOPE),"caos_boundary":"CAOS is read-only.",
   "status":"NOT_READY","checkpoint":"TEST","web_game_artifact":{"path":"index.html","bytes":len(self.raw)}}
  self.save()
 def save(self): (self.root/"docs"/"PROJECT_STATE.json").write_text(json.dumps(self.state),encoding="utf-8")
 def test_valid_checkpoint(self): self.assertEqual(M.verify(self.root)["status"],"PASS_MECHANICAL_ONLY")
 def test_html_mutation_detected(self):
  (self.root/"index.html").write_bytes(self.raw+b"changed")
  self.assertIn("WEB_ARTIFACT_SIZE_MISMATCH",M.verify(self.root)["errors"])
 def test_scope_drift_detected(self):
  self.state["scope"]["multiplayer"]=False; self.save()
  self.assertIn("SCOPE_DRIFT:multiplayer",M.verify(self.root)["errors"])
 def test_branch_drift_detected(self):
  self.state["active_production_branch"]="development"; self.save()
  self.assertIn("ACTIVE_BRANCH_DRIFT",M.verify(self.root)["errors"])
 def test_external_script_detected(self):
  changed=self.raw.replace(b"<script>",b'<script src="https://cdn.example/x.js">')
  (self.root/"index.html").write_bytes(changed); self.state["web_game_artifact"]["bytes"]=len(changed); self.save()
  self.assertIn("EXTERNAL_RUNTIME_SCRIPT",M.verify(self.root)["errors"])
 def test_fake_ready_detected(self):
  self.state["status"]="READY"; self.save()
  self.assertIn("UNSUPPORTED_READY_STATUS",M.verify(self.root)["errors"])
if __name__=="__main__": unittest.main()
