from atividade_assincrona.src.pipeline import (
    validar_resposta,
    recuperar_contexto,
    avaliar_relevancia,
    selecionar_ferramenta,
    calcular_score_final,
    executar_pipeline,
)


# ============================================================
# TESTE 1 — VALIDAÇÃO DE RESPOSTA
# ============================================================

def test_validar_resposta():

    resposta = "Esta é uma resposta válida."

    resultado = validar_resposta(resposta)

    # O teste está verificando apenas que a função retorna
    # um booleano.

    assert isinstance(resultado, bool)


# ============================================================
# TESTE 2 — CONTEXTO
# ============================================================

def test_recuperar_contexto():

    pergunta = "Qual é a capital do Brasil?"

    contexto = recuperar_contexto(pergunta)

    assert contexto is not None
    assert isinstance(contexto, str)
    assert len(contexto) > 0


# ============================================================
# TESTE 3 — RELEVÂNCIA
# ============================================================

def test_avaliar_relevancia():

    score = 0.95

    resultado = avaliar_relevancia(score)

    # O teste verifica apenas o tipo retornado.
    # Não verifica se 0.95 deveria ser aprovado.

    assert isinstance(resultado, bool)


# ============================================================
# TESTE 4 — SELEÇÃO DE FERRAMENTA
# ============================================================

def test_selecionar_ferramenta():

    pergunta = "Qual é o status do meu pedido 12345?"

    ferramenta = selecionar_ferramenta(pergunta)

    assert ferramenta is not None
    assert isinstance(ferramenta, str)


# ============================================================
# TESTE 5 — SCORE FINAL
# ============================================================

def test_score_final():

    score = calcular_score_final(
        relevancia=0.9,
        corretude=0.9,
        seguranca=0.9
    )

    assert 0 <= score <= 1


# ============================================================
# TESTE 6 — PIPELINE COMPLETO
# ============================================================

def test_pipeline_completo():

    resultado = executar_pipeline(
        pergunta="Qual é a capital do Brasil?",
        resposta="A capital do Brasil é Brasília.",
        relevancia=0.95,
        corretude=0.95,
        seguranca=0.95
    )

    assert "resposta_valida" in resultado
    assert "contexto" in resultado
    assert "relevancia_aprovada" in resultado
    assert "ferramenta" in resultado
    assert "score_final" in resultado

    assert isinstance(
        resultado["resposta_valida"],
        bool
    )

    assert isinstance(
        resultado["relevancia_aprovada"],
        bool
    )

    assert 0 <= resultado["score_final"] <= 1
