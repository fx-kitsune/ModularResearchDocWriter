import unittest
from mrm.core.validator import MRMValidator

class TestMRMParser(unittest.TestCase):
    def setUp(self):
        self.validator = MRMValidator(verbose=False)

    def test_parse_frontmatter_standard(self):
        block = "id: test-id\ntitle: Test Title\nstatus: final\ntags: [tag1, tag2]\nsummary: A short summary.\nai_context: Some context."
        data = self.validator.parse_frontmatter_block(block)
        self.assertEqual(data["id"], "test-id")
        self.assertEqual(data["title"], "Test Title")
        self.assertEqual(data["status"], "final")
        self.assertEqual(data["tags"], ["tag1", "tag2"])

    def test_parse_frontmatter_list(self):
        block = "tags:\n  - tag1\n  - tag2"
        data = self.validator.parse_frontmatter_block(block)
        self.assertEqual(data["tags"], ["tag1", "tag2"])

    def test_extract_frontmatter(self):
        content = "---\nid: 1\ntitle: T\nstatus: draft\ntags: []\nsummary: S\nai_context: C\n---\nBody content"
        fm, body = self.validator.extract_frontmatter(content)
        self.assertIsNotNone(fm)
        self.assertEqual(fm["id"], "1")
        self.assertEqual(body.strip(), "Body content")

if __name__ == "__main__":
    unittest.main()
