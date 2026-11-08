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
> *"Crie uma lógica de classificação de severidade de risco urbano de 1 a 5, onde cabos elétricos com risco de choque e bueiros abertos recebam prioridade 4 ou 5 automaticamente, e incidentes como entulho ou veículos abandonados fiquem entre 1 e 3."*

---

## 3. Funcionalidades Desenvolvidas e Modificadas pelo Grupo

1. **Persistência em JSON (`carregar_ocorrencias` e `salvar_ocorrencias`):**
   * *Sugestão da IA:* A IA sugeriu gravar os dados imediatamente após cada operação de adição ou edição.
   * *Ajuste do Grupo:* O grupo adicionou a verificação prévia com `os.path.exists()` e um gerador de dados padrão (`criar_dados_exemplo()`), garantindo que se o professor rodar o script sem nenhum arquivo na pasta, a aplicação inicializa dados reais de São Paulo sem crashar.
2. **Sistema de Apoio Comunitário (Sem Duplicidade):**
   * *Desenvolvimento da Equipe:* Implementamos a função `apoiar_ocorrencia_existente()`. A IA sugeriu apenas criar e listar chamados. O grupo percebeu que no problema real do SP156 as pessoas criam dezenas de chamados para o mesmo buraco ou fio caído, por isso transformamos o sistema para permitir "apoiar" a demanda já existente.
3. **Menu com `match/case`:**
   * A equipe implementou a sintaxe moderna do Python 3.10+, substituindo cadeias longas de `if/elif` no roteamento das opções principais do sistema.

---

## 4. Verificação, Testes e Validação dos Resultados

* **Teste de Entrada Inválida:** Inserção de letras em menus numéricos e números negativos em faixas de 1 a 5. O sistema tratou com `ValueError` e repetiu a solicitação sem interromper a execução.
* **Teste de Integridade do JSON:** O arquivo `ocorrencias_zelasp.json` foi editado com caracteres corrompidos. O bloco `try/except json.JSONDecodeError` detectou a inconsistência, exibiu um aviso e manteve o sistema estável.
* **Teste de Persistência:** Cadastramos um novo chamado de fio arrebentado na Rua da Consolação, encerramos a aplicação (`Opção 0`) e reabrimos o `main.py`. O registro foi recarregado perfeitamente com todos os campos salvos em UTF-8.

---

## 5. Análise Crítica e Reflexão sobre o Uso da IA

### Benefícios:
* Acelerou a montagem da estrutura repetitiva de validação de dados e escrita de arquivos JSON.
* Ajudou a antecipar cenários de exceção e falhas de usuário (inputs vazios, tipos errados).

### Limitações e Dificuldades:
* **Tendência a soluções genéricas ("AI Slop"):** A IA tende a sugerir soluções padronizadas de e-commerce ou cadastros genéricos em inglês. Foi necessário direcionar ativamente o raciocínio para a realidade dos bairros de São Paulo (risco elétrico da Enel, enchentes, entulho da Subprefeitura).
* **Necessidade de Domínio Próprio:** Nenhuma linha de código gerada foi aceita sem que a equipe compreendesse a sintaxe. Em uma entrevista técnica ou avaliação ao vivo, a IA não estará disponível; portanto, dominar a manipulação de dicionários, listas e arquivos é essencial.

> **Conclusão:** A Inteligência Artificial atuou como um **trampolim técnico**, poupando tempo na escrita de código repetitivo e permitindo que o grupo focasse no que realmente importa: a resolução do problema humano e a segurança do cidadão de São Paulo.

