# ================================================================
#  FICHEIRO: utilizadores.py
#  DESCRICAO: Dados, CRUD e menu da entidade Utilizador
#  AUTOR: Abel Chongolola | GPSI 10A | N 01
# ================================================================

import json
import os
from datetime import date
from utils import validar_nome, validar_url, validar_pais, validar_data, validar_generos, validar_estado

# Dicionario principal - chave: ID, valor: dados do utilizador
utilizadores = {}

# Contador global para IDs unicos (U0001, U0002...)
contador_utilizador = 1

FICHEIRO_UTILIZADORES = "utilizadores.json"


# ================================================================
#  PERSISTENCIA JSON
# ================================================================

def guardar_utilizadores():
    dados = {"contador": contador_utilizador, "utilizadores": utilizadores}
    with open(FICHEIRO_UTILIZADORES, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    print("Dados guardados em " + FICHEIRO_UTILIZADORES)


def carregar_utilizadores():
    global utilizadores, contador_utilizador
    if not os.path.exists(FICHEIRO_UTILIZADORES):
        print("Nenhum ficheiro encontrado, a comecar do zero.")
        return
    with open(FICHEIRO_UTILIZADORES, "r", encoding="utf-8") as f:
        dados = json.load(f)
    contador_utilizador = dados["contador"]
    utilizadores        = dados["utilizadores"]
    print("Utilizadores carregados: " + str(len(utilizadores)) + " registo(s).")


# ================================================================
#  CREATE
# ================================================================

def criar_utilizador():
    global contador_utilizador

    print("\n-- Criar Utilizador --")

    # while True em cada campo: repete ate o utilizador acertar
    while True:
        nome_exibicao = input("Nome de exibicao: ").strip()
        if validar_nome(nome_exibicao):
            break
        print("Erro: Nome invalido. Minimo 2 caracteres.")

    while True:
        nome_utilizador = input("Nome de utilizador (interno): ").strip()
        if not validar_nome(nome_utilizador):
            print("Erro: Nome de utilizador invalido.")
            continue
        # Username tem de ser unico no sistema
        repetido = False
        for u in utilizadores.values():
            if u["nome_utilizador"] == nome_utilizador:
                repetido = True
        if repetido:
            print("Erro: Este nome de utilizador ja esta em uso.")
        else:
            break

    while True:
        foto_perfil = input("URL da foto de perfil (http://...): ").strip()
        if validar_url(foto_perfil):
            break
        print("Erro: URL invalido. Use http:// ou https://")

    while True:
        pais = input("Pais: ").strip()
        if validar_pais(pais):
            break
        print("Erro: Pais invalido. Nao pode conter numeros.")

    while True:
        data_nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()
        if validar_data(data_nascimento):
            break
        print("Erro: Data invalida. Use DD/MM/AAAA (ex: 15/03/2000).")

    while True:
        generos_str = input("Generos preferidos (separados por virgula): ").strip()
        if validar_generos(generos_str):
            break
        print("Erro: Generos invalidos. Minimo 2 caracteres por genero.")

    while True:
        estado_conta = input("Estado da conta (ativo/inativo/premium): ").strip().lower()
        if validar_estado(estado_conta):
            break
        print("Erro: Estado invalido. Opcoes: ativo, inativo, premium.")

    # Data de registo gerada automaticamente pelo sistema
    data_registro = date.today().strftime("%d/%m/%Y")

    id_utilizador = "U" + str(contador_utilizador).zfill(4)
    contador_utilizador += 1

    utilizadores[id_utilizador] = {
        "id_utilizador":      id_utilizador,
        "nome_exibicao":      nome_exibicao,
        "nome_utilizador":    nome_utilizador,
        "foto_perfil":        foto_perfil,
        "seguidores":         [],
        "seguidos":           [],
        "playlists_publicas": [],
        "pais":               pais,
        "data_nascimento":    data_nascimento,
        "generos_preferidos": [g.strip() for g in generos_str.split(",")],
        "historico_consumo":  [],
        "data_registro":      data_registro,
        "estado_conta":       estado_conta,
    }

    print("OK! Utilizador criado com ID: " + id_utilizador)
    guardar_utilizadores()


# ================================================================
#  READ
# ================================================================

def ler_utilizador():
    print("\n-- Ler Utilizador --")

    if not utilizadores:
        print("Aviso: Nenhum utilizador registado.")
        return

    id_u = input("ID do utilizador (ex: U0001): ").strip().upper()
    if id_u not in utilizadores:
        print("Erro: Utilizador nao encontrado.")
        return

    u = utilizadores[id_u]
    print("\n  ID               : " + u["id_utilizador"])
    print("  Nome de Exibicao : " + u["nome_exibicao"])
    print("  Username         : " + u["nome_utilizador"])
    print("  Foto de Perfil   : " + u["foto_perfil"])
    print("  Pais             : " + u["pais"])
    print("  Nascimento       : " + u["data_nascimento"])
    print("  Generos          : " + ", ".join(u["generos_preferidos"]))
    print("  Data de Registo  : " + u["data_registro"])
    print("  Estado da Conta  : " + u["estado_conta"])
    print("  Seguidores       : " + str(len(u["seguidores"])))
    print("  Seguindo         : " + str(len(u["seguidos"])))
    if len(u["seguidos"]) > 0:
        print("  Artistas seguidos: " + ", ".join(u["seguidos"]))


def pesquisar_utilizador_por_nome():
    print("\n-- Pesquisar Utilizador por Nome --")

    if not utilizadores:
        print("Aviso: Nenhum utilizador registado.")
        return

    nome = input("Nome a pesquisar: ").strip().lower()
    if len(nome) == 0:
        print("Erro: Introduza um nome.")
        return

    encontrados = []
    for u in utilizadores.values():
        if nome in u["nome_exibicao"].lower() or nome in u["nome_utilizador"].lower():
            encontrados.append(u)

    if len(encontrados) == 0:
        print("Nenhum utilizador encontrado.")
        return

    print("ID".ljust(8) + "Nome".ljust(25) + "Username".ljust(20) + "Estado")
    print("-" * 65)
    for u in encontrados:
        print(u["id_utilizador"].ljust(8) + u["nome_exibicao"].ljust(25) + u["nome_utilizador"].ljust(20) + u["estado_conta"])


# ================================================================
#  UPDATE
# ================================================================

def atualizar_utilizador():
    print("\n-- Atualizar Utilizador --")

    if not utilizadores:
        print("Aviso: Nenhum utilizador registado.")
        return

    id_u = input("ID do utilizador: ").strip().upper()
    if id_u not in utilizadores:
        print("Erro: Utilizador nao encontrado.")
        return

    u = utilizadores[id_u]
    print("Deixe em branco para manter o valor atual.\n")

    # --- nome_exibicao ---
    val = input("Nome de exibicao [" + u["nome_exibicao"] + "]: ").strip()
    if val != "":
        if not validar_nome(val):
            print("Erro: Nome invalido.")
            return
        u["nome_exibicao"] = val

    # --- foto_perfil ---
    val = input("URL da foto [" + u["foto_perfil"] + "]: ").strip()
    if val != "":
        if not validar_url(val):
            print("Erro: URL invalido. Use http:// ou https://")
            return
        u["foto_perfil"] = val

    # --- pais ---
    val = input("Pais [" + u["pais"] + "]: ").strip()
    if val != "":
        if not validar_pais(val):
            print("Erro: Pais invalido.")
            return
        u["pais"] = val

    # --- estado_conta ---
    val = input("Estado da conta [" + u["estado_conta"] + "]: ").strip().lower()
    if val != "":
        if not validar_estado(val):
            print("Erro: Estado invalido. Opcoes: ativo, inativo, premium.")
            return
        u["estado_conta"] = val

    # --- generos_preferidos ---
    val = input("Generos [" + ", ".join(u["generos_preferidos"]) + "]: ").strip()
    if val != "":
        if not validar_generos(val):
            print("Erro: Generos invalidos.")
            return
        u["generos_preferidos"] = [g.strip() for g in val.split(",")]

    # --- deixar de seguir artista ---
    if len(u["seguidos"]) > 0:
        print("Artistas seguidos: " + ", ".join(u["seguidos"]))
        val = input("ID do artista a deixar de seguir (Enter para ignorar): ").strip().upper()
        if val != "":
            if val not in u["seguidos"]:
                print("Erro: O utilizador nao segue este artista.")
                return
            u["seguidos"].remove(val)
            print("OK! Deixou de seguir " + val)

    print("OK! Utilizador " + id_u + " atualizado!")
    guardar_utilizadores()


# ================================================================
#  DELETE
# ================================================================

def remover_utilizador():
    print("\n-- Remover Utilizador --")

    if not utilizadores:
        print("Aviso: Nenhum utilizador registado.")
        return

    id_u = input("ID do utilizador a remover: ").strip().upper()
    if id_u not in utilizadores:
        print("Erro: Utilizador nao encontrado.")
        return

    nome = utilizadores[id_u]["nome_exibicao"]
    confirmacao = input("Tem a certeza que quer remover '" + nome + "'? (s/n): ").strip().lower()

    if confirmacao == "s":
        del utilizadores[id_u]
        print("OK! Utilizador " + id_u + " removido!")
        guardar_utilizadores()
    elif confirmacao == "n":
        print("Operacao cancelada.")
    else:
        print("Erro: Resposta invalida. Escreva s ou n.")


# ================================================================
#  LIST
# ================================================================

def listar_utilizadores():
    print("\n-- Lista de Utilizadores --")

    if not utilizadores:
        print("Aviso: Nenhum utilizador registado.")
        return

    print("ID".ljust(8) + "Nome".ljust(25) + "Username".ljust(20) + "Estado".ljust(12) + "Pais")
    print("-" * 75)
    for u in utilizadores.values():
        print(u["id_utilizador"].ljust(8) + u["nome_exibicao"].ljust(25) + u["nome_utilizador"].ljust(20) + u["estado_conta"].ljust(12) + u["pais"])


# ================================================================
#  MENU
# ================================================================

def menu_utilizadores():
    opcoes = {
        "1": criar_utilizador,
        "2": ler_utilizador,
        "3": pesquisar_utilizador_por_nome,
        "4": atualizar_utilizador,
        "5": remover_utilizador,
        "6": listar_utilizadores,
    }

    while True:
        print("""
+------------------------------+
|      MENU - UTILIZADORES     |
+------------------------------+
|  1. Criar utilizador         |
|  2. Ver utilizador           |
|  3. Pesquisar por nome       |
|  4. Atualizar utilizador     |
|  5. Remover utilizador       |
|  6. Listar todos             |
|  0. Voltar                   |
+------------------------------+""")

        op = input("Opcao: ").strip()
        if op == "0":
            break
        elif op in opcoes:
            opcoes[op]()
        else:
            print("Opcao invalida.")
