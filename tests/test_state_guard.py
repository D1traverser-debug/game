"""Negative controls: the state guard must catch drift, not simply return PASS."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SOURCE=Path(__file__).resolve().parents[1]/'scripts'/'verify_project_state.py'
spec=importlib.util.spec_from_file_location('project_guard',SOURCE)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class GuardTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        (self.root/'docs').mkdir()
        (self.root/'HANDOFF.md').write_text('checkpoint\n',encoding='utf8')
        self.source=b'<html><style>x{}</style><script>let x=1</script></html>'
        (self.root/'index.html').write_bytes(self.source)
        import hashlib
        digest=hashlib.sha256(self.source).hexdigest()
        self.state={'repository':'D1traverser-debug/game','scope':dict(module.OWNER_SCOPE),
                    'active_production_branch':'full-game','branch':'full-game',
                    'legacy_browser_prototype':{'branch':'development','sha256':digest,'bytes':len(self.source)},
                    'caos_boundary':'CAOS parent is read-only and unchanged.',
                    'status':'NOT_READY','checkpoint':'TEST',
                    'development_candidate_sha256':digest,
                    'development_candidate_bytes':len(self.source)}
        self.save_state()
    def save_state(self):
        (self.root/'docs'/'PROJECT_STATE.json').write_text(json.dumps(self.state),encoding='utf8')
    def test_valid_baseline(self):
        self.assertEqual(module.verify(self.root)['status'],'PASS_MECHANICAL_ONLY')
    def test_changed_code_detected(self):
        (self.root/'index.html').write_bytes(self.source+b'mutation')
        self.assertIn('ARTIFACT_SHA_MISMATCH',module.verify(self.root)['errors'])
    def test_scope_drift_detected(self):
        self.state['scope']['multiplayer']=False
        self.save_state()
        self.assertIn('SCOPE_DRIFT:multiplayer',module.verify(self.root)['errors'])
    def test_active_branch_drift_detected(self):
        self.state['active_production_branch']='development'
        self.save_state()
        self.assertIn('ACTIVE_BRANCH_DRIFT',module.verify(self.root)['errors'])
    def test_fake_ready_detected(self):
        self.state['status']='READY'
        self.save_state()
        self.assertIn('UNSUPPORTED_READY_STATUS',module.verify(self.root)['errors'])
    def test_debug_surface_detected(self):
        new=b'<html><style>x{}</style><script>window.__QA={}</script></html>'
        (self.root/'index.html').write_bytes(new)
        import hashlib
        digest=hashlib.sha256(new).hexdigest()
        self.state['legacy_browser_prototype']['sha256']=digest
        self.state['legacy_browser_prototype']['bytes']=len(new)
        self.state['development_candidate_sha256']=digest
        self.state['development_candidate_bytes']=len(new)
        self.save_state()
        self.assertIn('PRODUCTION_DEBUG_MUTATION_SURFACE',module.verify(self.root)['errors'])

if __name__=='__main__':unittest.main()
