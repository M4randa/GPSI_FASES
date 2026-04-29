# ==============================
# utils.py
# TODAS as validacoes de formato
# importado por utilizadores.py e artistas.py
# ==============================

from datetime import datetime


def validar_nome(nome):
    if len(nome.strip()) < 2:
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
    try:
        dt = datetime.strptime(data, "%d/%m/%Y")
    except ValueError:
        return False
    if dt.year < 1900 or dt.year > 2025:
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
    if len(pais.strip()) < 2:
        return False
    for c in pais.strip():
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
    if len(genero.strip()) < 2:
        return False
    for c in genero.strip():
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
    if not ano.isdigit():
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
    if len(bio.strip()) < 5:
        return False
    return True


def validar_titulo(titulo):
    if len(titulo.strip()) < 1:
        return False
    return True


def validar_faixa(faixa):
    if len(faixa.strip()) < 1:
        return False
    return True


def validar_escolha(escolha):
    if len(escolha.strip()) < 1:
        return False
    return True


def validar_pesquisa(termo):
    if len(termo.strip()) == 0:
# ==============================
# VALIDAÇÕES PARA musicas.py
# ==============================

def validar_duracao(duracao_ms):
    """Valida duração (deve ser um número inteiro positivo)"""
    try:
        valor = int(duracao_ms)
        return valor > 0
    except (ValueError, TypeError):
        return False


def validar_isrc(isrc):
    """Valida código ISRC (formato: 2 letras + 3 letras + 2 dígitos + 5 dígitos)"""
    if not isinstance(isrc, str):
        return False
    if len(isrc) != 12:
        return False
    # Primeiros 2 caracteres: letras
    if not isrc[0:2].isalpha():
        return False
    # Próximos 3 caracteres: letras
    if not isrc[2:5].isalpha():
        return False
    # Próximos 2 caracteres: dígitos
    if not isrc[5:7].isdigit():
        return False
    # Últimos 5 caracteres: dígitos
    if not isrc[7:12].isdigit():
        return False
    return True


def validar_letra(letra):
    """Valida letra da música (mínimo 5 caracteres)"""
    if len(letra.strip()) < 5:
        return False
    return True


def validar_bitrate(bitrate):
    """Valida bitrate (deve ser 128, 192, 256, 320)"""
    try:
        valor = int(bitrate)
        return valor in [128, 192, 256, 320]
    except (ValueError, TypeError):
        return False


def validar_reproducoes(reproducoes):
    """Valida contagem de reproduções (número inteiro não negativo)"""
    try:
        valor = int(reproducoes)
        return valor >= 0
    except (ValueError, TypeError):
        return False


def validar_booleano(valor):
    """Valida se o valor pode ser convertido para booleano"""
    if isinstance(valor, bool):
        return True
    if isinstance(valor, str):
        if valor.lower() in ["true", "false", "1", "0", "s", "n", "sim", "nao"]:
            return True
    if isinstance(valor, int):
        if valor in [0, 1]:
            return True
    return False


# ==============================
# VALIDAÇÕES PARA playlists.py
# ==============================

def validar_privacidade(privacidade):
    """Valida privacidade da playlist: publica ou privada"""
    if privacidade == "publica":
        return True
    elif privacidade == "privada":
        return True
    else:
        return False


def validar_descricao(descricao):
    """Valida descrição (mínimo 5 caracteres, máximo 500)"""
    if len(descricao.strip()) < 5:
        return False
    if len(descricao) > 500:
        return False
    return True
        return False
    return True
