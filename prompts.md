# 🤖 Documentação do Uso de Inteligência Artificial — `prompts.md`

**Disciplina:** Computational Thinking with Python  
**Projeto:** ZelaSP — Zeladoria Cidadã Inteligente  
**Global Solution 2026.2:** CitizenTech · FIAP  
**Integrantes:**  
* Gustavo Rezende Louro — RM570708  
* João Pedro Lagonegro Bosco e Silva — RM569444  
* João Pedro Maschion da Cruz Sá — RM570509  
* Lucas Henrique Alves da Silva — RM572216  

---

## 1. Ferramentas de IA Utilizadas e Finalidades

* **Google Antigravity (Gemini 3.8 Flash):** Utilizado como copiloto de raciocínio de engenharia de software para ideação da estrutura do menu, desenho de casos de teste de exceções (`try/except`) e validação dos critérios acadêmicos do edital da FIAP.
* **Claude / ChatGPT (Análise Conceitual):** Utilizado em sessões prévias para pesquisa sobre tratamento assintótico de algoritmos de busca e ordenação.

---

## 2. Prompts Utilizados Durante o Desenvolvimento

### Prompt 1: Estruturação dos Requisitos Obrigatórios
> *"Como estruturar uma aplicação em Python puro que atenda 100% aos critérios da Global Solution da FIAP para Computational Thinking (menu interativo com match/case, estruturas de repetição while/for, funções com retorno, tratamento com try/except, listas/tuplas/dicionários e persistência em JSON), aplicada à triagem de cabos rompidos e entulho em São Paulo?"*

### Prompt 2: Validação Defensiva e Prevenção de Erros
> *"Quais são os principais erros de entrada de usuário que podem quebrar a aplicação ao ler dados do teclado (ex: strings vazias, valores fora da faixa, caracteres em campos numéricos) e como capturá-los com try/except e loops de validação sem travar o programa?"*

### Prompt 3: Regras de Negócio e Cálculo de Risco
> *"Crie uma política acadêmica única de classificação de prioridade urbana de 1 a 5: risco elétrico marcado resulta em nível 5 em todas as categorias; sem risco elétrico marcado, bueiro inicia em 5, buraco em 4, fios e poda em 3, entulho em 2 e carro abandonado em 1; a partir de 10 apoios comunitários, acrescentar apenas um único nível a partir da base (teto 5), e bloquear apoio em ocorrências com status RESOLVIDO."*

---

## 3. Funcionalidades Desenvolvidas e Modificadas pelo Grupo

1. **Persistência em JSON (`carregar_ocorrencias` e `salvar_ocorrencias`):**
   * *Sugestão da IA:* A IA sugeriu gravar os dados imediatamente após cada operação de adição ou edição.
   * *Ajuste do Grupo:* O grupo adicionou a verificação prévia com `os.path.exists()` e um gerador de base demonstrativa (`criar_dados_exemplo()`), alinhado aos 6 bairros de São Paulo e à tabela única de prioridade para garantir inicialização limpa caso o arquivo JSON ainda não exista.
2. **Apoio Comunitário Manual com Recálculo e Bloqueio (`aplicar_apoio_ocorrencia` e `apoiar_ocorrencia_existente`):**
   * *Desenvolvimento da Equipe:* Além de permitir apoiar chamados já cadastrados para incentivar a redução de relatos repetidos, a equipe implementou o bloqueio para ocorrências com status `RESOLVIDO` (preservando o contador) e o recálculo automático da prioridade a partir da base quando a contagem atinge 10 apoios.
3. **Validação Estrita de Risco e Seleção Demonstrativa de Foto:**
   * *Ajuste do Grupo:* Criamos a função `ler_confirmacao_sim_nao()` exigindo respostas válidas (`s`, `sim`, `n`, `não`, `nao`) antes de calcular a prioridade, e ajustamos o campo de foto apenas como registro demonstrativo do nome escolhido (sem enviar, armazenar imagens reais ou inventar nomes padrão).
4. **Menu com `match/case`:**
   * A equipe implementou a sintaxe moderna do Python 3.10+, substituindo cadeias longas de `if/elif` no roteamento das opções principais do sistema e na tabela de categorias.

---

## 4. Verificação, Testes e Validação dos Resultados

* **Teste de Matriz de Prioridades (8 casos):** Verificamos que entulho e poda com risco elétrico resultam em nível 5; bueiro sem risco elétrico mantém nível 5; buraco mantém nível 4; fios soltos sem risco elétrico mantêm nível 3; entulho passando de 9 para 10 apoios sobe de 2 para 3 e permanece em 3 com 11 apoios; e ocorrências `RESOLVIDO` têm apoio bloqueado.
* **Teste de Entrada Inválida:** Inserção de letras em menus numéricos e respostas vazias/inválidas na pergunta de risco elétrico (`ler_confirmacao_sim_nao()`). O sistema tratou `ValueError` e repetiu a solicitação até entrada válida.
* **Teste de Integridade do JSON:** O arquivo `ocorrencias_zelasp.json` foi testado com tratamento em `try/except json.JSONDecodeError`, mantendo estabilidade na leitura.
* **Teste de Persistência:** Novos registros e apoios foram gravados e recarregados em UTF-8 no arquivo `ocorrencias_zelasp.json`.

---

## 5. Análise Crítica e Reflexão sobre o Uso da IA

### Benefícios:
* Acelerou a montagem da estrutura repetitiva de validação de dados e escrita de arquivos JSON.
* Ajudou a antecipar cenários de exceção e falhas de usuário (inputs vazios, tipos errados).

### Limitações e Dificuldades:
* **Tendência a soluções genéricas ("AI Slop"):** A IA tende a sugerir soluções padronizadas de e-commerce ou cadastros genéricos em inglês. Foi necessário direcionar ativamente o raciocínio para a realidade dos bairros de São Paulo (risco elétrico da Enel, enchentes, entulho da Subprefeitura).
* **Necessidade de Domínio Próprio:** Nenhuma linha de código gerada foi aceita sem que a equipe compreendesse a sintaxe. Em uma entrevista técnica ou avaliação ao vivo, a IA não estará disponível; portanto, dominar a manipulação de dicionários, listas e arquivos é essencial.

> **Conclusão:** A Inteligência Artificial atuou como um **trampolim técnico**, poupando tempo na escrita de código repetitivo e permitindo que o grupo focasse no que realmente importa: a resolução do problema humano e a segurança do cidadão de São Paulo.

