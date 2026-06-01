# ==============================
# spotify_online.py
# Integração com API do Spotify (versão online)
# Segue padrão HTTP (200, 400, 401, 404, 500)
# Usa utils.py para logger e validações
# ==============================

import requests
import base64
import json
import os
from datetime import datetime, timedelta
from utils import get_logger

logger = get_logger()

# ==============================
# CONFIGURAÇÃO
# ==============================
# !!! SUBSTITUA PELOS SEUS DADOS DO SPOTIFY DEVELOPER !!!
CLIENT_ID = "a055ccf1e2be4d888a5e14f5e5193461"
CLIENT_SECRET = "9d0df6d5fd854eadbc708dbb690fcc40"

TOKEN_FILE = "spotify_token.json"


# ==============================
# PERSISTÊNCIA DO TOKEN
# ==============================

def _guardar_token(token, expires_in):
    """Guarda o token em ficheiro"""
    dados = {
        "token": token,
        "expires_at": (datetime.now() + timedelta(seconds=expires_in)).isoformat()
    }
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4)
    logger.debug("Token guardado com sucesso")


def _carregar_token():
    """Carrega token do ficheiro"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def _token_valido():
    """Verifica se o token guardado ainda é válido"""
    dados = _carregar_token()
    if not dados:
        return False
    expires_at = datetime.fromisoformat(dados["expires_at"])
    return datetime.now() < expires_at


# ==============================
# AUTENTICAÇÃO
# ==============================

def _obter_token():
    """
    Obtém token de acesso da API do Spotify
    Retorna: (codigo, token ou mensagem_erro)
    """
    # Verificar se já temos token válido
    if _token_valido():
        dados = _carregar_token()
        logger.debug("Token válido reutilizado")
        return 200, dados["token"]

    # Verificar credenciais
    if CLIENT_ID == "SEU_CLIENT_ID_AQUI" or CLIENT_SECRET == "SEU_CLIENT_SECRET_AQUI":
        logger.error("Credenciais do Spotify não configuradas")
        return 401, "Configurar CLIENT_ID e CLIENT_SECRET no ficheiro spotify_online.py"

    # Pedir novo token
    url = "https://accounts.spotify.com/api/token"

    # Criar autenticação Basic
    auth_string = f"{CLIENT_ID}:{CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    try:
        response = requests.post(url, headers=headers, data=data, timeout=10)

        if response.status_code == 200:
            resultado = response.json()
            token = resultado["access_token"]
            expires_in = resultado["expires_in"]

            _guardar_token(token, expires_in)
            logger.info("Token Spotify obtido com sucesso")
            return 200, token
        else:
            logger.error(f"Erro ao obter token: {response.status_code}")
            return response.status_code, f"Erro na autenticação: {response.status_code}"

    except requests.exceptions.Timeout:
        logger.error("Timeout ao obter token Spotify")
        return 500, "Timeout na conexão com Spotify"
    except Exception as e:
        logger.error(f"Erro ao obter token: {e}")
        return 500, f"Erro interno: {str(e)}"


# ==============================
# FUNÇÕES PÚBLICAS (COM CÓDIGOS HTTP)
# ==============================

def pesquisar_musicas(query, limite=10):
    """
    Pesquisa músicas no Spotify
    Retorna: (codigo, dados)
    """
    if not query or len(query.strip()) < 2:
        logger.warning("Termo de pesquisa vazio: " + query)
        return 400, "Termo de pesquisa inválido. Mínimo 2 caracteres"

    code, token = _obter_token()
    if code != 200:
        return code, token

    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": query,
        "type": "track",
        "limit": min(limite, 50),
        "market": "PT"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            dados = response.json()
            items = dados.get("tracks", {}).get("items", [])

            if not items:
                logger.warning(f"Nenhuma música encontrada para: {query}")
                return 404, f"Nenhuma música encontrada para '{query}'"

            musicas = []
            for item in items:
                musicas.append({
                    "id": item["id"],
                    "titulo": item["name"],
                    "artistas": [a["name"] for a in item["artists"]],
                    "artista_principal": item["artists"][0]["name"],
                    "duracao_ms": item["duration_ms"],
                    "preview_url": item.get("preview_url"),
                    "album": item["album"]["name"],
                    "data_lancamento": item["album"]["release_date"],
                    "imagem": item["album"]["images"][0]["url"] if item["album"]["images"] else None,
                    "uri": item["uri"],
                    "url": item["external_urls"]["spotify"]
                })

            logger.info(f"Pesquisa '{query}' retornou {len(musicas)} musicas")
            return 200, musicas
        else:
            logger.error(f"Erro Spotify: {response.status_code}")
            return response.status_code, f"Erro do Spotify: {response.status_code}"

    except requests.exceptions.Timeout:
        logger.error("Timeout na pesquisa")
        return 500, "Timeout na requisição"
    except Exception as e:
        logger.error(f"Erro na pesquisa: {e}")
        return 500, f"Erro interno: {str(e)}"


def pesquisar_artistas(nome, limite=10):
    """
    Pesquisa artistas no Spotify
    Retorna: (codigo, dados)
    """
    if not nome or len(nome.strip()) < 2:
        logger.warning("Nome de artista vazio")
        return 400, "Nome do artista inválido. Mínimo 2 caracteres"

    code, token = _obter_token()
    if code != 200:
        return code, token

    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": nome,
        "type": "artist",
        "limit": min(limite, 50),
        "market": "PT"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            dados = response.json()
            items = dados.get("artists", {}).get("items", [])

            if not items:
                logger.warning(f"Nenhum artista encontrado para: {nome}")
                return 404, f"Nenhum artista encontrado para '{nome}'"

            artistas = []
            for item in items:
                # Tratamento seguro para followers (pode não existir)
                seguidores = 0
                if "followers" in item and item["followers"]:
                    seguidores = item["followers"].get("total", 0)

                artistas.append({
                    "id": item["id"],
                    "nome": item["name"],
                    "seguidores": seguidores,
                    "generos": item.get("genres", [])[:5],
                    "imagem": item["images"][0]["url"] if item.get("images") else None,
                    "uri": item["uri"],
                    "url": item["external_urls"]["spotify"]
                })

            logger.info(f"Pesquisa de artista '{nome}' retornou {len(artistas)} resultados")
            return 200, artistas
        else:
            return response.status_code, f"Erro do Spotify: {response.status_code}"

    except Exception as e:
        logger.error(f"Erro na pesquisa de artista: {e}")
        return 500, str(e)

def get_musicas_artista(artista_id, limite=10):
    """
    Obtém as músicas mais populares de um artista pelo ID
    Retorna: (codigo, lista_de_musicas)
    """
    if not artista_id:
        logger.warning("ID do artista não fornecido")
        return 400, "ID do artista não fornecido"

    code, token = _obter_token()
    if code != 200:
        return code, token

    url = f"https://api.spotify.com/v1/artists/{artista_id}/top-tracks"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"market": "PT", "limit": limite}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            dados = response.json()
            tracks = dados.get("tracks", [])

            if not tracks:
                logger.warning(f"Nenhuma música encontrada para artista {artista_id}")
                return 404, "Nenhuma música encontrada para este artista"

            musicas = []
            for track in tracks[:limite]:
                musicas.append({
                    "id": track["id"],
                    "titulo": track["name"],
                    "duracao_ms": track["duration_ms"],
                    "preview_url": track.get("preview_url"),
                    "album": track["album"]["name"],
                    "imagem": track["album"]["images"][0]["url"] if track["album"]["images"] else None
                })

            logger.info(f"Obtidas {len(musicas)} musicas do artista {artista_id}")
            return 200, musicas
        elif response.status_code == 404:
            logger.warning(f"Artista não encontrado: {artista_id}")
            return 404, "Artista não encontrado"
        else:
            return response.status_code, f"Erro: {response.status_code}"

    except Exception as e:
        logger.error(f"Erro ao buscar músicas do artista: {e}")
        return 500, str(e)


def get_musicas_populares(limite=20):
    """
    Obtém músicas populares do momento
    Retorna: (codigo, lista_de_musicas)
    """
    code, token = _obter_token()
    if code != 200:
        return code, token

    # Buscar músicas populares
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "q": "year:2024",
        "type": "track",
        "limit": min(limite, 10),
        "market": "PT"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            dados = response.json()
            items = dados.get("tracks", {}).get("items", [])

            if not items:
                logger.warning("Não foi possível obter músicas populares")
                return 404, "Não foi possível obter músicas populares"

            musicas = []
            for i, item in enumerate(items, 1):
                musicas.append({
                    "posicao": i,
                    "id": item["id"],
                    "titulo": item["name"],
                    "artista": item["artists"][0]["name"],
                    "preview_url": item.get("preview_url"),
                    "album": item["album"]["name"],
                    "url": item["external_urls"]["spotify"]
                })

            logger.info(f"Obtidas {len(musicas)} musicas populares")
            return 200, musicas
        else:
            return response.status_code, f"Erro ao buscar músicas: {response.status_code}"

    except Exception as e:
        logger.error(f"Erro ao buscar musicas populares: {e}")
        return 500, str(e)


def testar_conexao():
    """
    Testa se a API do Spotify está funcionando
    Retorna: (codigo, mensagem)
    """
    try:
        code, token = _obter_token()
        if code != 200:
            logger.error(f"Falha na autenticacao: {token}")
            return code, token

        url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {token}"}
        params = {
            "q": "Queen",
            "type": "track",
            "limit": 1,
            "market": "PT"
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            logger.info("Teste de conexão Spotify realizado com sucesso")
            return 200, "✅ Conexão com Spotify API funcionando!"
        else:
            logger.error(f"Erro no teste de conexão: {response.status_code}")
            return response.status_code, f"Erro na API: {response.status_code}"

    except requests.exceptions.Timeout:
        logger.error("Timeout no teste de conexão")
        return 500, "Timeout na conexão com Spotify"
    except Exception as e:
        logger.error(f"Erro no teste de conexão: {e}")
        return 500, f"Erro na conexão: {str(e)}"


def obter_imagem_artista(artista_id):
    """
    Obtém a URL da imagem do artista pelo ID
    Retorna: (codigo, url_imagem)
    """
    if not artista_id:
        logger.warning("ID do artista não fornecido")
        return 400, "ID do artista não fornecido"

    code, token = _obter_token()
    if code != 200:
        return code, token

    url = f"https://api.spotify.com/v1/artists/{artista_id}"
    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            dados = response.json()
            imagens = dados.get("images", [])
            if imagens:
                imagem_url = imagens[0]["url"]
                logger.info(f"Imagem obtida para artista {artista_id}")
                return 200, imagem_url
            else:
                logger.warning(f"Artista {artista_id} sem imagem")
                return 404, "Artista sem imagem disponível"
        elif response.status_code == 404:
            logger.warning(f"Artista não encontrado: {artista_id}")
            return 404, "Artista não encontrado"
        else:
            logger.error(f"Erro ao obter imagem: {response.status_code}")
            return response.status_code, f"Erro na API: {response.status_code}"

    except requests.exceptions.Timeout:
        logger.error("Timeout ao obter imagem")
        return 500, "Timeout na conexão"
    except Exception as e:
        logger.error(f"Erro ao obter imagem: {e}")
        return 500, str(e)


# ==============================
# TESTE DIRETO (opcional)
# ==============================

if __name__ == "__main__":
    print("=" * 50)
    print("🎵 TESTE DA API SPOTIFY ONLINE")
    print("=" * 50)

    print("\n📡 A testar conexão...")

    code, msg = testar_conexao()
    print(f"\n📡 Resultado: [{code}] {msg}")

    if code == 200:
        print("\n🔍 Teste 1: Pesquisando 'Bohemian Rhapsody'...")
        code2, musicas = pesquisar_musicas("Bohemian Rhapsody", 3)

        if code2 == 200:
            print(f"   ✅ Encontrou {len(musicas)} música(s):")
            for m in musicas:
                print(f"      🎵 {m['titulo']} - {m['artista_principal']}")
        else:
            print(f"   ⚠️ Erro: {musicas}")

        print("\n🌍 Teste 2: Buscando Músicas Populares...")
        code3, top = get_musicas_populares(5)

        if code3 == 200:
            print(f"   ✅ Top 5 músicas:")
            for t in top:
                print(f"      #{t['posicao']} {t['titulo']} - {t['artista']}")
        else:
            print(f"   ⚠️ Erro: {top}")

        print("\n🎤 Teste 3: Pesquisando 'Queen'...")
        code4, artistas = pesquisar_artistas("Queen", 2)

        if code4 == 200:
            print(f"   ✅ Encontrou {len(artistas)} artista(s):")
            for a in artistas:
                seguidores = f"{a['seguidores']:,}" if a['seguidores'] else "N/A"
                print(f"      🎤 {a['nome']} - {seguidores} seguidores")
        else:
            print(f"   ⚠️ Erro: {artistas}")

    print("\n" + "=" * 50)
    print("✅ Teste concluído!")
    print("=" * 50)