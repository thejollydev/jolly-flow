import unittest
from jolly_sync.transform import remove_frontmatter, resolve_wikilinks

class TestTransform(unittest.TestCase):
    def test_remove_frontmatter(self):
        content = "---\ntitle: Test\n---\n# Content"
        expected = "# Content"
        self.assertEqual(remove_frontmatter(content), expected)

        content_no_fm = "# No Frontmatter"
        self.assertEqual(remove_frontmatter(content_no_fm), content_no_fm)

    def test_resolve_wikilinks(self):
        content = "Check [[Target]] and [[Link|Display Text]]"
        expected = "Check Target and Display Text"
        self.assertEqual(resolve_wikilinks(content), expected)

if __name__ == "__main__":
    unittest.main()
