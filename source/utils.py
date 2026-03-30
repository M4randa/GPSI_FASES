# ==============================
# utils.py
# funcoes auxiliares partilhadas
# ==============================

# contadores para gerar IDs automaticos
contador_utilizadores = 1
contador_artistas     = 1


def gerar_id_utilizador():
    global contador_utilizadores
    novo_id = "U" + str(contador_utilizadores).zfill(3)
    contador_utilizadores += 1
    return novo_id


def gerar_id_artista():
    global contador_artistas
    novo_id = "A" + str(contador_artistas).zfill(3)
    contador_artistas += 1
    return novo_id


def validar_nome(nome):
    if len(nome) < 2:
        return False
    return True


def validar_url(url):
    if url.startswith("http://"):
        return True
    elif url.startswith("https://"):
        return True
    else:
        return False


def validar_data(data):
    if len(data) != 10:
        return False
    if data[2] != "/" or data[5] != "/":
        return False
    dia = data[0:2]
    mes = data[3:5]
    ano = data[6:10]
    for c in dia + mes + ano:
        if c < "0" or c > "9":
            return False
    if int(dia) < 1 or int(dia) > 31:
        return False
    if int(mes) < 1 or int(mes) > 12:
        return False
    if int(ano) < 1900 or int(ano) > 2025:
        return False
    return True


def validar_estado_conta(estado):
    if estado == "ativo":
        return True
    elif estado == "inativo":
        return True
    elif estado == "premium":
        return True
    else:
        return False


def validar_pais(pais):
    if len(pais) < 2:
        return False
    for c in pais:
        if c >= "0" and c <= "9":
            return False
    return True


def validar_generos(generos):
    lista = [g.strip() for g in generos.split(",")]
    for g in lista:
        if len(g) < 2:
            return False
    return True


def validar_genero(genero):
    if len(genero) < 2:
        return False
    for c in genero:
        if c >= "0" and c <= "9":
            return False
    return True


def validar_ouvintes(valor):
    if len(valor) == 0:
        return False
    for c in valor:
        if c < "0" or c > "9":
            return False
    return True


def validar_ano(ano):
    if len(ano) != 4:
        return False
    for c in ano:
        if c < "0" or c > "9":
            return False
    if int(ano) < 1900 or int(ano) > 2025:
        return False
    return True


def validar_tipo_lancamento(tipo):
    if tipo == "album":
        return True
    elif tipo == "ep":
        return True
    elif tipo == "single":
        return True
    else:
        return False


def validar_verificado(valor):
    if valor == "s":
        return True
    elif valor == "n":
        return True
    else:
        return False


def validar_biografia(bio):
    if len(bio) < 5:
        return False
    return True


def validar_titulo(titulo):
    if len(titulo) < 1:
        return False
    return True


def validar_faixa(faixa):
    if len(faixa) < 1:
        return False
    return True


def validar_escolha(escolha):
    if len(escolha) < 1:
        return False
    return True


def validar_pesquisa(termo):
    if len(termo) == 0:
        return False
    return True
