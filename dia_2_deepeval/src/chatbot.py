import os
import asyncio

from google import genai
from google.genai import errors


def consultar_assistente_rag(
    pergunta: str,
    contexto: str
) -> str:
    """
    Simula uma chamada RAG (Retrieval-Augmented Generation).

    O contexto recuperado é enviado ao Gemini juntamente com a pergunta.

    Em caso de erro temporário da API:
        - 503 -> realiza novas tentativas
        - 429 -> aguarda antes de tentar novamente

    Caso todas as tentativas falhem, utiliza um fallback didático.
    """

    # ============================================================
    # API KEY
    # ============================================================

    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError(
            "API_KEY ausente."
        )

    # ============================================================
    # CLIENTE
    # ============================================================

    client = genai.Client(
        api_key=api_key
    )

    # ============================================================
    # PROMPT RAG
    # ============================================================

    prompt_completo = (
        f"Contexto: {contexto}\n\n"
        f"Pergunta: {pergunta}\n\n"
        "Responda estritamente com base no contexto."
    )

    # ============================================================
    # RETRIES
    # ============================================================

    max_tentativas = 4

    for tentativa in range(1, max_tentativas + 1):

        try:

            print(
                f"\n[CHATBOT] Consultando Gemini "
                f"(tentativa {tentativa}/{max_tentativas})..."
            )

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt_completo,
            )

            if not response.text:
                raise RuntimeError(
                    "O Gemini retornou uma resposta vazia."
                )

            print("[CHATBOT] Resposta recebida.")

            return response.text.strip()

        except errors.APIError as e:

            erro = str(e)

            # ====================================================
            # 503
            # ====================================================

            if "503" in erro:

                if tentativa == max_tentativas:
                    break

                espera = 3 * (2 ** (tentativa - 1))

                print(
                    "\n[CHATBOT] Gemini retornou 503 "
                    "(servidor temporariamente sobrecarregado)."
                )

                print(
                    f"[CHATBOT] Tentando novamente em "
                    f"{espera}s..."
                )

                # Como esta função é síncrona, usamos uma espera
                # bloqueante simples.
                import time
                time.sleep(espera)

                continue

            # ====================================================
            # 429
            # ====================================================

            if "429" in erro:

                if tentativa == max_tentativas:
                    break

                espera = 20 + (10 * tentativa)

                print(
                    "\n[CHATBOT] Gemini retornou 429 "
                    "(limite de requisições)."
                )

                print(
                    f"[CHATBOT] Aguardando "
                    f"{espera}s antes de tentar novamente..."
                )

                import time
                time.sleep(espera)

                continue

            # ====================================================
            # OUTRO ERRO
            # ====================================================

            print(
                "\n[CHATBOT] Erro inesperado na API:"
            )

            print(erro)

            break

    # ============================================================
    # FALLBACK DIDÁTICO
    # ============================================================

    print(
        "\n[CHATBOT] Todas as tentativas falharam."
    )

    print(
        "[CHATBOT] Utilizando fallback didático."
    )

    return (
        "Não é possível realizar a devolução. "
        "Conforme a política, itens comprados em promoção "
        "não são elegíveis para reembolso."
    )