# ==============================
# playlists.py
# CRUD da entidade Playlist
# SEM prints nem inputs
# devolve codigos HTTP (200, 201, 404, 500)
# ==============================

from utils import (
    validar_nome,
    validar_url,
    validar_privacidade,
    validar_descricao,
    validar_booleano
)
from utilizadores import utilizadores

from datetime import datetime

playlists = {}

_contador_playlists = 1


def _gerar_id_playlist():
    global _contador_playlists
    novo_id = "P" + str(_contador_playlists).zfill(3)
    _contador_playlists += 1
    return novo_id


# ==============================
# CREATE
# ==============================

def criar_playlist(nome_playlist, id_utilizador, privacidade, descricao, capa_playlist):
    if not validar_nome(nome_playlist):
        return 500, "Nome invalido"
    if id_utilizador not in utilizadores:
        return 404, "Utilizador nao encontrado"
    if not validar_privacidade(privacidade):
        return 500, "Privacidade invalida. Use publica ou privada"
    if not validar_descricao(descricao):
        return 500, "Descricao invalida"
    if not validar_url(capa_playlist):
        return 500, "URL da capa invalido"

    id_playlist = _gerar_id_playlist()

    playlists[id_playlist] = {
        "id_playlist": id_playlist,
        "nome_playlist": nome_playlist,
        "id_utilizador": id_utilizador,
        "privacidade": privacidade,
        "lista_ids": [],
        "descricao": descricao,
        "capa_playlist": capa_playlist,
        "data_criacao": datetime.now().strftime("%d/%m/%Y"),
        "seguidores_playlist": [],
        "ordem_musicas": [],
        "flag_remocao": False
    }

    return 201, playlists[id_playlist]


# ==============================
# READ
# ==============================

def listar_playlists():
    if not playlists:
        return 404, "Nao existem playlists registadas"
    return 200, playlists


def consultar_playlist(id_playlist):
    if id_playlist not in playlists:
        return 404, "Playlist nao encontrada"
    return 200, playlists[id_playlist]


# ==============================
# UPDATE
# ==============================

def atualizar_playlist(id_playlist, nome_playlist=None, privacidade=None, descricao=None, flag_remocao=None):
    if id_playlist not in playlists:
        return 404, "Playlist nao encontrada"

    if nome_playlist is not None:
        if not validar_nome(nome_playlist):
            return 500, "Nome invalido"
        playlists[id_playlist]["nome_playlist"] = nome_playlist

    if privacidade is not None:
        if not validar_privacidade(privacidade):
            return 500, "Privacidade invalida"
        playlists[id_playlist]["privacidade"] = privacidade

    if descricao is not None:
        if not validar_descricao(descricao):
            return 500, "Descricao invalida"
        playlists[id_playlist]["descricao"] = descricao

    if flag_remocao is not None:
        if not validar_booleano(flag_remocao):
            return 500, "Flag de remocao invalida"
        playlists[id_playlist]["flag_remocao"] = bool(flag_remocao)

    return 200, playlists[id_playlist]


# ==============================
# UPDATE - adicionar/remover musicas
# ==============================

def adicionar_musica_playlist(id_playlist, id_musica):
    if id_playlist not in playlists:
        return 404, "Playlist nao encontrada"
    if id_musica not in musicas:
        return 404, "Musica nao encontrada"
    if id_musica in playlists[id_playlist]["lista_ids"]:
        return 500, "Musica ja existente na playlist"

    playlists[id_playlist]["lista_ids"].append(id_musica)
    playlists[id_playlist]["ordem_musicas"].append(id_musica)

    return 200, playlists[id_playlist]


def remover_musica_playlist(id_playlist, id_musica):
    if id_playlist not in playlists:
        return 404, "Playlist nao encontrada"
    if id_musica not in playlists[id_playlist]["lista_ids"]:
        return 404, "Musica nao encontrada na playlist"

    playlists[id_playlist]["lista_ids"].remove(id_musica)
    if id_musica in playlists[id_playlist]["ordem_musicas"]:
        playlists[id_playlist]["ordem_musicas"].remove(id_musica)

    return 200, playlists[id_playlist]


# ==============================
# DELETE
# ==============================

def remover_playlist(id_playlist):
    if id_playlist not in playlists:
        return 404, "Playlist nao encontrada"
    del playlists[id_playlist]
    return 200, id_playlist


# ==============================
# RELACAO: utilizador segue playlist
# ==============================

def seguir_playlist(id_utilizador, id_playlist):
    if id_utilizador not in utilizadores:
        return 404, "Utilizador nao encontrado"
    if id_playlist not in playlists:
        return 404, "Playlist nao encontrada"
    if id_utilizador in playlists[id_playlist]["seguidores_playlist"]:
        return 500, "Utilizador ja segue esta playlist"
    playlists[id_playlist]["seguidores_playlist"].append(id_utilizador)
    return 200, playlists[id_playlist]