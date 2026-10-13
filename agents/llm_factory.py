"""Deterministic local responder.

Only the mock provider is implemented. There is no remote model inference
or independent validation of a query's contents.
"""
from .base import PHIGuard


class MockLLM:
    """Local string-based response adapter, without external requests."""

    def __init__(self, system_name: str = "Zero Knowledge Location Exposure Agent"):
        self.system_name = system_name

    def invoke(self, prompt: str) -> str:
        PHIGuard.assert_no_phi(prompt)
        return (
            f"[{self.system_name} local demo]: "
            f"Configuration query received: {prompt[:120]}"
        )


class LLMFactory:
    """Create the supported local responder; reject unavailable providers."""

    @staticmethod
    def create(provider: str = "mock", system_name: str = "Zero Knowledge Location Exposure Agent") -> MockLLM:
        if provider.lower() != "mock":
            raise ValueError("Only the deterministic 'mock' provider is implemented.")
        return MockLLM(system_name)
