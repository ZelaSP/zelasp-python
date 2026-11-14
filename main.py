"""
========================================================================================
ZelaSP — Sistema Integrado de Zeladoria Urbana Inteligente (Protótipo CLI Acadêmico)
Disciplina: Computational Thinking with Python
Tema: Global Solution 2026.2 · CitizenTech
Integrantes:
- Gustavo Rezende Louro (RM570708)
- João Pedro Lagonegro Bosco e Silva (RM569444)
- João Pedro Maschion da Cruz Sá (RM570509)
- Lucas Henrique Alves da Silva (RM572216)
========================================================================================
Aplicação responsável por registrar relatos urbanos simulados em terminal (cabos rompidos,
bueiros, buracos, poda, entulho e carros abandonados), validar entradas, calcular escores
de prioridade conforme política acadêmica interna, permitir apoio comunitário sem
duplicar chamados abertos e persistir os dados localmente em arquivo JSON.
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
    """Gera base inicial demonstrativa alinhada à política única de prioridade."""
    return [
        {
            "protocolo": "SP-2026-101",
            "categoria": "Fios e Cabos Rompidos/Soltos",
            "bairro": "Jabaquara",
            "endereco": "Av. Eng. Armando de Arruda Pereira, 1200",
            "descricao": "Caminhão baú atingiu a fiação aérea. Cabos caídos na calçada próximos ao acesso da estação de metrô.",
            "risco_choque": True,
            "nivel_prioridade": 5,
            "status": "EM_EXECUCAO",
            "apoios_comunitarios": 12,
            "data_registro": "04/11/2026 08:30",
            "foto_demonstracao": ""
        },
        {
            "protocolo": "SP-2026-102",
            "categoria": "Poda de Árvore com Risco Elétrico",
            "bairro": "Vila Mariana",
            "endereco": "Rua Domingos de Morais, 2180",
            "descricao": "Galho de grande porte curvado e pressionando cabos de média tensão perto do colégio.",
            "risco_choque": True,
            "nivel_prioridade": 5,
            "status": "EM_VISTORIA",
            "apoios_comunitarios": 8,
            "data_registro": "04/11/2026 10:15",
            "foto_demonstracao": ""
        },
        {
            "protocolo": "SP-2026-103",
            "categoria": "Buraco em Via ou Calçada",
            "bairro": "Saúde",
            "endereco": "Av. Bosque da Saúde, 420",
            "descricao": "Cratera aberta na pista da direita após infiltração de chuva, gerando risco de queda para motociclistas.",
            "risco_choque": False,
            "nivel_prioridade": 4,
            "status": "ABERTO",
            "apoios_comunitarios": 5,
            "data_registro": "04/11/2026 14:00",
            "foto_demonstracao": ""
        },
        {
            "protocolo": "SP-2026-104",
            "categoria": "Tampa de Bueiro Furtada/Quebrada",
            "bairro": "Bela Vista",
            "endereco": "Rua Treze de Maio, 850",
            "descricao": "Boca de lobo aberta sem grade protetora na calçada, risco iminente de acidente com pedestres.",
            "risco_choque": False,
            "nivel_prioridade": 5,
            "status": "ABERTO",
            "apoios_comunitarios": 7,
            "data_registro": "05/11/2026 09:20",
            "foto_demonstracao": ""
        },
        {
            "protocolo": "SP-2026-105",
            "categoria": "Descarte Irregular de Entulho",
            "bairro": "Mooca",
            "endereco": "Rua da Mooca, 1120",
            "descricao": "Despejo clandestino de restos de obra e móveis descartados obstruindo completamente a passagem de pedestres.",
            "risco_choque": False,
            "nivel_prioridade": 2,
            "status": "ABERTO",
            "apoios_comunitarios": 4,
            "data_registro": "05/11/2026 11:45",
            "foto_demonstracao": ""
        },
        {
            "protocolo": "SP-2026-106",
            "categoria": "Fios e Cabos Rompidos/Soltos",
            "bairro": "Vila Mascote",
            "endereco": "Av. Mascote, 630",
            "descricao": "Chicote de fiação de telecomunicação rompido e pendurado até a altura do rosto de pedestres.",
            "risco_choque": False,
            "nivel_prioridade": 3,
            "status": "RESOLVIDO",
            "apoios_comunitarios": 6,
            "data_registro": "05/11/2026 16:10",
            "foto_demonstracao": ""
        }
    ]


# ======================================================================================
# LÓGICA DE NEGÓCIO E CLASSIFICAÇÃO DE RISCO (POLÍTICA INTERNA ACADÊMICA)
# ======================================================================================
def classificar_faixa_atendimento(nivel_prioridade):
    """
    Exibe uma faixa de prazo meramente exemplificativa (cenário acadêmico) com base
    no nível de prioridade (1 a 5), sem representar compromisso oficial de SLA.
    """
    if nivel_prioridade == 5:
        return "EMERGÊNCIA (exemplo acadêmico: atendimento imediato em até 2 horas)"
    elif nivel_prioridade == 4:
        return "PRIORIDADE ALTA (exemplo acadêmico: vistoria prioritária em até 12 horas)"
    elif nivel_prioridade == 3:
        return "MÉDIO (exemplo acadêmico: programação regular em até 48 horas)"
    elif nivel_prioridade == 2:
        return "BAIXO (exemplo acadêmico: rota preventiva em até 5 dias úteis)"
    else:
        return "MONITORAMENTO (exemplo acadêmico: planejamento operacional)"


def calcular_score_prioridade(categoria, risco_eletrico, apoios=1):
    """
    Política interna acadêmica de triagem (escala 1 a 5 — não é classificação oficial):
    1. Risco elétrico marcado resulta em nível 5 em todas as categorias.
    2. Sem risco elétrico marcado, aplica a prioridade-base da categoria.
    3. A partir de 10 apoios comunitários, acrescenta um único nível à base (teto 5).
    """
    if risco_eletrico:
        return 5

    match categoria:
        case "Tampa de Bueiro Furtada/Quebrada":
            base = 5
        case "Buraco em Via ou Calçada":
            base = 4
        case "Fios e Cabos Rompidos/Soltos" | "Poda de Árvore com Risco Elétrico":
            base = 3
        case "Descarte Irregular de Entulho":
            base = 2
        case "Carro Abandonado":
            base = 1
        case _:
            base = 2

    if apoios >= 10:
        return min(base + 1, 5)

    return base


# ======================================================================================
# FLUXOS DE INTERAÇÃO DO USUÁRIO (VALIDAÇÃO E CAPTURA DE ENTRADAS)
# ======================================================================================
def ler_confirmacao_sim_nao(mensagem):
    """Valida respostas de risco aceitando apenas s, sim, n, não ou nao."""
    while True:
        resposta = input(mensagem).strip().lower()
        if resposta in ("s", "sim"):
            return True
        if resposta in ("n", "não", "nao"):
            return False
        print("[!] Resposta inválida. Digite apenas 's', 'sim', 'n' ou 'não'.")


def obter_opcao_menu():
    """Exibe o menu de opções principal e valida a escolha via match/case"""
    print("\n" + "=" * 65)
    print("           🏙️  ZelaSP — PAINEL DE ZELADORIA URBANA")
    print("=" * 65)
    print("  [1] Registrar Novo Relato Urbano (endereço manual e foto demo)")
    print("  [2] Consultar e Filtrar Ocorrências por Bairro ou Categoria")
    print("  [3] Apoiar Demanda Existente (Apoio Manual / Sem Duplicar)")
    print("  [4] Atualizar Status de Atendimento (Vistoria / Execução / Conclusão)")
    print("  [5] Relatório Executivo de Chamados de Risco Alto/Crítico")
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

    # 4. Detalhes de Segurança e Seleção Demonstrativa de Foto
    risco_eletrico = ler_confirmacao_sim_nao(
        "Há fios caídos, faíscas ou poça d'água próxima? (s/sim/n/não): "
    )

    descricao = input("Descrição adicional do problema: ").strip()
    if not descricao:
        descricao = "Relato cidadão registrado sem observações complementares."

    print("\n[Foto do local — demonstração]")
    print("Obs.: O envio da imagem e a localização pela foto estão previstos para uma próxima versão.")
    foto = input("Nome do arquivo de foto para demonstração (opcional, Enter para omitir): ").strip()

    # Geração de protocolo único sequencial
    maior_num = 100
    for item in lista_ocorrencias:
        partes = str(item.get("protocolo", "")).split("-")
        if partes and partes[-1].isdigit():
            maior_num = max(maior_num, int(partes[-1]))
    protocolo_gerado = f"SP-2026-{maior_num + 1}"

    # Cálculo automatizado de prioridade (política interna acadêmica)
    nivel_prioridade = calcular_score_prioridade(categoria_selecionada, risco_eletrico, apoios=1)

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
        "foto_demonstracao": foto
    }

    lista_ocorrencias.append(nova_ocorrencia)
    rotulo_nivel = (
        "URGÊNCIA MÁXIMA"
        if nivel_prioridade == 5
        else ("PRIORIDADE ALTA" if nivel_prioridade == 4 else "Zeladoria Regular")
    )
    print("\n" + "=" * 60)
    print("✅ Ocorrência registrada com sucesso!")
    print(f"Protocolo Gerado:   {protocolo_gerado}")
    print(f"Nível de Prioridade: {nivel_prioridade}/5 ({rotulo_nivel})")
    if foto:
        print(f"Arquivo selecionado para demonstração: {foto}")
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
        foto_demo = oc.get("foto_demonstracao") or ""
        if foto_demo:
            print(f"Foto:      Arquivo selecionado para demonstração: {foto_demo}")
        print("-" * 80)


def aplicar_apoio_ocorrencia(oc):
    """
    Incrementa o contador comunitário e recalcula a prioridade a partir da base.
    Ocorrências com status RESOLVIDO não recebem novos apoios.
    """
    if oc.get("status") == "RESOLVIDO":
        return False

    oc["apoios_comunitarios"] = oc.get("apoios_comunitarios", 0) + 1
    oc["nivel_prioridade"] = calcular_score_prioridade(
        oc["categoria"],
        oc.get("risco_choque", False),
        oc["apoios_comunitarios"],
    )
    return True


def apoiar_ocorrencia_existente(lista_ocorrencias):
    """
    Apoio manual a ocorrências existentes para incentivar a redução de relatos repetidos.
    """
    protocolo_alvo = input("\nDigite o número do protocolo que deseja apoiar (ex: SP-2026-101): ").strip().upper()

    for oc in lista_ocorrencias:
        if oc["protocolo"] == protocolo_alvo:
            if not aplicar_apoio_ocorrencia(oc):
                print(
                    f"\n[!] Apoio bloqueado: o protocolo {protocolo_alvo} já está RESOLVIDO. "
                    f"Contador preservado em {oc['apoios_comunitarios']} apoio(s)."
                )
                return False

            print(f"\n🤝 Apoio registrado com sucesso para o protocolo {protocolo_alvo}!")
            print(f"Total de apoios comunitários: {oc['apoios_comunitarios']}.")
            print(f"Prioridade recalculada:      Nível {oc['nivel_prioridade']}/5.")
            return True

    print(f"\n[!] Protocolo '{protocolo_alvo}' não localizado na base.")
    return False


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
    print("      📊 RELATÓRIO DE CHAMADOS DE RISCO ALTO/CRÍTICO (ACADÊMICO)")
    print("=" * 65)
    print(f"Total de ocorrências cadastradas:       {len(lista_ocorrencias)}")
    print(f"Chamados de risco alto/crítico abertos: {len(criticos)}")
    print("Nota: prazos abaixo são exemplos acadêmicos e não configuram SLA oficial.")
    print("-" * 65)

    if criticos:
        print("LISTA DE INTERVENÇÃO PRIORITÁRIA (NÍVEIS 4 E 5):")
        for c in sorted(
            criticos,
            key=lambda x: (x["nivel_prioridade"], x.get("apoios_comunitarios", 0)),
            reverse=True,
        ):
            prazo = classificar_faixa_atendimento(c["nivel_prioridade"])
            print(f"-> [{c['protocolo']}] Nível {c['nivel_prioridade']}/5 — {prazo}")
            print(
                f"   Local: {c['bairro']} — {c['categoria']} ({c['endereco']}) "
                f"| Apoios: {c.get('apoios_comunitarios', 0)}"
            )
    else:
        print("Nenhum chamado de risco alto/crítico pendente no momento.")


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
