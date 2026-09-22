# Pratica-llm-as-a-judge

Repositório oficial das atividades práticas do curso de extensão **Testes de Agentes baseados em LLM**.

Este laboratório foi projetado para guiar o estudante desde as limitações dos testes unitários determinísticos até a implementação de testes avançados de avaliação comportamental de agentes autônomos utilizando o framework **DeepEval** e o paradigma **LLM-as-a-Judge**.

---

## 📁 Estrutura do Repositório

O projeto adota o padrão de arquitetura modular de software, separando rigorosamente o código-fonte da aplicação (`src/`) do código das suítes de validação (`tests/`):

```text
Pratica-llm-as-a-judge/
├── dia_1_determinismo/
│   ├── src/
│   │   └── functions.py
│   └── tests/
│       ├── test_01_tradicional.py
│       ├── test_02_quebra_llm.py
│       └── test_03_relevancy.py
├── dia_2_suites_e_agentes
│   ├── src/
│   │   ├── custom_model.py
│   │   └── agent.py
│   └── tests/
│       ├── test_01_full_suite.py
│       ├── test_02_debug_sala.py
│       └── test_03_tool_calling.py
├── atividade_assincrona/
│   ├── src/
│   ├── tests/
│   └── BUG_REPORT_TEMPLATE.md
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🎯 Detalhamento dos Módulos e Atividades

### 1. `dia_1_determinismo/` — O Limite do Paradigma Determinístico
Focado em demonstrar na prática por que testes tradicionais (baseados em igualdade estrita de strings) quebram diante de saídas em linguagem natural.
* **`src/`**: Contém funções determinísticas convencionais e funções simulando respostas de modelos de linguagem (LLMs).
* **`tests/`**:
  * **Script 1 (Teste Unitário Tradicional):** Teste com `pytest` contra uma função estática. Demonstra o fluxo determinístico funcionando perfeitamente (passando com assert exato).
  * **Script 2 (Quebra do Teste com LLM):** Aplicação da mesma lógica de teste rígido sobre o retorno do LLM. Demonstra a falha do teste por variação sintática, mesmo quando a resposta está semanticamente correta.

### 2. `dia_2_deepeval/` — Avaliação com DeepEval (LLM-as-a-Judge)
Introdução à avaliação probabilística automatizada utilizando um LLM como avaliador através do framework DeepEval.
* **`src/`**: Implementação do wrapper customizado utilizando provedor de inferência gratuito para atuar como juiz sem custos de execução.
* **`tests/`**:
  * **Script 1 (Métrica Simples de Relevância):** Configuração do primeiro teste utilizando a métrica *Answer Relevancy* para validar se a resposta atende à pergunta.
  * **Script 2 (Suíte Completa com Múltiplas Métricas):** Execução de testes combinando métricas essenciais (*Faithfulness*, *Answer Relevancy* e *Hallucination*). Demonstra o teste passando com contexto adequado e falhando ao injetar prompts propositalmente errados.

### 3. `dia_3_tool_calling/` — Decisão, Agentes e Debug
Validação comportamental de agentes que executam ações e ferramentas no backend.
* **`src/`**: Implementação do agente e das ferramentas externas (*tools*) que ele pode acionar.
* **`tests/`**:
  * **Script 1 (Debug Guiado em Sala):** Resolução de um cenário prático com erro lógico simples para exercitar a leitura dos relatórios do DeepEval e correção ao vivo.
  * **Script 2 (Teste de Tool Calling):** Avaliação da rota de decisão do agente, garantindo que ele invoque a ferramenta correta e envie os argumentos esperados no payload JSON.

### 4. `atividade_assincrona/` — Desafio: A Falsa Sensação de Segurança
Laboratório de *Code Review* e depuração crítica de testes automatizados.
* **`src/`**: Pipeline de atendimento baseado em IA.
* **`tests/`**: Suíte de testes com inconsistências lógicas de configuração.
* **`BUG_REPORT_TEMPLATE.md`**: Template padronizado para preenchimento e entrega da análise.

---

## ⚙️ Pré-requisitos

Para clonar e executar os laboratórios, você precisa ter instalado no seu ambiente local:
* **Python 3.10** ou superior
* **Git**
* Conexão com a internet para download de dependências e chamadas de API de inferência gratuita

---

## 🛠️ Instalação e Configuração

### 1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/Pratica-llm-as-a-judge.git
cd Pratica-llm-as-a-judge
```

### 2. Criar e Ativar o Ambiente Virtual

* **No Linux/macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

* **No Windows (Prompt/PowerShell):**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. Instalar Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurar Chaves de API
Crie um arquivo `.env` na raiz do projeto (ou exporte as variáveis no seu terminal) com a chave gratuita indicada pelos instrutores no Dia 2:
```bash
API_KEY="sua_chave_aqui"
```

---

## 🧪 Como Executar os Testes

A execução é modularizada por diretório usando o `pytest`:

* **Executar os testes do Dia 1:**
  ```bash
  pytest dia_1_determinismo/tests/ -v
  ```

* **Executar os testes do Dia 2:**
  ```bash
  pytest dia_2_deepeval/tests/ -v
  ```

* **Executar os testes do Dia 3:**
  ```bash
  pytest dia_3_tool_calling/tests/ -v
  ```

* **Executar os testes da Atividade Assíncrona:**
  ```bash
  pytest atividade_assincrona/tests/ -v
  ```

---

## 📝 Instruções da Atividade Assíncrona

A atividade assíncrona simula um dos problemas mais críticos no desenvolvimento de IA: **a falsa sensação de segurança gerada por testes mal configurados**.

### O Desafio
Na pasta `atividade_assincrona/tests/`, você encontrará uma suíte onde a execução apresenta anomalias lógicas:
* **Falsos Positivos:** Testes que passam (ficam verdes), mas na realidade o agente cometeu falhas que deveriam ter sido reprovadas.
* **Falsos Negativos:** Testes que reprovam indevidamente devido a premissas ou asserções inadequadas para a natureza da tarefa.

### O Que Você Deve Fazer
1. Crie uma branch de trabalho no Git:
   ```bash
   git checkout -b feature/debug-seu-nome
   ```
2. Execute a suíte da atividade e analise cada caso de teste individualmente.
3. Inspecione tanto o código da aplicação em `src/` quanto as asserções em `tests/`.
4. Julgue o comportamento real esperado para cada cenário e identifique onde a lógica dos testes foi distorcida.
5. Corrija os testes para que reflitam com precisão o estado real do sistema.
6. Preencha o arquivo `atividade_assincrona/BUG_REPORT_TEMPLATE.md` documentando as falhas identificadas e a justificativa das suas correções e gere uma PR no repositório do Github.
