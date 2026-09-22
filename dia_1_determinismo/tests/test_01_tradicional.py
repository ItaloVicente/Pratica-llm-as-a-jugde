from dia_1_determinismo.src.functions import soma_sistema_legado


def test_soma_legado_sucesso(number1=1,number2=1):
    """
    O teste unitário clássico passa com sucesso porque
    o sistema legado retorna exatamente o valor esperado.
    """
    resultado = soma_sistema_legado(number1, number2)

    assert resultado == "2"

test_soma_legado_sucesso(1,1)