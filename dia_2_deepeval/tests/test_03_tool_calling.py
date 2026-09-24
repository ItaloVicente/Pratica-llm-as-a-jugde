import json
import os

from google import genai

from deepeval.test_case import LLMTestCase, ToolCall
from deepeval.metrics import ArgumentCorrectnessMetric

from dia_2_deepeval.src.custom_model import GeminiJudge


# ============================================================
# CONFIGURAÇÃO
# ============================================================

MODEL_NAME = "gemini-3.5-flash-lite"


# ============================================================
# FERRAMENTAS DISPONÍVEIS PARA O AGENTE
# ============================================================

def consultar_pedido(numero_pedido: str):
    """
    Consulta o status e a previsão de entrega de um pedido.
    """

    pedidos = {
        "12345": {
            "status": "Enviado",
            "previsao_entrega": "25/09/2026"
        },
        "67890": {
            "status": "Processando",
            "previsao_entrega": "30/09/2026"
        }
    }

    pedido = pedidos.get(numero_pedido)

    if pedido is None:
        return {
            "erro": "Pedido não encontrado"
        }

    return {
        "numero_pedido": numero_pedido,
        **pedido
    }


def calcular_frete(cep: str):
    """
    Calcula o valor e o prazo do frete.
    """

    return {
        "cep": cep,
        "valor": 25.90,
        "prazo": "5 dias úteis"
    }


def consultar_politica_devolucao():
    """
    Consulta a política de devolução da loja.
    """

    return {
        "prazo": "30 dias",
        "produtos_em_promocao": False
    }


FERRAMENTAS = {
    "consultar_pedido": consultar_pedido,
    "calcular_frete": calcular_frete,
    "consultar_politica_devolucao": consultar_politica_devolucao,
}


# ============================================================
# GEMINI COMO AGENTE
# ============================================================

def selecionar_ferramentas(pergunta: str):
    """
    Pede ao Gemini para decidir quais ferramentas precisam
    ser utilizadas para responder à pergunta.

    O Gemini pode escolher uma ou mais ferramentas.
    """

    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError("API_KEY ausente.")

    client = genai.Client(api_key=api_key)

    ferramentas_descricao = """
    1. consultar_pedido(numero_pedido)
       Consulta o status e a previsão de entrega de um pedido.

    2. calcular_frete(cep)
       Calcula o valor e o prazo do frete.

    3. consultar_politica_devolucao()
       Consulta as regras de devolução da loja.
    """

    prompt = f"""
Você é um agente de atendimento de uma loja.

Pergunta do usuário:
{pergunta}

Ferramentas disponíveis:
{ferramentas_descricao}

Analise a pergunta e escolha TODAS as ferramentas necessárias
para conseguir responder completamente.

Uma pergunta pode precisar de mais de uma ferramenta.

Responda SOMENTE em JSON, seguindo exatamente este formato:

{{
    "tools": [
        {{
            "tool_name": "nome_da_ferramenta",
            "arguments": {{
                "argumento": "valor"
            }}
        }}
    ]
}}

Não invente ferramentas.
Não adicione explicações fora do JSON.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    texto = response.text.strip()

    # Remove possíveis blocos ```json ... ```
    if texto.startswith("```"):
        texto = texto.replace("```json", "")
        texto = texto.replace("```", "")
        texto = texto.strip()

    return json.loads(texto)


# ============================================================
# EXECUTA UMA FERRAMENTA
# ============================================================

def executar_ferramenta(
    nome_ferramenta: str,
    argumentos: dict
):
    """
    Executa uma ferramenta escolhida pelo agente.
    """

    if nome_ferramenta not in FERRAMENTAS:
        raise ValueError(
            f"Ferramenta inexistente: {nome_ferramenta}"
        )

    ferramenta = FERRAMENTAS[nome_ferramenta]

    return ferramenta(**argumentos)


# ============================================================
# GERAR RESPOSTA FINAL
# ============================================================

def gerar_resposta_final(
    pergunta: str,
    resultados_ferramentas: list
):
    """
    Usa o Gemini para transformar os resultados das ferramentas
    em uma resposta final para o usuário.
    """

    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError("API_KEY ausente.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
Você é um agente de atendimento de uma loja.

Pergunta do usuário:
{pergunta}

Resultados obtidos pelas ferramentas:

{resultados_ferramentas}

Responda ao usuário de forma natural e objetiva.

Utilize somente as informações presentes nos resultados
das ferramentas.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
    )

    return response.text.strip()


# ============================================================
# TESTE PRINCIPAL
# ============================================================

def test_tool_calling():

    print("\n")
    print("=" * 70)
    print("        TOOL CALLING — MÚLTIPLAS FERRAMENTAS")
    print("=" * 70)

    # ========================================================
    # PERGUNTA
    # ========================================================

    pergunta_usuario = (
        "Qual é o status do meu pedido 12345 "
        "e quanto vou pagar de frete para o CEP 60000-000?"
    )

    print("\n[1] PERGUNTA DO USUÁRIO")
    print("-" * 70)
    print(pergunta_usuario)

    # ========================================================
    # FERRAMENTAS ESPERADAS
    # ========================================================

    ferramenta_pedido_esperada = ToolCall(
        name="consultar_pedido",
        input_parameters={
            "numero_pedido": "12345"
        }
    )

    ferramenta_frete_esperada = ToolCall(
        name="calcular_frete",
        input_parameters={
            "cep": "60000-000"
        }
    )

    ferramentas_esperadas = [
        ferramenta_pedido_esperada,
        ferramenta_frete_esperada
    ]

    print("\n[2] FERRAMENTAS ESPERADAS")
    print("-" * 70)

    print(
        f"1. {ferramenta_pedido_esperada.name}"
        f"({ferramenta_pedido_esperada.input_parameters})"
    )

    print(
        f"2. {ferramenta_frete_esperada.name}"
        f"({ferramenta_frete_esperada.input_parameters})"
    )

    # ========================================================
    # GEMINI ESCOLHE AS FERRAMENTAS
    # ========================================================

    print("\n[3] AGENTE")
    print("-" * 70)
    print("Gemini está analisando a pergunta...")
    print("O agente pode escolher mais de uma ferramenta.")

    decisao = selecionar_ferramentas(
        pergunta_usuario
    )

    ferramentas_escolhidas = decisao.get(
        "tools",
        []
    )

    print(
        f"\nQuantidade de ferramentas escolhidas: "
        f"{len(ferramentas_escolhidas)}"
    )

    for i, ferramenta in enumerate(
        ferramentas_escolhidas,
        start=1
    ):
        print(f"\nFerramenta {i}:")
        print(f"  Nome:      {ferramenta['tool_name']}")
        print(f"  Argumentos: {ferramenta.get('arguments', {})}")

    # ========================================================
    # EXECUTA TODAS AS FERRAMENTAS
    # ========================================================

    print("\n[4] EXECUÇÃO DAS FERRAMENTAS")
    print("-" * 70)

    ferramentas_utilizadas = []
    resultados_ferramentas = []

    for ferramenta in ferramentas_escolhidas:

        nome_ferramenta = ferramenta["tool_name"]
        argumentos = ferramenta.get(
            "arguments",
            {}
        )

        resultado = executar_ferramenta(
            nome_ferramenta,
            argumentos
        )

        ferramenta_utilizada = ToolCall(
            name=nome_ferramenta,
            input_parameters=argumentos
        )

        ferramentas_utilizadas.append(
            ferramenta_utilizada
        )

        resultados_ferramentas.append({
            "ferramenta": nome_ferramenta,
            "resultado": resultado
        })

        print(f"\nFerramenta: {nome_ferramenta}")
        print(f"Argumentos: {argumentos}")
        print(f"Resultado:  {resultado}")

    # ========================================================
    # TOOL CALLS REGISTRADAS
    # ========================================================

    print("\n[5] TOOL CALLS REGISTRADAS")
    print("-" * 70)

    for i, ferramenta in enumerate(
        ferramentas_utilizadas,
        start=1
    ):
        print(f"\n{i}. {ferramenta.name}")
        print(
            f"   Argumentos: "
            f"{ferramenta.input_parameters}"
        )

    # ========================================================
    # RESPOSTA FINAL DO AGENTE
    # ========================================================

    print("\n[6] RESPOSTA FINAL DO AGENTE")
    print("-" * 70)

    resposta_gerada = gerar_resposta_final(
        pergunta_usuario,
        resultados_ferramentas
    )

    print(resposta_gerada)

    # ========================================================
    # TEST CASE DO DEEPEVAL
    # ========================================================

    test_case = LLMTestCase(
        input=pergunta_usuario,
        actual_output=resposta_gerada,

        tools_called=ferramentas_utilizadas,

        expected_tools=ferramentas_esperadas
    )

    # ========================================================
    # JUIZ
    # ========================================================

    print("\n[7] LLM-AS-A-JUDGE")
    print("-" * 70)

    juiz = GeminiJudge(
        model_name=MODEL_NAME
    )

    metrica = ArgumentCorrectnessMetric(
        threshold=0.7,
        model=juiz,
        include_reason=True
    )

    print("Avaliando as chamadas das ferramentas...")

    metrica.measure(test_case)

    # ========================================================
    # RESULTADO
    # ========================================================

    print("\n[8] RESULTADO DA AVALIAÇÃO")
    print("-" * 70)

    score = metrica.score
    passou = metrica.is_successful()

    print(f"Score:      {score:.4f}")
    print(f"Threshold:  {metrica.threshold:.4f}")
    print(f"Passou:     {passou}")

    print("\nJustificativa do Gemini:")
    print(metrica.reason)

    # ========================================================
    # RESUMO
    # ========================================================

    print("\n")
    print("=" * 70)
    print("                         RESUMO")
    print("=" * 70)

    print("\nPergunta:")
    print(f"  {pergunta_usuario}")

    print("\nFerramentas esperadas:")

    for ferramenta in ferramentas_esperadas:
        print(
            f"  - {ferramenta.name}"
            f"({ferramenta.input_parameters})"
        )

    print("\nFerramentas escolhidas:")

    for ferramenta in ferramentas_utilizadas:
        print(
            f"  - {ferramenta.name}"
            f"({ferramenta.input_parameters})"
        )

    print("\nResposta do agente:")
    print(f"  {resposta_gerada}")

    print("\nArgument Correctness:")
    print(
        f"  Score = {score:.4f}"
        f" -> {'PASS' if passou else 'FAIL'}"
    )

    # ========================================================
    # ASSERT
    # ========================================================

    assert passou, (
        "As chamadas das ferramentas realizadas pelo agente "
        "não foram consideradas corretas pelo juiz."
    )

    print("\n")
    print("=" * 70)
    print("                    TESTE APROVADO")
    print("=" * 70)
