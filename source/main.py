
from utilizadores import utilizadores

artistas = {}

# contador local para gerar IDs de artista
_contador_artistas = 1


def _gerar_id_artista():
    global _contador_artistas
    novo_id = "A" + str(_contador_artistas).zfill(3)
    _contador_artistas += 1
    return novo_id


# ==============================
# CREATE
# ==============================

def criar_artista(nome, bio, imagem, imagem_capa, genero, verificado):
    # regra de negocio: nome de artista tem de ser unico
    for a in artistas.values():
        if a["nome"].lower() == nome.lower():
            return 500, "Ja existe um artista com esse nome"

    id_artista = _gerar_id_artista()

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
        artistas[id_artista]["nome"] = nome

    if bio is not None:
        artistas[id_artista]["bio"] = bio

    if imagem is not None:
        artistas[id_artista]["imagem"] = imagem

    if imagem_capa is not None:
        artistas[id_artista]["imagem_capa"] = imagem_capa

    if genero is not None:
        artistas[id_artista]["genero"] = genero

    if verificado is not None:
        artistas[id_artista]["verificado"] = verificado == "s"

    if ouvintes_mensais is not None:
        artistas[id_artista]["ouvintes_mensais"] = int(ouvintes_mensais)

    if escolha_artista is not None:
        artistas[id_artista]["escolha_artista"] = escolha_artista

    return 200, "Artista atualizado com sucesso"


# ==============================
# UPDATE - adicionar a discografia
# ==============================

def adicionar_lancamento(id_artista, titulo, tipo, ano):
    if id_artista not in artistas:
        return 404, "Artista nao encontrado"
    artistas[id_artista]["discografia"].append({"titulo": titulo, "tipo": tipo, "ano": ano})
    return 200, "Lancamento adicionado com sucesso"


# ==============================
# UPDATE - adicionar top faixa
# ==============================

def adicionar_top_faixa(id_artista, faixa):
    if id_artista not in artistas:
        return 404, "Artista nao encontrado"
    # regra de negocio: maximo 5 faixas no top
    if len(artistas[id_artista]["top_faixas"]) >= 5:
        return 500, "O top ja tem 5 faixas (maximo)"
    # regra de negocio: faixa nao pode estar duplicada
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
    # regra de negocio: nao pode seguir duas vezes
    if id_artista in utilizadores[id_utilizador]["seguidos"]:
        return 500, "O utilizador ja segue este artista"
    utilizadores[id_utilizador]["seguidos"].append(id_artista)
    artistas[id_artista]["seguidores"].append(id_utilizador)
    return 200, "Utilizador agora segue o artista com sucesso"
