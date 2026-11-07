# Bug Report

## Bug 1

### Localização
`src/pipeline.py` — função `validar_resposta`

### Problema
A função devolve sempre `False` mesmo para entradas não-vazias e com mais de 10 caracteres.

### Comportamento atual
Função sempre retorna `False`.
### Comportamento esperado
Retornar `True` quando a resposta conter pelo menos 10 carateres após o strip.
### Correções feitas
Substituido o último `return False` por `return True`

## Bug 2

### Localização
`tests/test_pipeline.py` — função `test_validar_resposta`

### Problema
O teste sempre passa mesmo com respostas inválidas.

### Comportamento atual
Verifica apenas se o retorno da função é um booleano.
### Comportamento esperado
Verificar se o booleano retornado é `True`.
### Correções feitas
Adicionada a linha `assert resultado` para verificar o valor de resultado. Agora o teste deve ser bem-sucedido somente quando o retorno da função for um booleano com valor `True`.

## Bug 3

### Localização
`src/pipeline.py` — função `recuperar_contexto`.

### Problema
O valor padrão de retorno da função não condiz com a realidade e pode causar confusões.

### Comportamento atual
A função retorna a string `"A capital do Brasil é Rio de Janeiro."` em casos em que a pergunta não está no dicionário. Ex:

`pergunta -> "Qual a capital da França?"`

`return -> "A capital do Brasil é Rio de Janeiro."`
### Comportamento esperado
Retorno ser None quando a não houver contexto conhecido para a pergunta, batendo com a verificação feita no teste.
### Correções feitas
Foi retirado o valor de fallback customizado de `contexto_base.get(pergunta)`.

## Bug 4

### Localização
`src/pipeline.py` — função `avaliar_relevancia`

### Problema
A comparação de score com threshold está errada. A função trata valores de score baixos como respostas boas.

### Comportamento atual
`return score < threshold `.
### Comportamento esperado
`return score > threshold`.
### Correções feitas
Alterado o símbolo de comparação no return para bater com o comportamento esperado.

## Bug 5

### Localização
`tests/test_pipeline.py` — função `test_avaliar_relevancia`

### Problema
O teste sempre passa independente da relação entre score e threshold.

### Comportamento atual
Teste é sempre bem-sucedido.
### Comportamento esperado
Teste ser bem-sucedido apenas quando o score for maior que o threshold.
### Correções feitas
Adicionada uma linha com `assert resultado`.

## Bug 6

### Localização
`src/pipeline.py` — função `selecionar_ferramenta`.

### Problema
Perguntas que não usam nenhuma das ferramentas catalogadas levam ao retorno da ferramenta `"consultar_pedido"`.

### Comportamento atual
A função retorna a string `"consultar_pedido"` em casos em que a pergunta não exige nenhuma ferramenta. 
### Comportamento esperado
Retorno ser None quando não houver a necessidade de usar as ferramentas disponibilizadas.
### Correções feitas
Último return foi alterado de `return "consultar_pedido"` para return None, fazendo o test_selecionar_ferramenta falhar caso não seja preciso nenhuma ferramenta.

## Bug 7

### Localização
`src/pipeline.py` — função `calcular_score_final`

### Problema
O cálculo do score está errado.

### Comportamento atual
A métrica `seguranca` possui um peso maior no cálculo em relação as outras

`score = (
        relevancia
        + corretude
        + (seguranca * 2)
    ) / 4`
### Comportamento esperado
Todas as métricas devem ter o mesmo peso
### Correções feitas
Alterado o cálculo de score.

`score = (
        relevancia
        + corretude
        + seguranca 
    ) / 3`

## Bug 8

### Localização
`tests/test_pipeline.py` — função `test_pipeline_completo`

### Problema
O teste não verifica o valor de `resultado["resposta_valida"]` e `resultado["relevancia_aprovada]`, apenas checa se são valores booleanos.

### Comportamento atual
Teste é bem-sucedido mesmo quando não possui uma resposta válida ou relevância satisfatória.
### Comportamento esperado
Teste falhar quando bem-sucedido não possuir uma resposta válida ou relevância satisfatória.
### Correções feitas
Adicionada as linhas com `assert resultado["resposta_valida"]` e `assert resultado["relevancia_valida]`.