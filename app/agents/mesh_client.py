"""
Mesh client abstraction for SmartReco.

Provides a common interface for every AI agent.

During development we can use MockMeshClient.

Later we can switch to Groq, OpenAI or Ollama
without changing the agents.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


# ==========================================================
# Base Interface
# ==========================================================

class MeshClient(ABC):
    """
    Abstract LLM interface.
    """

    @abstractmethod
    def generate(
        self,
        prompt: str,
    ) -> str:
        """
        Generate a response.
        """
        raise NotImplementedError
    
# ==========================================================
# Mock Client
# ==========================================================

class MockMeshClient(MeshClient):
    """
    Fake LLM used during development.

    Produces deterministic responses
    so we can test agent workflows.
    """

    def generate(
        self,
        prompt: str,
    ) -> str:

        logger.info(
            "MockMeshClient called."
        )

        return (
            "Mock Response:\n\n"
            f"{prompt}"
        )
        
# ==========================================================
# Real Client (Placeholder)
# ==========================================================

class RealMeshClient(MeshClient):
    """
    Placeholder for production LLM.
    """

    def generate(
        self,
        prompt: str,
    ) -> str:

        raise NotImplementedError(
            "RealMeshClient not implemented yet."
        )
        
# ==========================================================
# Factory
# ==========================================================

def get_mesh_client() -> MeshClient:
    """
    Return the mesh client.

    Later this can read settings
    and choose OpenAI/Groq/Ollama.
    """

    return MockMeshClient()