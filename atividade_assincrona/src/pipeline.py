"""
Pipeline de avaliação de uma aplicação baseada em LLM.

ATENÇÃO:
Este arquivo contém bugs lógicos propositalmente escondidos.

A atividade consiste em executar os testes, verificar que todos
passam e, depois, investigar o código para encontrar os bugs.
"""


# ============================================================
# 1. VALIDAÇÃO DE RESPOSTA
# ============================================================

def validar_resposta(resposta: str) -> bool:
    """
    Verifica se uma resposta possui conteúdo.

    Uma resposta válida precisa:
    - existir;
    - não ser vazia;
    - possuir pelo menos 10 caracteres.
    """

    if resposta is None:
        return False

    resposta = resposta.strip()

    if len(resposta) < 10:
        return False

    # BUG 1:
    # O resultado da validação foi invertido.
    #
    # Uma resposta que passou por todas as validações deveria
    # retornar True.
    #
    # Porém, o código retorna False.

    return False


# ============================================================
# 2. RECUPERAÇÃO DE CONTEXTO
# ============================================================

def recuperar_contexto(pergunta: str) -> str:
    """
    Simula a recuperação de contexto para uma pergunta.

    Em um sistema real, esta função poderia consultar um
    banco vetorial ou outro mecanismo de RAG.
    """

    contexto_base = {
        "Qual é a capital do Brasil?":
            "A capital do Brasil é Brasília.",

        "Qual é a política de devolução?":
            "Produtos podem ser devolvidos em até 30 dias.",

        "Qual é o prazo de entrega?":
            "O prazo de entrega é de até 5 dias úteis."
    }

    # BUG 2:
    # Caso a pergunta não seja encontrada, o sistema deveria
    # retornar um contexto neutro ou informar que não encontrou
    # informação.
    #
    # Em vez disso, utiliza um contexto fixo e incorreto.

    return contexto_base.get(
        pergunta,
        "A capital do Brasil é Rio de Janeiro."
    )


# ============================================================
# 3. AVALIAÇÃO DE RELEVÂNCIA
# ============================================================

def avaliar_relevancia(score: float) -> bool:
    """
    Verifica se uma resposta possui relevância suficiente.

    O score varia de 0 a 1.

    Quanto maior o score, melhor a resposta.
    """

    threshold = 0.8

    # BUG 3:
    # O operador está invertido.
    #
    # O correto seria considerar a resposta aprovada quando:
    #
    #     score >= threshold
    #
    # Porém, o código considera aprovado quando o score
    # está abaixo do threshold.

    return score < threshold


# ============================================================
# 4. SELEÇÃO DE FERRAMENTA
# ============================================================

def selecionar_ferramenta(pergunta: str) -> str:
    """
    Escolhe qual ferramenta deve ser utilizada para responder
    à pergunta do usuário.
    """

    pergunta_lower = pergunta.lower()

    if "pedido" in pergunta_lower:
        return "consultar_pedido"

    if "frete" in pergunta_lower or "cep" in pergunta_lower:
        return "calcular_frete"

    if "devolução" in pergunta_lower:
        return "consultar_politica_devolucao"

    # BUG 4:
    # Para perguntas desconhecidas, o sistema deveria retornar
    # None ou uma indicação de que nenhuma ferramenta foi
    # encontrada.
    #
    # Em vez disso, sempre escolhe uma ferramenta.

    return "consultar_pedido"


# ============================================================
# 5. SCORE FINAL
# ============================================================

def calcular_score_final(
    relevancia: float,
    corretude: float,
    seguranca: float
) -> float:
    """
    Calcula o score final da avaliação.

    Cada métrica possui o mesmo peso.
    """

    # BUG 5:
    # As três métricas deveriam ter o mesmo peso.
    #
    # O cálculo abaixo dá peso dobrado para segurança.
    #
    # Correto:
    #
    #     (relevancia + corretude + seguranca) / 3

    score = (
        relevancia
        + corretude
        + (seguranca * 2)
    ) / 4

    return score


# ============================================================
# 6. PIPELINE COMPLETO
# ============================================================

def executar_pipeline(
    pergunta: str,
    resposta: str,
    relevancia: float,
    corretude: float,
    seguranca: float
) -> dict:
    """
    Executa todas as etapas do pipeline.
    """

    resposta_valida = validar_resposta(resposta)

    contexto = recuperar_contexto(pergunta)

    relevancia_aprovada = avaliar_relevancia(
        relevancia
    )

    ferramenta = selecionar_ferramenta(
        pergunta
    )

    score_final = calcular_score_final(
        relevancia,
        corretude,
        seguranca
    )

    return {
        "resposta_valida": resposta_valida,
        "contexto": contexto,
        "relevancia_aprovada": relevancia_aprovada,
        "ferramenta": ferramenta,
        "score_final": score_final
    }
