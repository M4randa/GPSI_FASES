# ==============================
# musicas.py
# CRUD da entidade Musica
# SEM prints nem inputs
# devolve codigos HTTP (200, 201, 404, 500)
# ==============================

from utils import (
    validar_nome,
    validar_url,
    validar_duracao,
    validar_isrc,
    validar_data,
    validar_letra,
    validar_bitrate,
    validar_reproducoes,
    validar_booleano
)

from artistas import artistas

musicas = {}

_contador_musicas = 1


def _gerar_id_musica():
    global _contador_musicas
    novo_id = "M" + str(_contador_musicas).zfill(3)
    _contador_musicas += 1
    return novo_id


# ==============================
# CREATE
# ==============================

def criar_musica(titulo, id_artista, duracao_ms, isrc, data_lancamento, letra, bitrate, flag_explicito, status_takedown, disponibilidade):
    if not validar_nome(titulo):
        return 500, "Titulo invalido. Minimo 2 caracteres"
    if id_artista not in artistas:
        return 404, "Artista nao encontrado"
    if not validar_duracao(duracao_ms):
        return 500, "Duracao invalida. Deve ser um numero inteiro"
    if not validar_isrc(isrc):
        return 500, "Codigo ISRC invalido"
    if not validar_data(data_lancamento):
        return 500, "Data invalida. Use DD/MM/AAAA"
    if not validar_letra(letra):
        return 500, "Letra invalida. Minimo 5 caracteres"
    if not validar_bitrate(bitrate):
        return 500, "Bitrate invalido. Exemplo: 320"
    if not validar_booleano(flag_explicito):
        return 500, "Flag explicito invalida"
    if not validar_booleano(status_takedown):
        return 500, "Status takedown invalido"
    if not validar_booleano(disponibilidade):
        return 500, "Disponibilidade invalida"

    id_musica = _gerar_id_musica()

    musicas[id_musica] = {
        "id_musica": id_musica,
        "titulo": titulo,
        "id_artista": id_artista,
        "duracao_ms": int(duracao_ms),
        "isrc": isrc,
        "data_lancamento": data_lancamento,
        "letra": letra,
        "bitrate": int(bitrate),
        "contagem_reproducoes": 0,
        "flag_explicito": bool(flag_explicito),
        "status_takedown": bool(status_takedown),
        "disponibilidade": bool(disponibilidade),
    }

    return 201, musicas[id_musica]


# ==============================
# READ
# ==============================

def listar_musicas():
    if not musicas:
        return 404, "Nao existem musicas registadas"
    return 200, musicas


def consultar_musica(id_musica):
    if id_musica not in musicas:
        return 404, "Musica nao encontrada"
    return 200, musicas[id_musica]


def pesquisar_musicas(nome):
    if not nome or len(nome.strip()) < 1:
        return 500, "Introduza um nome valido para pesquisa"
    encontrados = {}
    for id_m, m in musicas.items():
        if nome.lower() in m["titulo"].lower():
            encontrados[id_m] = m
    if not encontrados:
        return 404, "Nenhuma musica encontrada"
    return 200, encontrados


# ==============================
# UPDATE
# ==============================

def atualizar_musica(id_musica, titulo=None, duracao_ms=None, letra=None, bitrate=None, flag_explicito=None, disponibilidade=None):
    if id_musica not in musicas:
        return 404, "Musica nao encontrada"

    if titulo is not None:
        if not validar_nome(titulo):
            return 500, "Titulo invalido"
        musicas[id_musica]["titulo"] = titulo

    if duracao_ms is not None:
        if not validar_duracao(duracao_ms):
            return 500, "Duracao invalida"
        musicas[id_musica]["duracao_ms"] = int(duracao_ms)

    if letra is not None:
        if not validar_letra(letra):
            return 500, "Letra invalida"
        musicas[id_musica]["letra"] = letra

    if bitrate is not None:
        if not validar_bitrate(bitrate):
            return 500, "Bitrate invalido"
        musicas[id_musica]["bitrate"] = int(bitrate)

    if flag_explicito is not None:
        if not validar_booleano(flag_explicito):
            return 500, "Flag explicito invalida"
        musicas[id_musica]["flag_explicito"] = bool(flag_explicito)

    if disponibilidade is not None:
        if not validar_booleano(disponibilidade):
            return 500, "Disponibilidade invalida"
        musicas[id_musica]["disponibilidade"] = bool(disponibilidade)

    return 200, musicas[id_musica]


# ==============================
# DELETE
# ==============================

def remover_musica(id_musica):
    if id_musica not in musicas:
        return 404, "Musica nao encontrada"
    del musicas[id_musica]
    return 200, id_musica