"""The checked-in offline HTML must exactly match its boss source fragment."""
import unittest
from scripts.build_game import INDEX,build_html,BOSS_MODULE
class BuildReproducibilityTests(unittest.TestCase):
 def test_root_html_matches_source_fragment(self):
  self.assertEqual(INDEX.read_text(encoding="utf-8"),build_html())
 def test_boss_module_is_bundled_and_private(self):
  html=INDEX.read_text(encoding="utf-8")
  self.assertIn(BOSS_MODULE.read_text(encoding="utf-8").rstrip("\n"),html)
  self.assertIn("bossUpdateHomingProjectile(s,dt,p)",html)
  self.assertNotIn("window.BOSS_ARCHETYPES",html)
if __name__=="__main__":unittest.main()
