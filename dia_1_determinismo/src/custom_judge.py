import os

from google import genai
from deepeval.models.base_model import DeepEvalBaseLLM


class GeminiJudge(DeepEvalBaseLLM):
    """
    Wrapper para utilizar o Gemini como LLM-as-a-Judge no DeepEval.
    """

    def __init__(self, model_name="gemini-3.5-flash-lite"):
        self.model_name = model_name

        api_key = os.getenv("API_KEY")

        if not api_key:
            raise ValueError(
                "API_KEY ausente no ambiente."
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def load_model(self):
        return self.client

    def generate(self, prompt: str) -> str:
        """
        Geração síncrona.
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        return response.text.strip()

    async def a_generate(self, prompt: str) -> str:
        """
        Geração assíncrona.

        O DeepEval utiliza este método durante a execução
        assíncrona das métricas.
        """

        response = await self.client.aio.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        return response.text.strip()

    def get_model_name(self):
        return self.model_name
