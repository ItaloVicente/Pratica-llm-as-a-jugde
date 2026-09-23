from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

from dia_1_determinismo.src.functions import simular_resposta_llm
from dia_1_determinismo.src.custom_judge import GeminiJudge


def test_relevancia_semantica():
    """
    Testa a relevância semântica da resposta utilizando o Gemini
    como LLM-as-a-Judge.

    A resposta não precisa ser textualmente idêntica a uma resposta
    esperada. O Gemini avalia se a resposta é relevante para a pergunta.
    """

    # ---------------------------------------------------------
    # 1. Pergunta
    # ---------------------------------------------------------

    pergunta = "Quanto é 1 + 1? Seja natural na resposta."

    # ---------------------------------------------------------
    # 2. Geração da resposta da aplicação
    # ---------------------------------------------------------

    resposta_gerada = simular_resposta_llm(pergunta)

    print("\n")
    print("=" * 60)
    print("RESPOSTA GERADA PELA APLICAÇÃO")
    print("=" * 60)

    print(f"\nPergunta:")
    print(pergunta)

    print(f"\nResposta:")
    print(resposta_gerada)

    # ---------------------------------------------------------
    # 3. Gemini como LLM-as-a-Judge
    # ---------------------------------------------------------

    juiz_gemini = GeminiJudge(
        model_name="gemini-3.5-flash-lite"
    )

    # ---------------------------------------------------------
    # 4. Caso de teste
    # ---------------------------------------------------------

    test_case = LLMTestCase(
        input=pergunta,
        actual_output=resposta_gerada
    )

    # ---------------------------------------------------------
    # 5. Métrica
    # ---------------------------------------------------------

    metrica_relevancia = AnswerRelevancyMetric(
        threshold=0.7,
        model=juiz_gemini,
        include_reason=True
    )

    # ---------------------------------------------------------
    # 6. Executa a avaliação
    # ---------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("LLM-AS-A-JUDGE")
    print("=" * 60)

    print("\nMétrica: Answer Relevancy")
    print("Chamando Gemini como juiz...")

    metrica_relevancia.measure(test_case)

    # ---------------------------------------------------------
    # 7. Resultado
    # ---------------------------------------------------------

    score = metrica_relevancia.score
    threshold = metrica_relevancia.threshold
    passou = metrica_relevancia.is_successful()
    motivo = metrica_relevancia.reason

    print("\n")
    print("-" * 60)
    print("RESULTADO DA AVALIAÇÃO")
    print("-" * 60)

    print(f"\nScore:      {score:.4f}")
    print(f"Threshold:  {threshold:.4f}")
    print(f"Passou:     {passou}")

    print("\nJustificativa do Gemini:")
    print(motivo)

    # ---------------------------------------------------------
    # 8. Resumo
    # ---------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("RESUMO")
    print("=" * 60)

    print(f"\nPergunta:")
    print(pergunta)

    print(f"\nResposta:")
    print(resposta_gerada)

    print(f"\nAnswer Relevancy:")
    print(
        f"Score = {score:.4f} | "
        f"Threshold = {threshold:.4f} | "
        f"{'PASS' if passou else 'FAIL'}"
    )

    # ---------------------------------------------------------
    # 9. Assert do pytest
    # ---------------------------------------------------------

    assert passou, (
        f"Answer Relevancy abaixo do threshold. "
        f"Score: {score:.4f}, "
        f"Threshold: {threshold:.4f}"
    )

    print("\n")
    print("=" * 60)
    print("TESTE APROVADO")
    print("=" * 60)
