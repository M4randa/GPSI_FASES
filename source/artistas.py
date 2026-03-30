# ==============================
# artistas.py
# CRUD da entidade Artista
# SEM prints nem inputs
# devolve codigos HTTP (200, 201, 404, 500)
# ==============================

from utils import gerar_id_artista, validar_nome, validar_url, validar_genero, validar_ouvintes, validar_ano, validar_tipo_lancamento, validar_verificado, validar_biografia, validar_titulo, validar_faixa, validar_escolha, validar_pesquisa
from utilizadores import utilizadores

artistas = {}


# ==============================
# CREATE
# ==============================

def criar_artista(nome, bio, imagem, imagem_capa, genero, verificado):
    if not validar_nome(nome):
        return 500, "Nome invalido. Minimo 2 caracteres"
    for a in artistas.values():
        if a["nome"].lower() == nome.lower():
            return 500, "Ja existe um artista com esse nome"
    if not validar_biografia(bio):
        return 500, "Biografia demasiado curta. Minimo 5 caracteres"
    if not validar_url(imagem):
        return 500, "URL da imagem invalido"
    if not validar_url(imagem_capa):
        return 500, "URL da capa invalido"
    if not validar_genero(genero):
        return 500, "Genero invalido. Nao pode conter numeros"
    if not validar_verificado(verificado):
        return 500, "Verificado invalido. Use s ou n"

    id_artista = gerar_id_artista()

    artistas[id_artista] = {
        "id_artista":       id_artista,
        "nome":             nome,
        "bio":              bio,
        "imagem":           imagem,
        "imagem_capa":      imagem_capa,
        "genero":           genero,
        "verificado":       verificado == "s",
        "discografia":      [],
        "ouvintes_mensais": 0,
        "seguidores":       [],
        "top_faixas":       [],
        "datas_concertos":  [],
        "escolha_artista":  "",
    }

    return 201, id_artista


# ==============================
# READ (listar todos)
# ==============================

def listar_artistas():
    if not artistas:
        return 404, "Nao existem artistas registados"
    return 200, artistas


# ==============================
# READ (consultar individual)
# ==============================

def consultar_artista(id_artista):
    if id_artista not in artistas:
        return 404, "Artista nao encontrado"
    return 200, artistas[id_artista]


# ==============================
# READ (pesquisar por nome)
# ==============================

def pesquisar_artistas(nome):
    if not validar_pesquisa(nome):
        return 500, "Introduza um nome para pesquisar"
    encontrados = {}
    for id_a, a in artistas.items():
        if nome.lower() in a["nome"].lower():
            encontrados[id_a] = a
    if not encontrados:
        return 404, "Nenhum artista encontrado com esse nome"
    return 200, encontrados


# ==============================
# UPDATE
# ==============================

def atualizar_artista(id_artista, nome=None, bio=None, imagem=None, imagem_capa=None, genero=None, verificado=None, ouvintes_mensais=None, escolha_artista=None):
    if id_artista not in artistas:
        return 404, "Artista nao encontrado"

    if nome is not None:
        if not validar_nome(nome):
            return 500, "Nome invalido. Minimo 2 caracteres"
        artistas[id_artista]["nome"] = nome

    if bio is not None:
        if not validar_biografia(bio):
            return 500, "Biografia demasiado curta. Minimo 5 caracteres"
        artistas[id_artista]["bio"] = bio

    if imagem is not None:
        if not validar_url(imagem):
            return 500, "URL da imagem invalido"
        artistas[id_artista]["imagem"] = imagem

    if imagem_capa is not None:
        if not validar_url(imagem_capa):
            return 500, "URL da capa invalido"
        artistas[id_artista]["imagem_capa"] = imagem_capa

    if genero is not None:
        if not validar_genero(genero):
            return 500, "Genero invalido"
        artistas[id_artista]["genero"] = genero

    if verificado is not None:
        if not validar_verificado(verificado):
            return 500, "Verificado invalido. Use s ou n"
        artistas[id_artista]["verificado"] = verificado == "s"

    if ouvintes_mensais is not None:
        if not validar_ouvintes(ouvintes_mensais):
            return 500, "Ouvintes invalido. Introduza um numero positivo"
        artistas[id_artista]["ouvintes_mensais"] = int(ouvintes_mensais)

    if escolha_artista is not None:
        if not validar_escolha(escolha_artista):
            return 500, "Escolha do artista nao pode estar vazia"
        artistas[id_artista]["escolha_artista"] = escolha_artista

    return 200, "Artista atualizado com sucesso"


# ==============================
# UPDATE - adicionar a discografia
# ==============================

def adicionar_lancamento(id_artista, titulo, tipo, ano):
    if id_artista not in artistas:
        return 404, "Artista nao encontrado"
    if not validar_titulo(titulo):
        return 500, "Titulo invalido"
    if not validar_tipo_lancamento(tipo):
        return 500, "Tipo invalido. Opcoes: album, ep, single"
    if not validar_ano(ano):
        return 500, "Ano invalido. Use 4 digitos numericos entre 1900 e 2025"
    artistas[id_artista]["discografia"].append({"titulo": titulo, "tipo": tipo, "ano": ano})
    return 200, "Lancamento adicionado com sucesso"


# ==============================
# UPDATE - adicionar top faixa
# ==============================

def adicionar_top_faixa(id_artista, faixa):
    if id_artista not in artistas:
        return 404, "Artista nao encontrado"
    if len(artistas[id_artista]["top_faixas"]) >= 5:
        return 500, "O top ja tem 5 faixas (maximo)"
    if not validar_faixa(faixa):
        return 500, "Nome da faixa invalido"
    if faixa in artistas[id_artista]["top_faixas"]:
        return 500, "Esta faixa ja esta no top"
    artistas[id_artista]["top_faixas"].append(faixa)
    return 200, "Faixa adicionada ao top com sucesso"


# ==============================
# DELETE
# ==============================

def remover_artista(id_artista):
    if id_artista not in artistas:
        return 404, "Artista nao encontrado"
    del artistas[id_artista]
    return 200, "Artista removido com sucesso"


# ==============================
# RELACAO: utilizador segue artista
# ==============================

def seguir_artista(id_utilizador, id_artista):
    if id_utilizador not in utilizadores:
        return 404, "Utilizador nao encontrado"
    if id_artista not in artistas:
        return 404, "Artista nao encontrado"
    if id_artista in utilizadores[id_utilizador]["seguidos"]:
        return 500, "O utilizador ja segue este artista"
    utilizadores[id_utilizador]["seguidos"].append(id_artista)
    artistas[id_artista]["seguidores"].append(id_utilizador)
    return 200, "Utilizador agora segue o artista com sucesso"
