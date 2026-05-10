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

    def test_count_content_lines(self):
        content = """---
id: test
title: Test
status: draft
tags: []
summary: S
ai_context: C
---
Line 1
Line 2

Line 4
<!-- comment -->
Line 6
"""
        count = self.validator.count_content_lines(content)
        # 1, 2, empty, 4, 6 (comment is ignored)
        self.assertEqual(count, 5)

    def test_check_tldr(self):
        valid_content = "> **TL;DR**: This is a test."
        invalid_content = "Just some text."
        
        ok, errors, _ = self.validator.check_tldr(valid_content)
        self.assertTrue(ok)
        
        ok, errors, _ = self.validator.check_tldr(invalid_content)
        self.assertFalse(ok)
        self.assertIn("Missing TL;DR", errors[0])

    def test_check_heading_structure(self):
        valid_content = "---\nid: 1\ntitle: T\nstatus: draft\ntags: []\nsummary: S\nai_context: C\n---\n# H1\n## H2"
        invalid_content = "---\nid: 1\ntitle: T\nstatus: draft\ntags: []\nsummary: S\nai_context: C\n---\n# H1\n### H3"
        
        ok, _ = self.validator.check_heading_structure(valid_content)
        self.assertTrue(ok)
        
        ok, errors = self.validator.check_heading_structure(invalid_content)
        self.assertFalse(ok)
        self.assertTrue(any("Heading jump" in e for e in errors))

if __name__ == "__main__":
    unittest.main()
