from deepeval.test_case import LLMTestCase
from deepeval.metrics import HallucinationMetric

from dia_2_deepeval.src.custom_model import GeminiJudge


MODEL_NAME = "gemini-3.5-flash-lite"


def test_debug_hallucination():
    print("\n")
    print("=" * 70)
    print("        DEBUG — HALLUCINATION METRIC")
    print("=" * 70)

    # ---------------------------------------------------------
    # 1. PERGUNTA
    # ---------------------------------------------------------

    pergunta = "Qual é a capital do Brasil?"

    print("\n[1] PERGUNTA")
    print("-" * 70)
    print(pergunta)

    # ---------------------------------------------------------
    # 2. CONTEXTO CORRETO
    # ---------------------------------------------------------

    contexto = [
        "A capital do Brasil é Brasília."
    ]

    print("\n[2] CONTEXTO DE REFERÊNCIA")
    print("-" * 70)
    print(contexto[0])

    # ---------------------------------------------------------
    # 3. RESPOSTA DO LLM
    # ---------------------------------------------------------
    #
    # Colocamos uma resposta propositalmente incorreta.
    # O contexto diz que a capital é Brasília,
    # mas o LLM respondeu Rio de Janeiro.
    #
    # Isso permite demonstrar uma alucinação.
    # ---------------------------------------------------------

    resposta_gerada = (
        "A capital do Brasil é o Rio de Janeiro."
    )

    print("\n[3] RESPOSTA GERADA PELO LLM")
    print("-" * 70)
    print(resposta_gerada)

    # ---------------------------------------------------------
    # 4. TEST CASE
    # ---------------------------------------------------------

    test_case = LLMTestCase(
        input=pergunta,
        actual_output=resposta_gerada,
        context=contexto
    )

    # ---------------------------------------------------------
    # 5. JUIZ
    # ---------------------------------------------------------

    juiz = GeminiJudge(
        model_name=MODEL_NAME
    )

    metrica_hallucinacao = HallucinationMetric(
        threshold=0.7,
        model=juiz,
        include_reason=True
    )

    print("\n[4] LLM-AS-A-JUDGE")
    print("-" * 70)
    print("Executando HallucinationMetric...")

    metrica_hallucinacao.measure(test_case)

    score = metrica_hallucinacao.score
    threshold = metrica_hallucinacao.threshold
    passou = metrica_hallucinacao.is_successful()
    motivo = metrica_hallucinacao.reason

    # ---------------------------------------------------------
    # 6. RESULTADO REAL DA MÉTRICA
    # ---------------------------------------------------------

    print("\n[5] RESULTADO DA MÉTRICA")
    print("-" * 70)

    print(f"Score:      {score:.4f}")
    print(f"Threshold:  {threshold:.4f}")
    print(f"Passou:     {passou}")

    print("\nJustificativa do Gemini:")
    print(motivo)

    # ---------------------------------------------------------
    # 7. ERRO CONCEITUAL
    # ---------------------------------------------------------
    #
    # ATENÇÃO:
    #
    # "is_successful()" significa:
    #
    #     A MÉTRICA passou?
    #
    # Não significa:
    #
    #     O LLM alucinou?
    #
    # Estamos propositalmente usando o booleano de forma
    # incorreta para demonstrar o problema.
    # ---------------------------------------------------------

    alucinou = passou

    print("\n[6] INTERPRETAÇÃO")
    print("-" * 70)

    print(f"metrica.is_successful() = {passou}")
    print(f"alucinou = {alucinou}")

    print("\n")
    print("=" * 70)
    print("      ERRO CONCEITUAL PROPOSITAL")
    print("=" * 70)

    print(
        "\nO booleano 'is_successful()' indica se a métrica "
        "atingiu o threshold."
    )

    print(
        "\nEle NÃO significa diretamente que o LLM alucinou."
    )

    print(
        "\nNeste exemplo, estamos tratando propositalmente "
        "'passou' como se fosse 'alucinou'."
    )

    print(
        "\nEssa interpretação está invertida."
    )

    # ---------------------------------------------------------
    # 8. ASSERT PROPOSITALMENTE ERRADO
    # ---------------------------------------------------------
    #
    # Este assert está propositalmente errado.
    #
    # Se "alucinou" for True, o teste passa.
    #
    # Mas o objetivo da demonstração é justamente mostrar
    # que essa interpretação do booleano está errada.
    #
    # Portanto, o teste deve falhar.
    # ---------------------------------------------------------

    assert not alucinou, (
        "O LLM alucinou, mas o booleano foi interpretado incorretamente."
    )
