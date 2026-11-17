"""The checked-in offline HTML must exactly match its ordered source fragments."""
import unittest

from scripts.build_game import INDEX, build_html, render, BOSS_MODULE


class BuildReproducibilityTests(unittest.TestCase):
    def test_root_html_matches_source_fragments(self):
        self.assertEqual(INDEX.read_text(encoding="utf-8"), build_html())

    def test_boss_fragment_is_in_the_runtime_closure(self):
        html = INDEX.read_text(encoding="utf-8")
        module = BOSS_MODULE.read_text(encoding="utf-8").rstrip("\n")
        self.assertEqual(html.count("/* Boss pool and combat patterns."), 1)
        self.assertIn(module, html)
        self.assertNotIn("window.BOSS_ARCHETYPES", html)


if __name__ == "__main__":
    unittest.main()
