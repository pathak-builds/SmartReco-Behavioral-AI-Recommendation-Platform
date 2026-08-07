"""
Mesh client abstraction for SmartReco.

Provides a common interface for every AI agent.

During development we can use MockMeshClient.

Later we can switch to Groq, OpenAI or Ollama
without changing the agents.
"""

from __future__ import annotations

from openai import OpenAI

from app.config import settings

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
# Groq Client
# ==========================================================

class GroqClient(MeshClient):
    """
    Groq API client.
    """

    def __init__(self):

        self.client = OpenAI(

            base_url="https://api.groq.com/openai/v1",

            api_key=settings.GROQ_API_KEY,

        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        logger.info(
            "Calling Groq API..."
        )

        response = self.client.chat.completions.create(

            model=settings.MODEL_NAME,

            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],

            temperature=0.3,

            max_tokens=250,

        )

        return response.choices[0].message.content   
# ==========================================================
# Real Client (Placeholder)
# ==========================================================

class RealMeshClient(MeshClient):
    """
    Production Mesh API client.
    """

    def __init__(self):

        self.client = OpenAI(

            base_url=settings.MESH_API_URL,

            api_key=settings.MESH_API_KEY,

        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        logger.info(
            "Calling Mesh API..."
        )

        response = self.client.chat.completions.create(

            model=settings.MODEL_NAME,

            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],

            temperature=0.3,

            max_tokens=250,

        )

        return response.choices[0].message.content
        
# ==========================================================
# Factory
# ==========================================================

from app.config import settings


# def get_mesh_client() -> MeshClient:
#     """
#     Return the configured AI client.
#     """

#     if settings.LLM_PROVIDER.lower() == "mesh":

#         logger.info("Using Mesh API")

#         return RealMeshClient()

#     logger.info("Using Mock Mesh Client")

#     return MockMeshClient()

def get_mesh_client() -> MeshClient:
    """
    Return the configured AI client.
    """

    provider = settings.LLM_PROVIDER.lower()

    if provider == "groq":

        logger.info("Using Groq API")

        return GroqClient()

    elif provider == "mesh":

        logger.info("Using Mesh API")

        return RealMeshClient()

    logger.info("Using Mock Mesh Client")

    return MockMeshClient()