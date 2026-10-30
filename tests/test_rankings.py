"""Regression checks for the static KSQI ranking pages (stdlib only)."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RankingContentTests(unittest.TestCase):
    def test_integrated_ranking_matches_other_category_tables(self):
        html = (ROOT / 'integrated.html').read_text()
        ranking = html.split('<section class="section"', 1)[1].split('</section>', 1)[0]
        self.assertNotIn('<img', ranking)
        self.assertNotIn('wimg', ranking)
        self.assertIn('<h3>The full Top 10</h3>', ranking)
        self.assertIn('Ranks 1–10 · editorial selection', ranking)
        ranks = re.findall(r'class="pos rk">(\d+)</span>', ranking)
        self.assertEqual(ranks, [f'{n:02d}' for n in range(1, 11)])
        rows = re.findall(r'<div class="wrow[^\"]*">(.*?)</div>', ranking, re.S)
        self.assertEqual(len(rows), 11)
        for row in rows:
            self.assertEqual(row.count('<span'), 5)
        first = rows[1]
        self.assertIn('Rays Public School', first)
        self.assertIn('Kozhikode', first)
        css = (ROOT / 'styles.css').read_text()
        match = re.search(r'\.wrow\{[^}]*grid-template-columns:([^;]+);', css)
        assert match is not None
        desktop = match.group(1)
        self.assertEqual(len(desktop.split()), 5)


    def test_rps_fees_are_not_published(self):
        html = (ROOT / 'integrated.html').read_text()
        self.assertNotIn('₹', html)
        self.assertNotRegex(html.lower(), r'\b(?:annual fee|gst)\b')


    def test_rps_timetable_uses_requested_copy(self):
        html = (ROOT / 'integrated.html').read_text()
        self.assertIn('<b>The integrated timetable.</b> The school scores in this category due to both its Board and Entrance Modules being well integrated and taught by the same entrance faculty for each chapter.', html)
        self.assertNotIn('Preparation is inside the school day — mornings for board academics', html)


    def test_editorial_panel_contains_requested_people(self):
        html = (ROOT / 'panelists.html').read_text()
        self.assertNotRegex(html.lower(), r'hafeez|anin|puthuk')
        self.assertEqual(html.count('id="anirudh-surendran"'), 1)
        self.assertIn('https://www.linkedin.com/in/anirudh-surendran-900494157/', html)
        self.assertIn('IIT Kharagpur', html)
        self.assertIn('IIM Bangalore', html)

    def test_all_category_tables_have_ten_five_cell_rows(self):
        for name in ('integrated', 'private', 'government'):
            with self.subTest(category=name):
                html = (ROOT / f'{name}.html').read_text()
                rows = re.findall(r'<div class="wrow[^\"]*">(.*?)</div>', html, re.S)
                self.assertEqual(len(rows), 11)
                for row in rows:
                    self.assertEqual(row.count('<span'), 5)


if __name__ == '__main__':
    unittest.main()
