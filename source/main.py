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
        print("0 - Sair")

        opcao = input("Escolha uma opcao: ")

        if opcao == "1":
            menu_utilizadores()
        elif opcao == "2":
            menu_artistas()
        elif opcao == "0":
            print("A sair...")
            break
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()
