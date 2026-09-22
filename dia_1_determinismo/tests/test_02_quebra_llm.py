from dia_1_determinismo.src.functions import simular_resposta_llm


def test_falha_por_variacao_semantica():
    """
    O assert quebra porque o LLM insere ruído conversacional
    (ex: 'A resposta para 1 + 1 é 2.'), invalidando a igualdade estrita.
    """
    resultado = simular_resposta_llm("Quanto é 1 + 1? Seja natural na resposta.")

    # Este assert vai reprovar a execução propositalmente
    assert resultado == "2", (
        f"\n[FALHA DETERMINÍSTICA]\n"
        f"Esperava string exata: '2'\n"
        f"O LLM gerou: '{resultado}'"
    )