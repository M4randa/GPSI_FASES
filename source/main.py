# ==============================
# main.py
# menu terminal para testar CRUD
# todos os inputs e prints estao aqui
# NAO importa utils
# ==============================

from utilizadores import (
    criar_utilizador,
    listar_utilizadores,
    consultar_utilizador,
    pesquisar_utilizadores,
    atualizar_utilizador,
    remover_utilizador,
    unfollow_artista
)
from artistas import (
    criar_artista,
    listar_artistas,
    consultar_artista,
    pesquisar_artistas,
    atualizar_artista,
    adicionar_lancamento,
    adicionar_top_faixa,
    remover_artista,
    seguir_artista
)
from musica import (
    criar_musica,
    listar_musicas,
    consultar_musica,
    pesquisar_musicas,
    atualizar_musica,
    remover_musica
)
from Playlist import (
    criar_playlist,
    listar_playlists,
    consultar_playlist,
    atualizar_playlist,
    adicionar_musica_playlist,
    remover_musica_playlist,
    remover_playlist,
    seguir_playlist
)

# ==============================
# MENUS
# ==============================

def menu_utilizadores():
    while True:
        print("\n===== MENU UTILIZADORES =====")
        print("1 - Criar utilizador")
        print("2 - Listar utilizadores")
        print("3 - Consultar utilizador")
        print("4 - Pesquisar por nome")
        print("5 - Atualizar utilizador")
        print("6 - Remover utilizador")
        print("7 - Deixar de seguir artista")
        print("0 - Voltar")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            nome      = input("Nome de exibicao: ")
            nome_util = input("Nome de utilizador (interno): ")
            foto      = input("URL da foto de perfil: ")
            pais      = input("Pais: ")
            data_nasc = input("Data de nascimento (DD/MM/AAAA): ")
            generos   = input("Generos preferidos (separados por virgula): ")
            estado    = input("Estado da conta (ativo/inativo/premium): ").lower()
            code, obj = criar_utilizador(nome, nome_util, foto, pais, data_nasc, generos, estado)
            if code == 201:
                print(code)
            else:
                print(obj)

        elif opcao == "2":
            code, obj = listar_utilizadores()
            if code == 200:
                for id_u, u in obj.items():
                    print(id_u + " | " + u["nome_exibicao"] + " | " + u["nome_utilizador"] + " | " + u["estado_conta"] + " | " + u["pais"])
                print(code)
            else:
                print(obj)

        elif opcao == "3":
            id_u = input("ID do utilizador: ")
            code, obj = consultar_utilizador(id_u)
            if code == 200:
                print("\n  ID               : " + obj["id_utilizador"])
                print("  Nome de Exibicao : " + obj["nome_exibicao"])
                print("  Username         : " + obj["nome_utilizador"])
                print("  Foto de Perfil   : " + obj["foto_perfil"])
                print("  Pais             : " + obj["pais"])
                print("  Nascimento       : " + obj["data_nascimento"])
                print("  Generos          : " + ", ".join(obj["generos_preferidos"]))
                print("  Data de Registo  : " + obj["data_registro"])
                print("  Estado da Conta  : " + obj["estado_conta"])
                print("  Seguidores       : " + str(len(obj["seguidores"])))
                print("  Seguindo         : " + str(len(obj["seguidos"])))
                if len(obj["seguidos"]) > 0:
                    print("  Artistas seguidos: " + ", ".join(obj["seguidos"]))
                print(code)
            else:
                print(obj)

        elif opcao == "4":
            nome = input("Nome a pesquisar: ")
            code, obj = pesquisar_utilizadores(nome)
            if code == 200:
                for id_u, u in obj.items():
                    print(id_u + " | " + u["nome_exibicao"] + " | " + u["nome_utilizador"] + " | " + u["estado_conta"])
                print(code)
            else:
                print(obj)

        elif opcao == "5":
            id_u    = input("ID do utilizador: ")
            nome    = input("Novo nome (enter para manter): ")
            foto    = input("Nova URL da foto (enter para manter): ")
            pais    = input("Novo pais (enter para manter): ")
            estado  = input("Novo estado (enter para manter): ").lower()
            generos = input("Novos generos (enter para manter): ")
            code, obj = atualizar_utilizador(
                id_u,
                nome    if nome    else None,
                foto    if foto    else None,
                pais    if pais    else None,
                estado  if estado  else None,
                generos if generos else None
            )
            if code == 200:
                print(code)
            else:
                print(obj)

        elif opcao == "6":
            id_u = input("ID do utilizador: ")
            code, obj = remover_utilizador(id_u)
            if code == 200:
                print(code)
            else:
                print(obj)

        elif opcao == "7":
            id_u = input("ID do utilizador: ")
            id_a = input("ID do artista a deixar de seguir: ")
            code, obj = unfollow_artista(id_u, id_a)
            if code == 200:
                print(code)
            else:
                print(obj)

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")
# ==============================
# MENU MUSICAS
# ==============================

def menu_musicas():
    while True:
        print("\n===== MENU MUSICAS =====")
        print("1 - Criar musica")
        print("2 - Listar musicas")
        print("3 - Consultar musica")
        print("4 - Pesquisar por titulo")
        print("5 - Atualizar musica")
        print("6 - Remover musica")
        print("0 - Voltar")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            titulo = input("Titulo da musica: ")
            id_artista = input("ID do artista: ")
            duracao_ms = input("Duracao (em milissegundos): ")
            isrc = input("Codigo ISRC (12 caracteres): ")
            data_lancamento = input("Data de lancamento (DD/MM/AAAA): ")
            letra = input("Letra da musica: ")
            bitrate = input("Bitrate (128/192/256/320): ")
            flag_explicito = input("Conteudo explicito? (true/false): ").lower()
            status_takedown = input("Status takedown? (true/false): ").lower()
            disponibilidade = input("Disponivel? (true/false): ").lower()
            code, obj = criar_musica(titulo, id_artista, duracao_ms, isrc, data_lancamento, letra, bitrate, flag_explicito, status_takedown, disponibilidade)
            if code == 201:
                print("Musica criada com sucesso! ID: " + obj["id_musica"])
            else:
                print(obj)

        elif opcao == "2":
            code, obj = listar_musicas()
            if code == 200:
                print("\nLISTA DE MUSICAS:")
                for id_m, m in obj.items():
                    explicito = "Sim" if m["flag_explicito"] else "Nao"
                    disponivel = "Sim" if m["disponibilidade"] else "Nao"
                    print("   " + id_m + " | " + m["titulo"] + " | " + m["id_artista"] + " | " + str(m["duracao_ms"]) + "ms | Explicito: " + explicito + " | Disponivel: " + disponivel)
                print("\nCodigo: 200")
            else:
                print(obj)

        elif opcao == "3":
            id_m = input("ID da musica: ")
            code, obj = consultar_musica(id_m)
            if code == 200:
                explicito = "Sim" if obj["flag_explicito"] else "Nao"
                takedown = "Sim" if obj["status_takedown"] else "Nao"
                disponivel = "Sim" if obj["disponibilidade"] else "Nao"
                print("\nDETALHES DA MUSICA:")
                print("   ID                  : " + obj["id_musica"])
                print("   Titulo              : " + obj["titulo"])
                print("   ID Artista          : " + obj["id_artista"])
                print("   Duracao             : " + str(obj["duracao_ms"]) + " ms")
                print("   ISRC                : " + obj["isrc"])
                print("   Data Lancamento     : " + obj["data_lancamento"])
                print("   Letra               : " + obj["letra"])
                print("   Bitrate             : " + str(obj["bitrate"]))
                print("   Reproducoes         : " + str(obj["contagem_reproducoes"]))
                print("   Conteudo Explicito  : " + explicito)
                print("   Status Takedown     : " + takedown)
                print("   Disponibilidade     : " + disponivel)
                print("\nCodigo: 200")
            else:
                print(obj)

        elif opcao == "4":
            nome = input("Titulo a pesquisar: ")
            code, obj = pesquisar_musicas(nome)
            if code == 200:
                print("\nRESULTADOS DA PESQUISA:")
                for id_m, m in obj.items():
                    print("   " + id_m + " | " + m["titulo"] + " | " + m["id_artista"])
                print("\nCodigo: 200")
            else:
                print(obj)

        elif opcao == "5":
            id_m = input("ID da musica: ")
            titulo = input("Novo titulo (enter para manter): ")
            duracao_ms = input("Nova duracao (enter para manter): ")
            letra = input("Nova letra (enter para manter): ")
            bitrate = input("Novo bitrate (enter para manter): ")
            flag_explicito = input("Conteudo explicito? (enter para manter): ").lower()
            disponibilidade = input("Disponivel? (enter para manter): ").lower()
            code, obj = atualizar_musica(
                id_m,
                titulo if titulo else None,
                duracao_ms if duracao_ms else None,
                letra if letra else None,
                bitrate if bitrate else None,
                flag_explicito if flag_explicito else None,
                disponibilidade if disponibilidade else None
            )
            if code == 200:
                print("Musica atualizada com sucesso!")
            else:
                print(obj)

        elif opcao == "6":
            id_m = input("ID da musica: ")
            code, obj = remover_musica(id_m)
            if code == 200:
                print("Musica removida com sucesso!")
            else:
                print(obj)

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")


def menu_artistas():
    while True:
        print("\n===== MENU ARTISTAS =====")
        print("1 - Criar artista")
        print("2 - Listar artistas")
        print("3 - Consultar artista")
        print("4 - Pesquisar por nome")
        print("5 - Atualizar artista")
        print("6 - Adicionar lancamento a discografia")
        print("7 - Adicionar faixa ao top")
        print("8 - Remover artista")
        print("9 - Utilizador seguir artista")
        print("0 - Voltar")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            nome        = input("Nome do artista: ")
            bio         = input("Biografia: ")
            imagem      = input("URL da imagem de perfil: ")
            imagem_capa = input("URL da imagem de capa: ")
            genero      = input("Genero musical: ")
            verificado  = input("Artista verificado? (s/n): ").lower()
            code, obj = criar_artista(nome, bio, imagem, imagem_capa, genero, verificado)
            if code == 201:
                print(code)
            else:
                print(obj)

        elif opcao == "2":
            code, obj = listar_artistas()
            if code == 200:
                for id_a, a in obj.items():
                    verificado_str = "Sim" if a["verificado"] else "Nao"
                    print(id_a + " | " + a["nome"] + " | " + a["genero"] + " | " + str(a["ouvintes_mensais"]) + " ouvintes | Verificado: " + verificado_str)
                print(code)
            else:
                print(obj)

        elif opcao == "3":
            id_a = input("ID do artista: ")
            code, obj = consultar_artista(id_a)
            if code == 200:
                verificado_str = "Sim" if obj["verificado"] else "Nao"
                print("\n  ID               : " + obj["id_artista"])
                print("  Nome             : " + obj["nome"])
                print("  Genero           : " + obj["genero"])
                print("  Verificado       : " + verificado_str)
                print("  Biografia        : " + obj["bio"])
                print("  Ouvintes Mensais : " + str(obj["ouvintes_mensais"]))
                print("  Seguidores       : " + str(len(obj["seguidores"])))
                print("  Discografia      : " + str(len(obj["discografia"])) + " lancamento(s)")
                print("  Top Faixas       : " + str(len(obj["top_faixas"])) + " faixa(s)")
                print("  Escolha Artista  : " + (obj["escolha_artista"] if obj["escolha_artista"] else "Nao definido"))
                if len(obj["discografia"]) > 0:
                    print("\n  --- Discografia ---")
                    for d in obj["discografia"]:
                        print("    " + d["tipo"].upper() + " | " + d["titulo"] + " (" + d["ano"] + ")")
                print(code)
            else:
                print(obj)

        elif opcao == "4":
            nome = input("Nome a pesquisar: ")
            code, obj = pesquisar_artistas(nome)
            if code == 200:
                for id_a, a in obj.items():
                    print(id_a + " | " + a["nome"] + " | " + a["genero"])
                print(code)
            else:
                print(obj)

        elif opcao == "5":
            id_a        = input("ID do artista: ")
            nome        = input("Novo nome (enter para manter): ")
            bio         = input("Nova biografia (enter para manter): ")
            imagem      = input("Nova URL imagem (enter para manter): ")
            imagem_capa = input("Nova URL capa (enter para manter): ")
            genero      = input("Novo genero (enter para manter): ")
            verificado  = input("Verificado s/n (enter para manter): ").lower()
            ouvintes    = input("Ouvintes mensais (enter para manter): ")
            escolha     = input("Escolha do artista (enter para manter): ")
            code, obj = atualizar_artista(
                id_a,
                nome        if nome        else None,
                bio         if bio         else None,
                imagem      if imagem      else None,
                imagem_capa if imagem_capa else None,
                genero      if genero      else None,
                verificado  if verificado  else None,
                ouvintes    if ouvintes    else None,
                escolha     if escolha     else None
            )
            if code == 200:
                print(code)
            else:
                print(obj)

        elif opcao == "6":
            id_a   = input("ID do artista: ")
            titulo = input("Titulo do lancamento: ")
            tipo   = input("Tipo (album/ep/single): ").lower()
            ano    = input("Ano (ex: 2023): ")
            code, obj = adicionar_lancamento(id_a, titulo, tipo, ano)
            if code == 200:
                print(code)
            else:
                print(obj)

        elif opcao == "7":
            id_a  = input("ID do artista: ")
            faixa = input("Nome da faixa: ")
            code, obj = adicionar_top_faixa(id_a, faixa)
            if code == 200:
                print(code)
            else:
                print(obj)

        elif opcao == "8":
            id_a = input("ID do artista: ")
            code, obj = remover_artista(id_a)
            if code == 200:
                print(code)
            else:
                print(obj)

        elif opcao == "9":
            id_u = input("ID do utilizador: ")
            id_a = input("ID do artista: ")
            code, obj = seguir_artista(id_u, id_a)
            if code == 200:
                print(code)
            else:
                print(obj)

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")
def menu_playlists():
    while True:
        print("\n===== MENU PLAYLISTS =====")
        print("1 - Criar playlist")
        print("2 - Listar playlists")
        print("3 - Consultar playlist")
        print("4 - Atualizar playlist")
        print("5 - Adicionar musica a playlist")
        print("6 - Remover musica da playlist")
        print("7 - Remover playlist")
        print("8 - Utilizador seguir playlist")
        print("0 - Voltar")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            nome_playlist = input("Nome da playlist: ")
            id_utilizador = input("ID do utilizador: ")
            privacidade = input("Privacidade (publica/privada): ").lower()
            descricao = input("Descricao: ")
            capa_playlist = input("URL da capa da playlist: ")
            code, obj = criar_playlist(nome_playlist, id_utilizador, privacidade, descricao, capa_playlist)
            if code == 201:
                print("Playlist criada com sucesso! ID: " + obj["id_playlist"])
            else:
                print(obj)

        elif opcao == "2":
            code, obj = listar_playlists()
            if code == 200:
                print("\nLISTA DE PLAYLISTS:")
                for id_p, p in obj.items():
                    print("   " + id_p + " | " + p["nome_playlist"] + " | " + p["id_utilizador"] + " | " + p["privacidade"] + " | " + p["data_criacao"])
                print("\nCodigo: 200")
            else:
                print(obj)

        elif opcao == "3":
            id_p = input("ID da playlist: ")
            code, obj = consultar_playlist(id_p)
            if code == 200:
                print("\nDETALHES DA PLAYLIST:")
                print("   ID Playlist        : " + obj["id_playlist"])
                print("   Nome               : " + obj["nome_playlist"])
                print("   ID Utilizador      : " + obj["id_utilizador"])
                print("   Privacidade        : " + obj["privacidade"])
                print("   Descricao          : " + obj["descricao"])
                print("   Capa               : " + obj["capa_playlist"])
                print("   Data Criacao       : " + obj["data_criacao"])
                print("   Seguidores         : " + str(len(obj["seguidores_playlist"])))
                print("   Total de Musicas   : " + str(len(obj["lista_ids"])))
                print("   Flag Remocao       : " + str(obj["flag_remocao"]))
                if len(obj["lista_ids"]) > 0:
                    print("\n   --- MUSICAS NA PLAYLIST ---")
                    for id_m in obj["lista_ids"]:
                        print("     " + id_m)
                if len(obj["seguidores_playlist"]) > 0:
                    print("\n   --- SEGUIDORES ---")
                    for seguidor in obj["seguidores_playlist"]:
                        print("     " + seguidor)
                print("\nCodigo: 200")
            else:
                print(obj)

        elif opcao == "4":
            id_p = input("ID da playlist: ")
            nome = input("Novo nome (enter para manter): ")
            privacidade = input("Nova privacidade (enter para manter): ").lower()
            descricao = input("Nova descricao (enter para manter): ")
            flag_remocao = input("Flag de remocao (true/false) (enter para manter): ").lower()
            code, obj = atualizar_playlist(
                id_p,
                nome if nome else None,
                privacidade if privacidade else None,
                descricao if descricao else None,
                flag_remocao if flag_remocao else None
            )
            if code == 200:
                print("Playlist atualizada com sucesso!")
            else:
                print(obj)

        elif opcao == "5":
            id_p = input("ID da playlist: ")
            id_m = input("ID da musica: ")
            code, obj = adicionar_musica_playlist(id_p, id_m)
            if code == 200:
                print("Musica adicionada a playlist com sucesso!")
            else:
                print(obj)

        elif opcao == "6":
            id_p = input("ID da playlist: ")
            id_m = input("ID da musica: ")
            code, obj = remover_musica_playlist(id_p, id_m)
            if code == 200:
                print("Musica removida da playlist com sucesso!")
            else:
                print(obj)

        elif opcao == "7":
            id_p = input("ID da playlist: ")
            code, obj = remover_playlist(id_p)
            if code == 200:
                print("Playlist removida com sucesso!")
            else:
                print(obj)

        elif opcao == "8":
            id_u = input("ID do utilizador: ")
            id_p = input("ID da playlist: ")
            code, obj = seguir_playlist(id_u, id_p)
            if code == 200:
                print("Utilizador passou a seguir a playlist!")
            else:
                print(obj)

        elif opcao == "0":
            break
        else:
            print("Opcao invalida.")


# ==============================
# PROGRAMA PRINCIPAL
# ==============================

def main():
    print("\n===== SPOTIFY MANAGER =====")
    print("Abel Chongolola | GPSI 10A | N 01")

    while True:
        print("\n===== MENU PRINCIPAL =====")
        print("1 - Gestao de Utilizadores")
        print("2 - Gestao de Artistas")
        print("3 - Gestao de Musicas")
        print("4 - Gestao de Playlists")
        print("0 - Sair")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            menu_utilizadores()
        elif opcao == "2":
            menu_artistas()
        elif opcao == "3":
            menu_musicas()
        elif opcao == "4":
            menu_playlists()
        elif opcao == "0":
            print("A sair...")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()






