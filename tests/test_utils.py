"""Unit tests for src/utils.py — error detection helpers."""

import unittest

from src.utils import is_auth_error, is_quota_error


class TestIsAuthError(unittest.TestCase):
    def test_401_status(self):
        self.assertTrue(is_auth_error("401 Unauthorized: invalid API key"))

    def test_auth_keyword(self):
        self.assertTrue(is_auth_error("Authentication failed for user"))

    def test_quota_is_not_auth(self):
        self.assertFalse(is_auth_error("429 RESOURCE_EXHAUSTED. quota exceeded"))

    def test_normal_error_is_not_auth(self):
        self.assertFalse(is_auth_error("500 Internal Server Error"))


class TestIsQuotaError(unittest.TestCase):
    def test_gemini_resource_exhausted(self):
        msg = (
            "429 RESOURCE_EXHAUSTED. {'error': {'code': 429, 'message': "
            "'You exceeded your current quota'}}"
        )
        self.assertTrue(is_quota_error(msg))

    def test_quota_exceeded_keyword(self):
        self.assertTrue(is_quota_error("quota exceeded for metric: foo"))

    def test_transient_429_not_quota(self):
        """A plain rate-limit 429 without 'quota'/'resource_exhausted' must NOT abort."""
        self.assertFalse(is_quota_error("429 Too Many Requests: rate limit exceeded"))

    def test_auth_error_not_quota(self):
        self.assertFalse(is_quota_error("401 Unauthorized: invalid API key"))

    def test_server_error_not_quota(self):
        self.assertFalse(is_quota_error("503 Service Unavailable"))

    def test_case_insensitive(self):
        self.assertTrue(is_quota_error("resource_EXHAUSTED something"))
        self.assertTrue(is_quota_error("Quota limit reached"))


if __name__ == "__main__":
    unittest.main()
