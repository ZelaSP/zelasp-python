# 🏙️ ZelaSP — Sistema Integrado de Zeladoria Urbana

> **Global Solution 2026.2 · FIAP**  
> **Disciplina:** Computational Thinking with Python  
> **Tema:** CitizenTech  
> **Integrantes:**
> * Gustavo Rezende Louro — RM570708
> * João Pedro Lagonegro Bosco e Silva — RM569444
> * João Pedro Maschion da Cruz Sá — RM570509
> * Lucas Henrique Alves da Silva — RM572216  

---

## 📋 A Ficha da CitizenTech

* **Nome da CitizenTech:** ZelaSP
* **Cidade e Bairro:** São Paulo — SP (foco prioritário em bairros com histórico de gargalos urbanos e fiação aérea crítica, como Jabaquara, Vila Mariana, Saúde, Bela Vista, Mooca e Vila Mascote).
* **Cidadão Beneficiado:** Moradores, pedestres, comerciantes e pessoas com deficiência ou mobilidade reduzida que enfrentam riscos urbanos diários (cabos rompidos nas calçadas, entulhos obstruindo passagens, buracos em vias e carros abandonados).
* **Problema em uma Frase:** O fluxo tradicional de atendimento urbano é burocrático e pouco transparente para o cidadão, desestimulando relatos preventivos e dificultando o acompanhamento coletivo de incidentes no mesmo quarteirão.
* **Como Funciona:** No módulo Python CLI, o usuário registra relatos de zeladoria em terminal com endereço manual, classificação automática de risco, seleção demonstrativa de foto e persistência local em JSON, além de poder apoiar ocorrências já abertas em vez de criar novos chamados repetidos.
* **Escopo Atual vs. Evolução:**
  * **Arquitetura:** Web com MockAPI e ViaCEP; CLI Python com JSON; estudo matemático independente; integração entre módulos e IoT prevista na evolução.
  * **Tempo de relato:** Meta de registro em até 15 segundos, a validar com testes de usabilidade (comparação cronometrada com o canal oficial prevista como atividade futura).
  * **Duplicidade atual:** Apoio manual a ocorrências existentes para incentivar a redução de relatos repetidos.
  * **Meta de duplicidade:** Meta futura de reduzir em 45% a parcela de chamados duplicados (além de deduplicação automática por proximidade no roadmap).
  * **Resultado matemático:** Redução simulada de 38,5% do excedente sobre a base já deduplicada, após reforço de capacidade, nas hipóteses do exercício.
  * **Foto e localização:** Funcionalidade futura: foto como evidência e apoio à localização da ocorrência; seleção demonstrativa na versão atual.
* **Proposta de Evolução (Imagens e Localização):**
  > A proposta de evolução do ZelaSP inclui o uso de fotografias como evidência e apoio à localização da ocorrência, aproveitando metadados GPS disponíveis no arquivo e a confirmação do cidadão. No protótipo acadêmico atual, a seleção de foto é demonstrativa: o conteúdo da imagem não é enviado, armazenado ou analisado. Na aplicação Web, o endereço é informado por CEP ou digitação, com captura opcional de GPS do navegador; na CLI Python, o endereço é digitado no terminal e o nome do arquivo de foto é apenas registrado de forma demonstrativa.
* **O que Cada Módulo Faz no Ecossistema ZelaSP:**
  * **Lógica (Computational Thinking with Python):** Sistema CLI de triagem acadêmica, cálculo de prioridade (1 a 5), validação de entradas e persistência local em `ocorrencias_zelasp.json`.
  * **Interface & Interação (Front-end Design & Web Development):** WebApp em React + Tailwind CSS com MockAPI, ViaCEP, captura opcional de GPS do navegador e cache local de consulta.
  * **Matemática (Differentiated Problem Solving):** Simulação acadêmica da taxa horária de relatos pós-temporal versus capacidade operacional e mecanismo GPCT.
  * **Sensor (Edge Computing & Computer Systems):** Dispositivo embarcado simulado no Wokwi com ESP32 para monitoramento local de alertas.
  * **Experiência (Software & Total Experience Design):** Documentação de requisitos, casos de uso UML, regras de negócio, heurísticas e roadmap de evolução.
  * **Pitch (Storytelling & Inspiração Empreendedora):** Videopitch de 3 minutos em 9 etapas e comunicação executiva da proposta.
* **ODS Conectados:** ODS 11 (Cidades e Comunidades Sustentáveis) e ODS 9 (Indústria, Inovação e Infraestrutura).

---

## ⚖️ Regra Única de Prioridade (Política Acadêmica Interna)

Os níveis abaixo pertencem à política acadêmica interna de triagem adotada de forma idêntica no Python, no Web e no TX Design. **Não representam classificação oficial da Prefeitura ou da concessionária**, e os prazos exibidos no relatório da CLI são exemplos didáticos.

1. **Risco elétrico marcado:** atribui **nível 5**, independentemente da categoria.
2. **Ausência de risco elétrico marcado:** aplica a prioridade-base da tabela abaixo.
3. **A partir de 10 apoios:** acrescenta **um único nível** à prioridade-base, limitado ao teto 5 (sempre recalculado a partir da base).
4. **Ocorrências com status `RESOLVIDO`:** não recebem novos apoios (contador preservado).

| Categoria | Prioridade-base sem risco elétrico marcado |
| :--- | :---: |
| Tampa de Bueiro Furtada/Quebrada | 5 |
| Buraco em Via ou Calçada | 4 |
| Fios e Cabos Rompidos/Soltos | 3 |
| Poda de Árvore com Risco Elétrico | 3 |
| Descarte Irregular de Entulho | 2 |
| Carro Abandonado | 1 |

---

## 🚀 Como Executar a Aplicação Python

### Pré-requisitos:
* Python 3.10 ou superior instalado (necessário para suporte a `match/case`).
* Não requer instalação de bibliotecas externas via `pip` (utiliza apenas os módulos padrão `os`, `json` e `datetime`).

### Execução:
1. Clone o repositório (ou acesse a pasta raiz):
   ```bash
   git clone https://github.com/ZelaSP/zelasp-python.git
   cd zelasp-python
   ```
2. Execute o arquivo principal:
   ```bash
   python main.py
   # ou no Windows:
   py main.py
   ```

---

## 🛠️ Requisitos Técnicos Atendidos (Tabela de Avaliação FIAP)

| Critério Avaliado | Onde se encontra no código |
| :--- | :--- |
| **Menu de Opções Interativo** | Função `obter_opcao_menu()` e laço `while executando` na função `main()`. |
| **Estruturas de Decisão (`match/case`)** | Roteamento do menu na função `main()` e na classificação de prioridades em `calcular_score_prioridade()`. |
| **Validação de Entradas** | Loops `while` com aceitação estrita de risco (`s/sim/n/não`) em `ler_confirmacao_sim_nao()`, `registrar_nova_ocorrencia()` e `atualizar_status_ocorrencia()`. |
| **Recálculo e Bloqueio em Resolvidos** | Função `aplicar_apoio_ocorrencia()` impede novos apoios em status `RESOLVIDO` e recalcula a prioridade a partir da base. |
| **Tratamento de Exceções (`try/except`)** | Captura de `ValueError`, `IOError`, `json.JSONDecodeError` e proteção em I/O. |
| **Persistência em Arquivo JSON** | Funções `carregar_ocorrencias()` e `salvar_ocorrencias()` manipulando `ocorrencias_zelasp.json`. |
| **Manipulação de Coleções** | Tuplas imutáveis (`CATEGORIAS_VALIDAS`, `BAIRROS_SP`), listas de dicionários e compreensões de lista para filtros. |
| **Boas Práticas e Clean Code** | Código modularizado em funções puras, nomes expressivos em português, docstrings e comentários explicativos. |
| **Documentação Ética de IA** | Arquivo `prompts.md` completo anexado na raiz da pasta. |

---

## 📁 Estrutura desta Entrega

```text
├── main.py                   # Script principal executável
├── ocorrencias_zelasp.json   # Banco de dados de persistência em JSON
├── prompts.md                # Relatório obrigatório de transparência no uso de IA
└── README.md                 # Este documento com a Ficha da CitizenTech e manual
```

