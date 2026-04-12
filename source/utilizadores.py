
from datetime import date

utilizadores = {}

# contador local para gerar IDs de utilizador
_contador_utilizadores = 1


def _gerar_id_utilizador():
    global _contador_utilizadores
    novo_id = "U" + str(_contador_utilizadores).zfill(3)
    _contador_utilizadores += 1
    return novo_id


# ==============================
# CREATE
# ==============================

def criar_utilizador(nome, nome_utilizador, foto_perfil, pais, data_nascimento, generos, estado_conta):
    # regra de negocio: nome de exibicao nao pode ser igual ao nome interno
    if nome.lower() == nome_utilizador.lower():
        return 500, "Nome de exibicao nao pode ser igual ao nome de utilizador"

    # regra de negocio: nome de utilizador tem de ser unico
    for u in utilizadores.values():
        if u["nome_utilizador"] == nome_utilizador:
            return 500, "Nome de utilizador ja esta em uso"

    id_utilizador = _gerar_id_utilizador()
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
        # regra de negocio: nome de exibicao nao pode ser igual ao nome interno
        if nome.lower() == utilizadores[id_utilizador]["nome_utilizador"].lower():
            return 500, "Nome de exibicao nao pode ser igual ao nome de utilizador"
        utilizadores[id_utilizador]["nome_exibicao"] = nome

    if foto_perfil is not None:
        utilizadores[id_utilizador]["foto_perfil"] = foto_perfil

    if pais is not None:
        utilizadores[id_utilizador]["pais"] = pais

    if estado_conta is not None:
        utilizadores[id_utilizador]["estado_conta"] = estado_conta

    if generos is not None:
        utilizadores[id_utilizador]["generos_preferidos"] = [g.strip() for g in generos.split(",")]

    return 200, "Utilizador atualizado com sucesso"


# ==============================
# DELETE
# ==============================

def remover_utilizador(id_utilizador):
    if id_utilizador not in utilizadores:
        return 404, "Utilizador nao encontrado"
    del utilizadores[id_utilizador]
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
    return 200, "Deixou de seguir o artista com sucesso"