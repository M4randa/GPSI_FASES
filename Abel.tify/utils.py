# ================================================================
#  FICHEIRO: utils.py
#  DESCRICAO: Funcoes de validacao partilhadas por todos os modulos
#  AUTOR: Abel Chongolola | GPSI 10A | N 01
# ================================================================


def so_numeros(texto):
    # Verifica se todos os caracteres estao entre "0" e "9"
    # Usamos comparacao directa em vez de isdigit()
    if len(texto) == 0:
        return False
    for c in texto:
        if c < "0" or c > "9":
            return False
    return True


def validar_nome(nome):
    # Nome nao pode estar vazio nem ter menos de 2 caracteres
    if len(nome) < 2:
        return False
    return True


def validar_url(url):
    # URL tem de comecar com http:// ou https://
    if url.startswith("http://"):
        return True
    elif url.startswith("https://"):
        return True
    else:
        return False


def validar_data(data):
    # Formato esperado: DD/MM/AAAA
    if len(data) != 10:
        return False
    if data[2] != "/" or data[5] != "/":
        return False
    dia = data[0:2]
    mes = data[3:5]
    ano = data[6:10]
    if not so_numeros(dia) or not so_numeros(mes) or not so_numeros(ano):
        return False
    if int(dia) < 1 or int(dia) > 31:
        return False
    if int(mes) < 1 or int(mes) > 12:
        return False
    if int(ano) < 1900 or int(ano) > 2025:
        return False
    return True


def validar_data_concerto(data):
    # Formato DD/MM/AAAA com ano entre 2024 e 2030
    if len(data) != 10:
        return False
    if data[2] != "/" or data[5] != "/":
        return False
    dia = data[0:2]
    mes = data[3:5]
    ano = data[6:10]
    if not so_numeros(dia) or not so_numeros(mes) or not so_numeros(ano):
        return False
    if int(dia) < 1 or int(dia) > 31:
        return False
    if int(mes) < 1 or int(mes) > 12:
        return False
    if int(ano) < 2024 or int(ano) > 2030:
        return False
    return True


def validar_estado(estado):
    # Estado tem de ser exactamente uma das 3 opcoes
    if estado == "ativo":
        return True
    elif estado == "inativo":
        return True
    elif estado == "premium":
        return True
    else:
        return False


def validar_pais(pais):
    # Pais nao pode estar vazio nem conter numeros
    if len(pais) < 2:
        return False
    for c in pais:
        if c >= "0" and c <= "9":
            return False
    return True


def validar_generos(generos):
    # Pelo menos um genero com minimo 2 caracteres
    lista = [g.strip() for g in generos.split(",")]
    for g in lista:
        if len(g) < 2:
            return False
    return True


def validar_genero(genero):
    # Genero unico sem numeros
    if len(genero) < 2:
        return False
    for c in genero:
        if c >= "0" and c <= "9":
            return False
    return True


def validar_ouvintes(valor):
    # Numero inteiro positivo sem isdigit
    if len(valor) == 0:
        return False
    for c in valor:
        if c < "0" or c > "9":
            return False
    if int(valor) < 0:
        return False
    return True


def validar_ano(ano):
    # Ano com 4 digitos entre 1900 e 2025
    if len(ano) != 4:
        return False
    if not so_numeros(ano):
        return False
    if int(ano) < 1900 or int(ano) > 2025:
        return False
    return True


def validar_tipo_lancamento(tipo):
    # Tipo tem de ser album, ep ou single
    if tipo == "album":
        return True
    elif tipo == "ep":
        return True
    elif tipo == "single":
        return True
    else:
        return False
