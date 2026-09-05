"""
Pytest configuration and shared fixtures for zero-knowledge-location-exposure-agent tests.
"""
import os
import pytest


def pytest_configure(config):
    """Set required environment variables for testing."""
    os.environ.setdefault(
        "AUDIT_SECRET_KEY",
        "test-audit-secret-key-for-testing-only-32chars1234567890"
    )


@pytest.fixture(autouse=True)
def reset_audit_trail():
    """Reset the global audit trail before each test for isolation."""
    from agents.base import AuditLogger
    AuditLogger.reset()
    yield
    AuditLogger.reset()
