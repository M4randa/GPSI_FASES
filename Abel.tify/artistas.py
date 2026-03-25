# ================================================================
#  FICHEIRO: artistas.py
#  DESCRICAO: Dados, CRUD e menu da entidade Artista
#  AUTOR: Abel Chongolola | GPSI 10A | N 01
# ================================================================

import json
import os
from utils import validar_nome, validar_url, validar_genero, validar_ouvintes, validar_ano, validar_tipo_lancamento, validar_data_concerto
from utilizadores import utilizadores, guardar_utilizadores

# Dicionario principal dos artistas
artistas = {}

# Contador global para IDs unicos (A0001, A0002...)
contador_artista = 1

FICHEIRO_ARTISTAS = "artistas.json"


# ================================================================
#  PERSISTENCIA JSON
# ================================================================

def guardar_artistas():
    dados = {"contador": contador_artista, "artistas": artistas}
    with open(FICHEIRO_ARTISTAS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    print("Dados guardados em " + FICHEIRO_ARTISTAS)


def carregar_artistas():
    global artistas, contador_artista
    if not os.path.exists(FICHEIRO_ARTISTAS):
        print("Nenhum ficheiro encontrado, a comecar do zero.")
        return
    with open(FICHEIRO_ARTISTAS, "r", encoding="utf-8") as f:
        dados = json.load(f)
    contador_artista = dados["contador"]
    artistas         = dados["artistas"]
    print("Artistas carregados: " + str(len(artistas)) + " registo(s).")


# ================================================================
#  CREATE
# ================================================================

def criar_artista():
    global contador_artista

    print("\n-- Criar Artista --")

    # while True em cada campo: repete ate o utilizador acertar
    while True:
        nome = input("Nome do artista: ").strip()
        if not validar_nome(nome):
            print("Erro: Nome invalido. Minimo 2 caracteres.")
            continue
        # Nome tem de ser unico
        repetido = False
        for a in artistas.values():
            if a["nome"].lower() == nome.lower():
                repetido = True
        if repetido:
            print("Erro: Ja existe um artista com esse nome.")
        else:
            break

    while True:
        bio = input("Biografia: ").strip()
        if len(bio) >= 5:
            break
        print("Erro: Biografia demasiado curta. Minimo 5 caracteres.")

    while True:
        imagem = input("URL da imagem de perfil (http://...): ").strip()
        if validar_url(imagem):
            break
        print("Erro: URL invalido. Use http:// ou https://")

    while True:
        imagem_capa = input("URL da imagem de capa (http://...): ").strip()
        if validar_url(imagem_capa):
            break
        print("Erro: URL de capa invalido. Use http:// ou https://")

    while True:
        genero = input("Genero musical: ").strip()
        if validar_genero(genero):
            break
        print("Erro: Genero invalido. Nao pode conter numeros.")

    while True:
        verificado_str = input("Artista verificado? (s/n): ").strip().lower()
        if verificado_str == "s":
            verificado = True
            break
        elif verificado_str == "n":
            verificado = False
            break
        else:
            print("Erro: Resposta invalida. Escreva s ou n.")

    id_artista = "A" + str(contador_artista).zfill(1)
    contador_artista += 1

    artistas[id_artista] = {
        "id_artista":       id_artista,
        "nome":             nome,
        "bio":              bio,
        "imagem":           imagem,
        "imagem_capa":      imagem_capa,
        "genero":           genero,
        "verificado":       verificado,
        "discografia":      [],     # lista de {titulo, tipo, ano}
        "ouvintes_mensais": 0,
        "seguidores":       [],
        "top_faixas":       [],     # max 5 faixas em destaque
        "datas_concertos":  [],
        "escolha_artista":  "",
    }

    print("OK! Artista criado com ID: " + id_artista)
    guardar_artistas()


# ================================================================
#  READ
# ================================================================

def ler_artista():
    print("\n-- Ler Artista --")

    if not artistas:
        print("Aviso: Nenhum artista registado.")
        return

    id_a = input("ID do artista (ex: A0001): ").strip().upper()
    if id_a not in artistas:
        print("Erro: Artista nao encontrado.")
        return

    a = artistas[id_a]
    verificado_str = "Sim" if a["verificado"] else "Nao"

    print("\n  ID               : " + a["id_artista"])
    print("  Nome             : " + a["nome"])
    print("  Genero           : " + a["genero"])
    print("  Verificado       : " + verificado_str)
    print("  Biografia        : " + a["bio"])
    print("  Imagem Perfil    : " + a["imagem"])
    print("  Imagem Capa      : " + a["imagem_capa"])
    print("  Ouvintes Mensais : " + str(a["ouvintes_mensais"]))
    print("  Seguidores       : " + str(len(a["seguidores"])))
    print("  Discografia      : " + str(len(a["discografia"])) + " lancamento(s)")
    print("  Top Faixas       : " + str(len(a["top_faixas"])) + " faixa(s)")
    print("  Concertos        : " + str(len(a["datas_concertos"])) + " data(s)")
    print("  Escolha Artista  : " + (a["escolha_artista"] if a["escolha_artista"] else "Nao definido"))

    if len(a["discografia"]) > 0:
        print("\n  --- Discografia ---")
        for d in a["discografia"]:
            print("    " + d["tipo"].upper() + " | " + d["titulo"] + " (" + d["ano"] + ")")

    if len(a["seguidores"]) > 0:
        print("  Seguidores (IDs) : " + ", ".join(a["seguidores"]))


def pesquisar_artista_por_nome():
    print("\n-- Pesquisar Artista por Nome --")

    if not artistas:
        print("Aviso: Nenhum artista registado.")
        return

    nome = input("Nome a pesquisar: ").strip().lower()
    if len(nome) == 0:
        print("Erro: Introduza um nome.")
        return

    encontrados = []
    for a in artistas.values():
        if nome in a["nome"].lower():
            encontrados.append(a)

    if len(encontrados) == 0:
        print("Nenhum artista encontrado.")
        return

    print("ID".ljust(8) + "Nome".ljust(25) + "Genero".ljust(20) + "Verificado")
    print("-" * 60)
    for a in encontrados:
        verificado_str = "Sim" if a["verificado"] else "Nao"
        print(a["id_artista"].ljust(8) + a["nome"].ljust(25) + a["genero"].ljust(20) + verificado_str)


# ================================================================
#  UPDATE
# ================================================================

def atualizar_artista():
    print("\n-- Atualizar Artista --")

    if not artistas:
        print("Aviso: Nenhum artista registado.")
        return

    id_a = input("ID do artista: ").strip().upper()
    if id_a not in artistas:
        print("Erro: Artista nao encontrado.")
        return

    a = artistas[id_a]
    print("Deixe em branco para manter o valor atual.\n")

    # --- nome ---
    val = input("Nome [" + a["nome"] + "]: ").strip()
    if val != "":
        if not validar_nome(val):
            print("Erro: Nome invalido.")
            return
        a["nome"] = val

    # --- bio ---
    val = input("Biografia [" + a["bio"] + "]: ").strip()
    if val != "":
        if len(val) < 5:
            print("Erro: Biografia demasiado curta.")
            return
        a["bio"] = val

    # --- imagem ---
    val = input("URL imagem [" + a["imagem"] + "]: ").strip()
    if val != "":
        if not validar_url(val):
            print("Erro: URL invalido.")
            return
        a["imagem"] = val

    # --- imagem_capa ---
    val = input("URL capa [" + a["imagem_capa"] + "]: ").strip()
    if val != "":
        if not validar_url(val):
            print("Erro: URL invalido.")
            return
        a["imagem_capa"] = val

    # --- genero ---
    val = input("Genero [" + a["genero"] + "]: ").strip()
    if val != "":
        if not validar_genero(val):
            print("Erro: Genero invalido.")
            return
        a["genero"] = val

    # --- verificado ---
    estado_atual = "s" if a["verificado"] else "n"
    val = input("Verificado [" + estado_atual + "] (s/n): ").strip().lower()
    if val == "s":
        a["verificado"] = True
    elif val == "n":
        a["verificado"] = False
    elif val != "":
        print("Erro: Resposta invalida. Escreva s ou n.")
        return

    # --- ouvintes_mensais ---
    val = input("Ouvintes mensais [" + str(a["ouvintes_mensais"]) + "]: ").strip()
    if val != "":
        if not validar_ouvintes(val):
            print("Erro: Valor invalido. Introduza um numero positivo.")
            return
        a["ouvintes_mensais"] = int(val)

    # --- escolha_artista ---
    val = input("Escolha do artista [" + (a["escolha_artista"] if a["escolha_artista"] else "vazio") + "]: ").strip()
    if val != "":
        a["escolha_artista"] = val

    # --- adicionar lancamento a discografia ---
    val = input("Adicionar lancamento a discografia? (s/n): ").strip().lower()
    if val == "s":
        titulo = input("  Titulo: ").strip()
        tipo   = input("  Tipo (album/ep/single): ").strip().lower()
        ano    = input("  Ano (ex: 2023): ").strip()
        if len(titulo) < 1 or not validar_tipo_lancamento(tipo) or not validar_ano(ano):
            print("Erro: Dados do lancamento invalidos.")
            return
        a["discografia"].append({"titulo": titulo, "tipo": tipo, "ano": ano})
        print("OK! Lancamento adicionado.")

    # --- adicionar data de concerto ---
    val = input("Adicionar data de concerto? (s/n): ").strip().lower()
    if val == "s":
        data = input("  Data (DD/MM/AAAA, ano 2024-2030): ").strip()
        if not validar_data_concerto(data):
            print("Erro: Data invalida.")
            return
        if data in a["datas_concertos"]:
            print("Erro: Esta data ja existe.")
            return
        a["datas_concertos"].append(data)
        print("OK! Concerto adicionado.")

    # --- adicionar faixa ao top ---
    val = input("Adicionar faixa ao top? (s/n): ").strip().lower()
    if val == "s":
        if len(a["top_faixas"]) >= 5:
            print("Erro: O top ja tem 5 faixas (maximo).")
            return
        faixa = input("  Nome da faixa: ").strip()
        if len(faixa) < 1 or faixa in a["top_faixas"]:
            print("Erro: Faixa invalida ou ja existe no top.")
            return
        a["top_faixas"].append(faixa)
        print("OK! Faixa adicionada ao top.")

    print("OK! Artista " + id_a + " atualizado!")
    guardar_artistas()


# ================================================================
#  RELACAO: UTILIZADOR SEGUE ARTISTA
# ================================================================

def utilizador_seguir_artista():
    print("\n-- Seguir Artista --")

    if not utilizadores or not artistas:
        print("Aviso: E necessario ter utilizadores e artistas registados.")
        return

    id_u = input("ID do utilizador: ").strip().upper()
    id_a = input("ID do artista: ").strip().upper()

    if id_u not in utilizadores:
        print("Erro: Utilizador nao encontrado.")
        return
    if id_a not in artistas:
        print("Erro: Artista nao encontrado.")
        return

    if id_a not in utilizadores[id_u]["seguidos"]:
        utilizadores[id_u]["seguidos"].append(id_a)
        artistas[id_a]["seguidores"].append(id_u)
        print("OK! " + utilizadores[id_u]["nome_exibicao"] + " agora segue " + artistas[id_a]["nome"] + "!")
        guardar_artistas()
        guardar_utilizadores()
    else:
        print("Info: O utilizador ja segue este artista.")


# ================================================================
#  DELETE
# ================================================================

def remover_artista():
    print("\n-- Remover Artista --")

    if not artistas:
        print("Aviso: Nenhum artista registado.")
        return

    id_a = input("ID do artista a remover: ").strip().upper()
    if id_a not in artistas:
        print("Erro: Artista nao encontrado.")
        return

    nome = artistas[id_a]["nome"]
    confirmacao = input("Tem a certeza que quer remover '" + nome + "'? (s/n): ").strip().lower()

    if confirmacao == "s":
        del artistas[id_a]
        print("OK! Artista " + id_a + " removido!")
        guardar_artistas()
    elif confirmacao == "n":
        print("Operacao cancelada.")
    else:
        print("Erro: Resposta invalida. Escreva s ou n.")


# ================================================================
#  LIST
# ================================================================

def listar_artistas():
    print("\n-- Lista de Artistas --")

    if not artistas:
        print("Aviso: Nenhum artista registado.")
        return

    print("ID".ljust(8) + "Nome".ljust(25) + "Genero".ljust(20) + "Ouvintes".ljust(15) + "Verificado")
    print("-" * 75)
    for a in artistas.values():
        verificado_str = "Sim" if a["verificado"] else "Nao"
        print(a["id_artista"].ljust(8) + a["nome"].ljust(25) + a["genero"].ljust(20) + str(a["ouvintes_mensais"]).ljust(15) + verificado_str)


# ================================================================
#  MENU
# ================================================================

def menu_artistas():
    opcoes = {
        "1": criar_artista,
        "2": ler_artista,
        "3": pesquisar_artista_por_nome,
        "4": atualizar_artista,
        "5": remover_artista,
        "6": listar_artistas,
        "7": utilizador_seguir_artista,
    }

    while True:
        print("""
+------------------------------+
|        MENU - ARTISTAS       |
+------------------------------+
|  1. Criar artista            |
|  2. Ver artista              |
|  3. Pesquisar por nome       |
|  4. Atualizar artista        |
|  5. Remover artista          |
|  6. Listar todos             |
|  7. Utilizador seguir        |
|  0. Voltar                   |
+------------------------------+""")

        op = input("Opcao: ").strip()
        if op == "0":
            break
        elif op in opcoes:
            opcoes[op]()
        else:
            print("Opcao invalida.")
