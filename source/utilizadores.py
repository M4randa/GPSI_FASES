# ==============================
# musica.py
# CRUD da entidade Musica
# SEM prints nem inputs
# devolve codigos HTTP (200, 201, 404, 500)
# ==============================

import json
import os
from utils import (
    gerar_id_musica,
    validar_nome,
    validar_duracao,
    validar_isrc,
    validar_data,
    validar_letra,
    validar_bitrate,
    validar_booleano,
    validar_pesquisa
)

FICHEIRO_MUSICAS = "musicas.json"

musicas = {}

logger = configurar_logger()

_contador_musicas = 1


# ==============================
# PERSISTENCIA
# ==============================

def guardar_musicas():
    with open(FICHEIRO_MUSICAS, "w", encoding="utf-8") as f:
        json.dump(musicas, f, indent=4, ensure_ascii=False)


def carregar_musicas():
    if os.path.exists(FICHEIRO_MUSICAS):
        with open(FICHEIRO_MUSICAS, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def gerar_id_musica():
    global _contador_musicas
    novo_id = "M" + str(_contador_musicas).zfill(3)
    _contador_musicas += 1
    return novo_id


# ==============================
# CREATE
# ==============================

def criar_musica(titulo, id_artista, duracao_ms, isrc, data_lancamento, letra, bitrate, flag_explicito, status_takedown, disponibilidade):
    musicas = carregar_musicas()
    artistas = carregar_artistas()
    if not validar_nome(titulo):
        return 500, "Titulo invalido. Minimo 2 caracteres"
    if id_artista not in artistas:
        logger.error("Artista nao encontrado: " + id_artista)
        return 404, "Artista nao encontrado"
    if not validar_duracao(duracao_ms):
        return 500, "Duracao invalida. Deve ser um numero inteiro positivo"
    if not validar_isrc(isrc):
        return 500, "Codigo ISRC invalido. Deve ter 12 caracteres"
    if not validar_data(data_lancamento):
        return 500, "Data invalida. Use DD/MM/AAAA"
    if not validar_letra(letra):
        return 500, "Letra invalida. Minimo 5 caracteres"
    if not validar_bitrate(bitrate):
        return 500, "Bitrate invalido. Exemplo: 320"
    if not validar_booleano(flag_explicito):
        return 500, "Flag explicito invalida. Use s ou n"
    if not validar_booleano(status_takedown):
        return 500, "Status takedown invalido. Use s ou n"
    if not validar_booleano(disponibilidade):
        return 500, "Disponibilidade invalida. Use s ou n"

    id_musica = gerar_id_musica()
    musica = {
        "id_musica":            id_musica,
        "titulo":               titulo,
        "id_artista":           id_artista,
        "duracao_ms":           int(duracao_ms),
        "isrc":                 isrc,
        "data_lancamento":      data_lancamento,
        "letra":                letra,
        "bitrate":              int(bitrate),
        "contagem_reproducoes": 0,
        "flag_explicito":       flag_explicito == "s",
        "status_takedown":      status_takedown == "s",
        "disponibilidade":      disponibilidade == "s",
    }
    musicas[id_musica] = musica
    guardar_musicas()
    logger.info("Musica criada: " + id_musica)
    return 201, musica


# ==============================
# READ (listar todas)
# ==============================

def listar_musicas():
    musicas = carregar_musicas()
    if not musicas:
        return 404, "Nao existem musicas registadas"
    return 200, musicas


# ==============================
# READ (consultar individual)
# ==============================

def consultar_musica(id_musica):
    musicas = carregar_musicas()
    if id_musica not in musicas:
        return 404, "Musica nao encontrada"
    return 200, musicas[id_musica]


# ==============================
# READ (pesquisar por titulo)
# ==============================

def pesquisar_musicas(nome):
    musicas = carregar_musicas()
    if not validar_pesquisa(nome):
        return 500, "Introduza um titulo para pesquisar"
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
    musicas = carregar_musicas()
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
            return 500, "Flag explicito invalida. Use s ou n"
        musicas[id_musica]["flag_explicito"] = flag_explicito == "s"

    if disponibilidade is not None:
        if not validar_booleano(disponibilidade):
            return 500, "Disponibilidade invalida. Use s ou n"
        musicas[id_musica]["disponibilidade"] = disponibilidade == "s"

    guardar_musicas()
    logger.info("Musica atualizada: " + id_musica)
    return 200, musicas[id_musica]


# ==============================
# UPDATE - registar reproducao
# ==============================

def registar_reproducao(id_musica, id_utilizador):
    musicas = carregar_musicas()
    utilizadores = carregar_utilizadores()
    if id_musica not in musicas:
        return 404, "Musica nao encontrada"
    if id_utilizador not in utilizadores:
        return 404, "Utilizador nao encontrado"
    if not musicas[id_musica]["disponibilidade"]:
        logger.warning("Musica nao disponivel: " + id_musica)
        return 500, "Musica nao disponivel"
    if musicas[id_musica]["status_takedown"]:
        return 500, "Musica removida por direitos autorais"
    musicas[id_musica]["contagem_reproducoes"] += 1
    utilizadores[id_utilizador]["historico_consumo"].append(id_musica)
    logger.debug("Reproducao registada: musica " + id_musica + " por " + id_utilizador)
    guardar_musicas()
    guardar_utilizadores()
    return 200, musicas[id_musica]


# ==============================
# DELETE
# ==============================

def remover_musica(id_musica):
    musicas = carregar_musicas()
    if id_musica not in musicas:
        return 404, "Musica nao encontrada"
    del musicas[id_musica]
    guardar_musicas()
    logger.info("Musica removida: " + id_musica)
    return 200, id_musica
