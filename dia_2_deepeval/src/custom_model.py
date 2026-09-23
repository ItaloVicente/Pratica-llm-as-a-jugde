import os
import asyncio
import random

from google import genai
from google.genai import errors

from deepeval.models.base_model import DeepEvalBaseLLM


class GeminiJudge(DeepEvalBaseLLM):

    def __init__(
        self,
        model_name="gemini-3.5-flash-lite",
        intervalo_entre_chamadas=2.0
    ):
        """
        Modelo utilizado pelo DeepEval como LLM-as-a-Judge.

        intervalo_entre_chamadas:
            Tempo mínimo aproximado entre chamadas ao Gemini.
            Ajuda a reduzir erros 503 causados por várias requisições
            próximas umas das outras.
        """

        self.model_name = model_name
        self.intervalo_entre_chamadas = intervalo_entre_chamadas

        api_key = os.getenv("API_KEY")

        if not api_key:
            raise ValueError(
                "API_KEY ausente no ambiente."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        # Controle para evitar múltiplas chamadas simultâneas.
        self._semaphore = asyncio.Semaphore(1)

        # Marca o momento da última chamada.
        self._ultima_chamada = 0.0

    # ============================================================
    # DEEPEVAL
    # ============================================================

    def load_model(self):
        return self.client

    # ============================================================
    # CHAMADA SÍNCRONA
    # ============================================================

    def generate(self, prompt: str) -> str:

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt
        )

        if not response.text:
            raise RuntimeError(
                "O Gemini retornou uma resposta vazia."
            )

        return response.text.strip()

    # ============================================================
    # CHAMADA ASSÍNCRONA
    # ============================================================

    async def a_generate(self, prompt: str) -> str:

        # --------------------------------------------------------
        # O DeepEval pode chamar o juiz de forma concorrente.
        #
        # O semaphore garante que apenas uma requisição ao Gemini
        # seja executada por vez.
        # --------------------------------------------------------

        async with self._semaphore:

            # ----------------------------------------------------
            # Controle de intervalo entre chamadas
            # ----------------------------------------------------

            agora = asyncio.get_running_loop().time()

            tempo_desde_ultima = (
                agora - self._ultima_chamada
            )

            if tempo_desde_ultima < self.intervalo_entre_chamadas:

                espera = (
                    self.intervalo_entre_chamadas
                    - tempo_desde_ultima
                )

                print(
                    f"\n[JUIZ] Aguardando "
                    f"{espera:.1f}s antes da próxima chamada..."
                )

                await asyncio.sleep(espera)

            # ----------------------------------------------------
            # Retry com backoff
            # ----------------------------------------------------

            max_tentativas = 5

            for tentativa in range(1, max_tentativas + 1):

                try:

                    print(
                        f"\n[JUIZ] Chamando Gemini "
                        f"(tentativa {tentativa}/{max_tentativas})..."
                    )

                    self._ultima_chamada = (
                        asyncio.get_running_loop().time()
                    )

                    response = (
                        await self.client.aio.models.generate_content(
                            model=self.model_name,
                            contents=prompt
                        )
                    )

                    if not response.text:
                        raise RuntimeError(
                            "O Gemini retornou uma resposta vazia."
                        )

                    print("[JUIZ] Resposta recebida.")

                    return response.text.strip()

                except errors.APIError as e:

                    erro = str(e)

                    # ==================================================
                    # 503 - SERVIDOR SOBRECARREGADO
                    # ==================================================

                    if "503" in erro:

                        if tentativa == max_tentativas:
                            raise RuntimeError(
                                "Gemini continuou retornando HTTP 503 "
                                f"após {max_tentativas} tentativas.\n"
                                f"Erro original: {erro}"
                            )

                        # Backoff progressivo:
                        #
                        # tentativa 1 -> ~3s
                        # tentativa 2 -> ~6s
                        # tentativa 3 -> ~12s
                        # tentativa 4 -> ~24s
                        #

                        espera = (
                            3 * (2 ** (tentativa - 1))
                            + random.uniform(0, 1)
                        )

                        print(
                            "\n[JUIZ] Gemini retornou 503 "
                            "(servidor temporariamente sobrecarregado)."
                        )

                        print(
                            f"[JUIZ] Aguardando "
                            f"{espera:.1f}s antes de tentar novamente..."
                        )

                        await asyncio.sleep(espera)

                        continue

                    # ==================================================
                    # 429 - LIMITE DE REQUISIÇÕES
                    # ==================================================

                    if "429" in erro:

                        if tentativa == max_tentativas:
                            raise RuntimeError(
                                "Limite de requisições do Gemini "
                                f"atingido após {max_tentativas} tentativas.\n"
                                f"Erro original: {erro}"
                            )

                        # Espera maior para permitir que a janela
                        # de rate limit seja renovada.
                        espera = 20 + (
                            10 * tentativa
                        )

                        print(
                            "\n[JUIZ] Gemini retornou 429 "
                            "(limite de requisições)."
                        )

                        print(
                            f"[JUIZ] Aguardando "
                            f"{espera}s antes de tentar novamente..."
                        )

                        await asyncio.sleep(espera)

                        continue

                    # ==================================================
                    # OUTRO ERRO DA API
                    # ==================================================

                    raise RuntimeError(
                        "Erro da API do Gemini:\n"
                        f"{erro}"
                    )

                except Exception as e:

                    raise RuntimeError(
                        "Erro inesperado ao executar o Gemini Judge:\n"
                        f"{e}"
                    )

            raise RuntimeError(
                "O Gemini Judge terminou sem produzir uma resposta."
            )

    # ============================================================
    # NOME DO MODELO
    # ============================================================

    def get_model_name(self):
        return self.model_name