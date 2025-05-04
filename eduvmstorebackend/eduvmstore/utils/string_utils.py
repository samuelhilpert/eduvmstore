import re

# Pattern to match version suffixes in AppTemplate names.
# This pattern is forbidden as it is automatically used for approved AppTemplates
VERSION_SUFFIX_PATTERN = r'-V\d+$'


def has_version_suffix(name: str) -> bool:
    """
    Check if the given AppTemplate name has a version suffix.
    Examples are '-V1', '-V2', etc.

    :param str name: The name of the AppTemplate to check
    :return: True if a version suffix is found, False otherwise
    :rtype: bool
    """
    return bool(re.search(VERSION_SUFFIX_PATTERN, name))


def extract_version_suffix(name: str) -> str:
    """
    Extract the version suffix from an AppTemplate name if present.

    :param str name: The name to check
    :return: The extracted version suffix or empty string if none found
    :rtype: str
    """
    match = re.search(VERSION_SUFFIX_PATTERN, name)
    return match.group(0) if match else ""


def create_version_pattern(name: str) -> str:
    """
    Create a regex pattern to match versioned templates with the given base name.

    :param str name: The base name to create the pattern for
    :return: The regex pattern for matching versioned templates
    :rtype: str
    """
    return f"^{re.escape(name)}{VERSION_SUFFIX_PATTERN}"
