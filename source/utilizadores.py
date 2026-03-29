# ==============================
# utilizadores.py
# CRUD da entidade Utilizador
# SEM prints nem inputs
# devolve codigos HTTP (200, 201, 404, 500)
# ==============================

import json
import os
from datetime import date
from utils import gerar_id_utilizador, validar_nome, validar_url, validar_pais, validar_data, validar_generos, validar_estado_conta

utilizadores = {}

FICHEIRO = "utilizadores.json"


# ==============================
# PERSISTENCIA JSON
# ==============================

def guardar_utilizadores():
    with open(FICHEIRO, "w", encoding="utf-8") as f:
        json.dump(utilizadores, f, indent=4, ensure_ascii=False)
    return 200, "Dados guardados com sucesso"


def carregar_utilizadores():
    global utilizadores
    if not os.path.exists(FICHEIRO):
        return 404, "Ficheiro nao encontrado, a comecar do zero"
    with open(FICHEIRO, "r", encoding="utf-8") as f:
        utilizadores = json.load(f)
    return 200, "Utilizadores carregados com sucesso"


# ==============================
# CREATE
# ==============================

def criar_utilizador(nome, nome_utilizador, foto_perfil, pais, data_nascimento, generos, estado_conta):
    if not validar_nome(nome):
        return 500, "Nome invalido. Minimo 2 caracteres"
    if not validar_nome(nome_utilizador):
        return 500, "Nome de utilizador invalido"
    # username tem de ser unico
    for u in utilizadores.values():
        if u["nome_utilizador"] == nome_utilizador:
            return 500, "Nome de utilizador ja esta em uso"
    if not validar_url(foto_perfil):
        return 500, "URL invalido. Use http:// ou https://"
    if not validar_pais(pais):
        return 500, "Pais invalido. Nao pode conter numeros"
    if not validar_data(data_nascimento):
        return 500, "Data invalida. Use formato DD/MM/AAAA"
    if not validar_generos(generos):
        return 500, "Generos invalidos. Minimo 2 caracteres por genero"
    if not validar_estado_conta(estado_conta):
        return 500, "Estado invalido. Opcoes: ativo, inativo, premium"

    id_utilizador = gerar_id_utilizador()
    # data de registo gerada automaticamente pelo sistema
    data_registro = date.today().strftime("%d/%m/%Y")

    utilizadores[id_utilizador] = {
        "id_utilizador":      id_utilizador,
        "nome_exibicao":      nome,
        "nome_utilizador":    nome_utilizador,
        "foto_perfil":        foto_perfil,
        "pais":               pais,
        "data_nascimento":    data_nascimento,
        "generos_preferidos": [g.strip() for g in generos.split(",")],
        "data_registro":      data_registro,
        "estado_conta":       estado_conta,
        "seguidores":         [],
        "seguidos":           [],
        "playlists_publicas": [],
        "historico_consumo":  [],
    }

    guardar_utilizadores()
    return 201, id_utilizador


# ==============================
# READ (listar todos)
# ==============================

def listar_utilizadores():
    if not utilizadores:
        return 404, "Nao existem utilizadores registados"
    return 200, utilizadores


# ==============================
# READ (consultar individual)
# ==============================

def consultar_utilizador(id_utilizador):
    if id_utilizador not in utilizadores:
        return 404, "Utilizador nao encontrado"
    return 200, utilizadores[id_utilizador]


# ==============================
# READ (pesquisar por nome)
# ==============================

def pesquisar_utilizadores(nome):
    if len(nome) == 0:
        return 500, "Introduza um nome para pesquisar"
    encontrados = {}
    for id_u, u in utilizadores.items():
        if nome.lower() in u["nome_exibicao"].lower() or nome.lower() in u["nome_utilizador"].lower():
            encontrados[id_u] = u
    if not encontrados:
        return 404, "Nenhum utilizador encontrado com esse nome"
    return 200, encontrados


# ==============================
# UPDATE
# ==============================

def atualizar_utilizador(id_utilizador, nome=None, foto_perfil=None, pais=None, estado_conta=None, generos=None):
    if id_utilizador not in utilizadores:
        return 404, "Utilizador nao encontrado"

    if nome is not None:
        if not validar_nome(nome):
            return 500, "Nome invalido. Minimo 2 caracteres"
        utilizadores[id_utilizador]["nome_exibicao"] = nome

    if foto_perfil is not None:
        if not validar_url(foto_perfil):
            return 500, "URL invalido. Use http:// ou https://"
        utilizadores[id_utilizador]["foto_perfil"] = foto_perfil

    if pais is not None:
        if not validar_pais(pais):
            return 500, "Pais invalido. Nao pode conter numeros"
        utilizadores[id_utilizador]["pais"] = pais

    if estado_conta is not None:
        if not validar_estado_conta(estado_conta):
            return 500, "Estado invalido. Opcoes: ativo, inativo, premium"
        utilizadores[id_utilizador]["estado_conta"] = estado_conta

    if generos is not None:
        if not validar_generos(generos):
            return 500, "Generos invalidos"
        utilizadores[id_utilizador]["generos_preferidos"] = [g.strip() for g in generos.split(",")]

    guardar_utilizadores()
    return 200, "Utilizador atualizado com sucesso"


# ==============================
# DELETE
# ==============================

def remover_utilizador(id_utilizador):
    if id_utilizador not in utilizadores:
        return 404, "Utilizador nao encontrado"
    del utilizadores[id_utilizador]
    guardar_utilizadores()
    return 200, "Utilizador removido com sucesso"


# ==============================
# RELACAO: deixar de seguir artista
# ==============================

def unfollow_artista(id_utilizador, id_artista):
    if id_utilizador not in utilizadores:
        return 404, "Utilizador nao encontrado"
    if id_artista not in utilizadores[id_utilizador]["seguidos"]:
        return 404, "O utilizador nao segue este artista"
    utilizadores[id_utilizador]["seguidos"].remove(id_artista)
    guardar_utilizadores()
    return 200, "Deixou de seguir o artista com sucesso"
