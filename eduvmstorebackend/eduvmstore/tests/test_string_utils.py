from django.test import TestCase
from eduvmstore.utils.string_utils import has_version_suffix, extract_version_suffix, create_version_pattern

class AppTemplateOperationsTests(TestCase):
    def test_has_version_suffix(self):
        # Should return True for names with proper version suffixes
        self.assertTrue(has_version_suffix("example-V21"))
        self.assertTrue(has_version_suffix("template-V1"))
        self.assertTrue(has_version_suffix("long name with spaces-V0"))
        self.assertTrue(has_version_suffix("name-V999"))

        # Should return False for names without version suffixes
        self.assertFalse(has_version_suffix("app_templateITIL3"))
        self.assertFalse(has_version_suffix("V1"))  # No hyphen
        self.assertFalse(has_version_suffix("template-v1"))  # Lowercase v
        self.assertFalse(has_version_suffix("template-V"))  # No digits
        self.assertFalse(has_version_suffix("template-V1a"))  # Non-digit after number
        self.assertFalse(has_version_suffix("template-V1-suffix"))  # Something after
        self.assertFalse(has_version_suffix("template V1"))  # Space instead of hyphen

    def test_extract_version_suffix(self):
        # Should extract version suffixes correctly
        self.assertEqual(extract_version_suffix("example-V21"), "-V21")
        self.assertEqual(extract_version_suffix("template-V1"), "-V1")
        self.assertEqual(extract_version_suffix("long name with spaces-V0"), "-V0")
        self.assertEqual(extract_version_suffix("name-V999"), "-V999")

        # Should return empty string for invalid or missing version suffixes
        self.assertEqual(extract_version_suffix("app_templateITIL3"), "")
        self.assertEqual(extract_version_suffix("V1"), "")
        self.assertEqual(extract_version_suffix("template-v1"), "")
        self.assertEqual(extract_version_suffix("template-V"), "")
        self.assertEqual(extract_version_suffix("template-V1a"), "")
        self.assertEqual(extract_version_suffix("template-V1-suffix"), "")
        self.assertEqual(extract_version_suffix("template V1"), "")

    def test_create_version_pattern(self):
        # Should create correct patterns for simple names
        self.assertEqual(create_version_pattern("template"), r"^template-V\d+$")
        self.assertEqual(create_version_pattern("example"), r"^example-V\d+$")

        # Should escape special regex characters in names
        self.assertEqual(create_version_pattern("test.template"), r"^test\.template-V\d+$")
        self.assertEqual(create_version_pattern("test+name"), r"^test\+name-V\d+$")
        self.assertEqual(create_version_pattern("name[1]"), r"^name\[1\]-V\d+$")
