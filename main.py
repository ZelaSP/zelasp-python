"""
========================================================================================
ZelaSP — Sistema Integrado de Zeladoria Urbana Inteligente
Disciplina: Computational Thinking with Python
Tema: Global Solution 2026.2 · CitizenTech
Integrantes:
- Gustavo Rezende Louro (RM570708)
- João Pedro Lagonegro Bosco e Silva (RM569444)
- João Pedro Maschion da Cruz Sá (RM570509)
- Lucas Henrique Alves da Silva (RM572216)
========================================================================================
Aplicação responsável por processar relatos urbanos (cabos rompidos, buracos, entulho,
carros abandonados), realizar validações, calcular escores de urgência/risco, agrupar
demandas comunitárias no mesmo quarteirão e persistir os dados em formato JSON.
========================================================================================
"""

import os
import json
from datetime import datetime

# ======================================================================================
# CONSTANTES E CONFIGURAÇÕES GLOBAIS
# ======================================================================================
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BD_JSON = os.path.join(DIRETORIO_ATUAL, "ocorrencias_zelasp.json")

# Tuplas imutáveis para categorias e bairros atendidos pelo piloto em São Paulo
CATEGORIAS_VALIDAS = (
    "Fios e Cabos Rompidos/Soltos",
    "Descarte Irregular de Entulho",
    "Buraco em Via ou Calçada",
    "Carro Abandonado",
    "Tampa de Bueiro Furtada/Quebrada",
    "Poda de Árvore com Risco Elétrico"
)

BAIRROS_SP = (
    "Jabaquara", "Vila Mariana", "Saúde", "Bela Vista", "Mooca", "Vila Mascote",
    "Pinheiros", "Sé", "Lapa", "Itaquera", "Santo Amaro", "Tatuapé"
)

STATUS_POSSIVEIS = ("ABERTO", "EM_VISTORIA", "EM_EXECUCAO", "RESOLVIDO")


# ======================================================================================
# PERSISTÊNCIA EM ARQUIVOS JSON (LEITURA E GRAVAÇÃO COM TRATAMENTO DE EXCEÇÃO)
# ======================================================================================
def carregar_ocorrencias(caminho_arquivo):
    """
    Lê a base de dados em arquivo JSON utilizando bloco try/except defensivo.
    Se o arquivo não existir ou estiver vazio, inicializa com base padrão de exemplos.
    """
    if not os.path.exists(caminho_arquivo):
        dados_iniciais = criar_dados_exemplo()
        salvar_ocorrencias(caminho_arquivo, dados_iniciais)
        return dados_iniciais

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return dados
    except json.JSONDecodeError:
        print("\n[AVISO] Arquivo JSON corrompido ou vazio. Inicializando nova base limpa...")
        return []
    except IOError as erro:
        print(f"\n[ERRO DE E/S] Não foi possível ler o arquivo: {erro}")
        return []


def salvar_ocorrencias(caminho_arquivo, lista_ocorrencias):
    """
    Grava a lista de ocorrências no arquivo JSON formatado com indentação e codificação UTF-8.
    """
    try:
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(lista_ocorrencias, f, indent=4, ensure_ascii=False)
        return True
    except IOError as erro:
        print(f"\n[ERRO CRÍTICO] Falha ao gravar dados no arquivo JSON: {erro}")
        return False


def criar_dados_exemplo():
    """Gera dados iniciais com cenários reais de São Paulo para testes da aplicação"""
    return [
        {
            "protocolo": "SP-2026-101",
            "categoria": "Fios e Cabos Rompidos/Soltos",
            "bairro": "Pinheiros",
            "endereco": "Rua dos Pinheiros, 450",
            "descricao": "Caminhão de carga arrancou cabos da rede. Fiação solta rente ao chão na calçada.",
            "risco_choque": True,
            "nivel_prioridade": 5,
            "status": "EM_EXECUCAO",
            "apoios_comunitarios": 4,
            "data_registro": "04/11/2026 09:15",
            "foto_evidencia": "evidencia_pinheiros_450.jpg"
        },
        {
            "protocolo": "SP-2026-102",
            "categoria": "Descarte Irregular de Entulho",
            "bairro": "Mooca",
            "endereco": "Rua da Mooca, 1120",
            "descricao": "Despejo de sofás velhos e sacos de entulho na calçada em frente a terreno baldio.",
            "risco_choque": False,
            "nivel_prioridade": 2,
            "status": "ABERTO",
            "apoios_comunitarios": 2,
            "data_registro": "04/11/2026 11:30",
            "foto_evidencia": "evidencia_mooca_1120.jpg"
        },
        {
            "protocolo": "SP-2026-103",
            "categoria": "Buraco em Via ou Calçada",
            "bairro": "Sé",
            "endereco": "Rua Boa Vista, 85",
            "descricao": "Cratera na faixa de ônibus causando freadas bruscas de coletivos.",
            "risco_choque": False,
            "nivel_prioridade": 4,
            "status": "EM_VISTORIA",
            "apoios_comunitarios": 7,
            "data_registro": "04/11/2026 14:00",
            "foto_evidencia": "evidencia_se_85.jpg"
        }
    ]


# ======================================================================================
# LÓGICA DE NEGÓCIO E CLASSIFICAÇÃO DE RISCO (ESTRUTURAS DE DECISÃO)
# ======================================================================================
def classificar_faixa_atendimento(nivel_prioridade):
    """
    Classifica o prazo de atendimento emergencial municipal com base na prioridade (1 a 5).
    Demonstração obrigatória do encadeamento condicional if / elif / else conforme edital FIAP.
    """
    if nivel_prioridade == 5:
        return "EMERGÊNCIA — Intervenção Imediata (até 2 horas)"
    elif nivel_prioridade == 4:
        return "URGENTE — Vistoria Prioritária (até 12 horas)"
    elif nivel_prioridade == 3:
        return "MÉDIO — Programação Regular (até 48 horas)"
    elif nivel_prioridade == 2:
        return "BAIXO — Rota Preventiva (até 5 dias úteis)"
    else:
        return "MONITORAMENTO — Planejamento Operacional"


def calcular_score_prioridade(categoria, risco_eletrico, via_movimentada):
    """
    Calcula a prioridade operacional (escala 1 a 5) com base em regras de segurança urbana.
    Usa match/case para classificar a severidade da tipologia.
    """
    match categoria:
        case "Fios e Cabos Rompidos/Soltos" | "Tampa de Bueiro Furtada/Quebrada":
            base = 4
        case "Buraco em Via ou Calçada" | "Poda de Árvore com Risco Elétrico":
            base = 3
        case "Descarte Irregular de Entulho":
            base = 2
        case "Carro Abandonado":
            base = 1
        case _:
            base = 2

    # Agravantes de risco à vida humana
    if risco_eletrico:
        base += 1  # Eleva imediatamente para nível crítico
    if via_movimentada and base < 5:
        base += 1

    return min(base, 5)  # Limita ao teto máximo de 5


# ======================================================================================
# FLUXOS DE INTERAÇÃO DO USUÁRIO (VALIDAÇÃO E CAPTURA DE ENTRADAS)
# ======================================================================================
def obter_opcao_menu():
    """Exibe o menu de opções principal e valida a escolha via match/case"""
    print("\n" + "=" * 65)
    print("           🏙️  ZelaSP — PAINEL DE ZELADORIA URBANA")
    print("=" * 65)
    print("  [1] Registrar Novo Relato Urbano (com foto e geolocalização)")
    print("  [2] Consultar e Filtrar Ocorrências por Bairro ou Categoria")
    print("  [3] Apoiar Demanda Existente (Consciência Comunitária / Sem Duplicidade)")
    print("  [4] Atualizar Status de Atendimento (Vistoria / Execução / Conclusão)")
    print("  [5] Relatório Executivo de Prioridades Críticas")
    print("  [0] Encerrar Sessão")
    print("-" * 65)
    
    opcao = input("Selecione uma opção (0 a 5): ").strip()
    return opcao


def registrar_nova_ocorrencia(lista_ocorrencias):
    """
    Fluxo de entrada com validações rigorosas de dados para evitar lixo no banco de dados.
    """
    print("\n" + "-" * 60)
    print("         REGISTRO RÁPIDO DE OCORRÊNCIA CIDADÃ")
    print("-" * 60)

    # 1. Seleção de Categoria
    print("\nCategorias disponíveis:")
    for idx, cat in enumerate(CATEGORIAS_VALIDAS, 1):
        print(f"  [{idx}] {cat}")
    
    while True:
        try:
            escolha_cat = int(input("\nDigite o número da categoria correspondente: ").strip())
            if 1 <= escolha_cat <= len(CATEGORIAS_VALIDAS):
                categoria_selecionada = CATEGORIAS_VALIDAS[escolha_cat - 1]
                break
            else:
                print(f"[!] Opção inválida. Digite um número entre 1 e {len(CATEGORIAS_VALIDAS)}.")
        except ValueError:
            print("[!] Entrada incorreta. Digite apenas o valor numérico.")

    # 2. Seleção de Bairro de São Paulo
    print("\nBairros atendidos no projeto:")
    for idx, b in enumerate(BAIRROS_SP, 1):
        print(f"  [{idx}] {b}")

    while True:
        try:
            escolha_bairro = int(input("\nDigite o número do bairro da ocorrência: ").strip())
            if 1 <= escolha_bairro <= len(BAIRROS_SP):
                bairro_selecionado = BAIRROS_SP[escolha_bairro - 1]
                break
            else:
                print(f"[!] Opção inválida. Escolha entre 1 e {len(BAIRROS_SP)}.")
        except ValueError:
            print("[!] Digite apenas o número correspondente ao bairro.")

    # 3. Endereço e Logradouro
    while True:
        endereco = input("\nInforme o endereço completo (Rua, Número ou Referência): ").strip()
        if len(endereco) >= 5:
            break
        print("[!] Endereço muito curto. Seja mais específico para orientar a equipe.")

    # 4. Detalhes de Segurança
    resposta_eletrica = input("Há fios caídos, faíscas ou poça d'água próxima? (s/n): ").strip().lower()
    risco_eletrico = (resposta_eletrica == "s" or resposta_eletrica == "sim")

    resposta_via = input("É uma avenida principal ou via de grande circulação? (s/n): ").strip().lower()
    via_movimentada = (resposta_via == "s" or resposta_via == "sim")

    descricao = input("Descrição adicional do problema: ").strip()
    if not descricao:
        descricao = "Relato cidadão registrado sem observações complementares."

    foto = input("Nome do arquivo de foto anexado (ex: cabo_quebrado.jpg): ").strip()
    if not foto:
        foto = "foto_padrao_evidencia.jpg"

    # Geração de protocolo único sequencial
    proximo_id = len(lista_ocorrencias) + 101
    protocolo_gerado = f"SP-2026-{proximo_id}"

    # Cálculo automatizado de prioridade
    nivel_prioridade = calcular_score_prioridade(categoria_selecionada, risco_eletrico, via_movimentada)

    nova_ocorrencia = {
        "protocolo": protocolo_gerado,
        "categoria": categoria_selecionada,
        "bairro": bairro_selecionado,
        "endereco": endereco,
        "descricao": descricao,
        "risco_choque": risco_eletrico,
        "nivel_prioridade": nivel_prioridade,
        "status": "ABERTO",
        "apoios_comunitarios": 1,
        "data_registro": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "foto_evidencia": foto
    }

    lista_ocorrencias.append(nova_ocorrencia)
    print("\n" + "=" * 60)
    print(f"✅ Ocorrência registrada com sucesso!")
    print(f"Protocolo Gerado:   {protocolo_gerado}")
    print(f"Nível de Prioridade: {nivel_prioridade}/5 ({'RISCO CRÍTICO' if nivel_prioridade == 5 else 'Acompanhamento Normal'})")
    print("=" * 60)
    return True


def listar_e_filtrar_ocorrencias(lista_ocorrencias):
    """
    Exibe a lista de chamados permitindo filtros por bairro ou exibição geral.
    """
    if not lista_ocorrencias:
        print("\n[INFO] Nenhuma ocorrência cadastrada no sistema.")
        return

    print("\n--- FILTROS DE CONSULTA ---")
    print("[1] Ver todas as ocorrências")
    print("[2] Filtrar por Bairro específico")
    print("[3] Filtrar por Categoria")
    opcao_filtro = input("Escolha uma opção de visualização: ").strip()

    resultado = lista_ocorrencias

    match opcao_filtro:
        case "2":
            bairro_busca = input("Digite o nome do bairro desejado: ").strip().lower()
            resultado = [item for item in lista_ocorrencias if item["bairro"].lower() == bairro_busca]
        case "3":
            termo = input("Digite a palavra-chave da categoria: ").strip().lower()
            resultado = [item for item in lista_ocorrencias if termo in item["categoria"].lower()]
        case _:
            pass

    if not resultado:
        print("\n[!] Nenhum registro encontrado para o filtro aplicado.")
        return

    print(f"\nExibindo {len(resultado)} ocorrência(s):")
    print("-" * 80)
    for oc in resultado:
        alerta_eletrico = " ⚡ [PERIGO DE CHOQUE]" if oc.get("risco_choque") else ""
        print(f"Protocolo: {oc['protocolo']} | Status: {oc['status']} | Apoios: {oc['apoios_comunitarios']}")
        print(f"Categoria: {oc['categoria']}{alerta_eletrico}")
        print(f"Local:     {oc['endereco']} — {oc['bairro']}")
        print(f"Urgência:  Nível {oc['nivel_prioridade']}/5 | Data: {oc['data_registro']}")
        print("-" * 80)


def apoiar_ocorrencia_existente(lista_ocorrencias):
    """
    Consciência comunitária do ZelaSP: o munícipe vê um chamado da mesma rua
    e manifesta apoio ao invés de duplicar registros idênticos.
    """
    protocolo_alvo = input("\nDigite o número do protocolo que deseja apoiar (ex: SP-2026-101): ").strip().upper()
    
    encontrado = False
    for oc in lista_ocorrencias:
        if oc["protocolo"] == protocolo_alvo:
            oc["apoios_comunitarios"] += 1
            encontrado = True
            print(f"\n🤝 Apoio registrado com sucesso para o protocolo {protocolo_alvo}!")
            print(f"Total de moradores que endossam essa resolução: {oc['apoios_comunitarios']}.")
            break

    if not encontrado:
        print(f"\n[!] Protocolo '{protocolo_alvo}' não localizado na base.")


def atualizar_status_ocorrencia(lista_ocorrencias):
    """
    Permite à equipe de zeladoria ou subprefeitura atualizar a evolução do serviço.
    """
    protocolo_alvo = input("\nDigite o protocolo a ser atualizado (ex: SP-2026-101): ").strip().upper()

    for oc in lista_ocorrencias:
        if oc["protocolo"] == protocolo_alvo:
            print(f"\nStatus atual da ocorrência: {oc['status']}")
            print("Novos status disponíveis:")
            for idx, st in enumerate(STATUS_POSSIVEIS, 1):
                print(f"  [{idx}] {st}")

            try:
                escolha = int(input("Selecione o novo status (1 a 4): ").strip())
                if 1 <= escolha <= len(STATUS_POSSIVEIS):
                    novo_status = STATUS_POSSIVEIS[escolha - 1]
                    oc["status"] = novo_status
                    print(f"✅ Status do protocolo {protocolo_alvo} atualizado para '{novo_status}'!")
                    return
                else:
                    print("[!] Opção fora do intervalo válido.")
            except ValueError:
                print("[!] Valor inválido. Ação cancelada.")
            return

    print(f"\n[!] Protocolo '{protocolo_alvo}' não encontrado.")


def emitir_relatorio_prioridades(lista_ocorrencias):
    """
    Gera estatísticas e ranking das ocorrências mais críticas (Risco 4 e 5).
    """
    if not lista_ocorrencias:
        print("\nBase de dados vazia.")
        return

    criticos = [item for item in lista_ocorrencias if item["nivel_prioridade"] >= 4 and item["status"] != "RESOLVIDO"]
    
    print("\n" + "=" * 65)
    print("      📊 RELATÓRIO MUNICIPAL DE ATENDIMENTO PRIORITÁRIO")
    print("=" * 65)
    print(f"Total de ocorrências cadastradas: {len(lista_ocorrencias)}")
    print(f"Incidentes Críticos em Aberto:    {len(criticos)}")
    print("-" * 65)

    if criticos:
        print("LISTA DE INTERVENÇÃO IMEDIATA (CABOS E RISCOS FÍSICOS):")
        for c in sorted(criticos, key=lambda x: x["nivel_prioridade"], reverse=True):
            prazo = classificar_faixa_atendimento(c["nivel_prioridade"])
            print(f"-> [{c['protocolo']}] Risco {c['nivel_prioridade']}/5 — {prazo}")
            print(f"   Local: {c['bairro']} — {c['categoria']} ({c['endereco']})")
    else:
        print("Nenhum chamado crítico pendente no momento. Malha urbana em conformidade.")


# ======================================================================================
# LAÇO PRINCIPAL DE EXECUÇÃO (MAIN LOOP)
# ======================================================================================
def main():
    """Ponto de entrada da aplicação Python ZelaSP"""
    print("\nInicializando sistema ZelaSP (Carregando dados JSON)...")
    base_ocorrencias = carregar_ocorrencias(CAMINHO_BD_JSON)
    print(f"Base carregada: {len(base_ocorrencias)} registros ativos.")

    executando = True
    while executando:
        opcao = obter_opcao_menu()

        match opcao:
            case "1":
                registrar_nova_ocorrencia(base_ocorrencias)
                salvar_ocorrencias(CAMINHO_BD_JSON, base_ocorrencias)
            case "2":
                listar_e_filtrar_ocorrencias(base_ocorrencias)
            case "3":
                apoiar_ocorrencia_existente(base_ocorrencias)
                salvar_ocorrencias(CAMINHO_BD_JSON, base_ocorrencias)
            case "4":
                atualizar_status_ocorrencia(base_ocorrencias)
                salvar_ocorrencias(CAMINHO_BD_JSON, base_ocorrencias)
            case "5":
                emitir_relatorio_prioridades(base_ocorrencias)
            case "0":
                print("\nEncerrando sessão no ZelaSP. Dados persistidos com segurança no arquivo JSON.")
                print("Obrigado por contribuir com a zeladoria de São Paulo!")
                executando = False
            case _:
                print("\n[!] Opção desconhecida. Por favor, escolha um item do menu entre 0 e 5.")


if __name__ == "__main__":
    main()
