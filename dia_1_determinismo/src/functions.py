import os
from google import genai
from google.genai import errors


def soma_sistema_legado(a: int, b: int) -> str:
    """Cálculo estático e determinístico."""
    return str(a + b)


def simular_resposta_llm(pergunta: str) -> str:
    """
    Tenta chamar a API real do Gemini.
    Possui um fallback embutido para garantir que a demonstração
    didática não quebre ao vivo por instabilidade (Erro 503) nos servidores do Google.
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("ERRO: Variável API_KEY não encontrada no ambiente.")

    client = genai.Client(api_key=api_key)

    try:
        # Você pode manter o modelo 3.5 aqui se ele está ativo na sua key
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=pergunta,
        )
        return response.text.strip()

    except errors.APIError as e:
        # Se o Google der 503 (ou qualquer outro erro de API), interceptamos aqui.
        print(f"\n[AVISO DE INFRAESTRUTURA] API instável ({e.message}). Usando fallback didático...")

        # Retornamos uma string que imita a prolixidade do LLM para o teste falhar corretamente
        return "A resposta correta para a sua pergunta matemática é 2."