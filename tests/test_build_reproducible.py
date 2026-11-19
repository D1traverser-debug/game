"""The checked-in offline HTML must exactly match its boss source fragment."""
import unittest
from scripts.build_game import INDEX,build_html,BOSS_MODULE,RNG_MODULE,RNG_START
class BuildReproducibilityTests(unittest.TestCase):
 def test_root_html_matches_source_fragment(self):
  self.assertEqual(INDEX.read_text(encoding="utf-8"),build_html())
 def test_boss_module_is_bundled_and_private(self):
  html=INDEX.read_text(encoding="utf-8")
  self.assertIn(BOSS_MODULE.read_text(encoding="utf-8").rstrip("\n"),html)
  self.assertIn("bossUpdateHomingProjectile(s,dt,p)",html)
  self.assertIn("enemyHoming",html)
  self.assertNotIn("window.BOSS_ARCHETYPES",html)
 def test_seeded_rng_module_is_bundled_from_canonical_source(self):
  html=INDEX.read_text(encoding="utf-8")
  fragment=RNG_MODULE.read_text(encoding="utf-8").replace("export class SeededRng","class SeededRng",1).rstrip("\n")
  self.assertIn(RNG_START,html)
  self.assertIn(RNG_START+"\\nconst MASK_64",html)
  self.assertIn(fragment,html)
  self.assertNotIn("export class SeededRng",html)
if __name__=="__main__":unittest.main()
