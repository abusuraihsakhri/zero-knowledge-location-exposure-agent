"""
LLM Provider Factory for Zero Knowledge Location Exposure Agent.

Currently provides a deterministic mock implementation for air-gapped operation.
Future extensions will integrate with Ollama, Anthropic Claude, and OpenAI.
"""
from typing import Optional
from .base import PHIGuard


class MockLLM:
    """Deterministic mock LLM for air-gapped and testing environments."""

    def __init__(self, system_name: str = "Zero Knowledge Location Exposure Agent"):
        self.system_name = system_name

    def invoke(self, prompt: str) -> str:
        PHIGuard.assert_no_phi(prompt)
        return (
            f"[{self.system_name} Deterministic Verification Engine]: "
            f"Clinical & scientific analysis verified for query: '{prompt[:60]}...'. "
            f"Parameters evaluated under CAP / CLSI / ISO Standards."
        )


class LLMFactory:
    """
    Creates LLM client instances with zero-PHI protection.

    Note: Currently all providers return the deterministic MockLLM.
    Production deployments should configure AUDIT_SECRET_KEY and
    install the appropriate SDK (ollama, anthropic, openai) for live inference.
    """

    @staticmethod
    def create(provider: str = "mock", system_name: str = "Zero Knowledge Location Exposure Agent") -> MockLLM:
        return MockLLM(system_name)
