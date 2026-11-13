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
* **Problema em uma Frase:** O canal oficial atual (SP 156) é burocrático, demorado e opaco, desestimulando o cidadão a relatar incidentes urbanos graves e impedindo a vizinhança de acompanhar e apoiar chamados do mesmo quarteirão.
* **Como Funciona:** O cidadão registra uma ocorrência em menos de 15 segundos enviando foto e localização automática; a plataforma exibe relatos abertos no mesmo raio (permitindo apoiar chamados existentes em vez de duplicá-los); e disponibiliza uma linha do tempo transparente com fotos antes/depois da execução do serviço.
* **O que Cada Parte Faz:**
  * **Lógica (Computational Thinking with Python):** Sistema de triagem, cálculo de risco/urgência (cabo elétrico vs. entulho) e persistência em arquivos JSON.
  * **Interface & Interação (Front-end Design & Web Development):** WebApp mobile-first em React + Tailwind CSS com consumo de API (CRUD completo), 8 componentes e Custom Hooks.
  * **Sensor (Edge Computing & Computer Systems):** Dispositivo embarcado com ESP32 simulado no Wokwi para monitorar vibração e integridade mecânica de cabos em postes, emitindo alerta sonoro/visual local.
  * **Matemática (Differentiated Problem Solving):** Modelagem diferencial da taxa de chegada de incidentes pós-tempestade versus capacidade de resposta da equipe de zeladoria.
  * **Experiência (Software & Total Experience Design):** Slide deck com requisitos funcionais, não funcionais, regras de negócio justificadas, casos de uso e heurísticas de usabilidade.
  * **Pitch (Storytelling & Inspiração Empreendedora):** Videopitch de 3 minutos em 9 etapas e e-mail executivo fundamentando o arquétipo de marca (O Cuidador / O Cidadão).
* **Indicador de Impacto:** Redução do tempo médio de relato de 5–8 minutos (estimado no SP 156 tradicional) para **menos de 15 segundos**, com **meta de −45% de chamados duplicados** e **redução simulada de 38,5% no backlog acumulado** (integrada à modelagem DPS).
* **ODS Conectados:** ODS 11 (Cidades e Comunidades Sustentáveis) e ODS 9 (Indústria, Inovação e Infraestrutura).

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
| **Validação de Entradas** | Loops `while` e verificações em `registrar_nova_ocorrencia()` e `atualizar_status_ocorrencia()`. |
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

