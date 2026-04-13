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
            rc = criar_utilizador(nome, nome_util, foto, pais, data_nasc, generos, estado)
            if rc[0] == 201:
                print("Utilizador criado com sucesso. ID: " + rc[1])
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "2":
            rc = listar_utilizadores()
            if rc[0] == 200:
                for id_u, u in rc[1].items():
                    print(id_u + " | " + u["nome_exibicao"] + " | " + u["nome_utilizador"] + " | " + u["estado_conta"] + " | " + u["pais"])
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "3":
            id_u = input("ID do utilizador: ")
            rc = consultar_utilizador(id_u)
            if rc[0] == 200:
                u = rc[1]
                print("\n  ID               : " + u["id_utilizador"])
                print("  Nome de Exibicao : " + u["nome_exibicao"])
                print("  Username         : " + u["nome_utilizador"])
                print("  Foto de Perfil   : " + u["foto_perfil"])
                print("  Pais             : " + u["pais"])
                print("  Nascimento       : " + u["data_nascimento"])
                print("  Generos          : " + ", ".join(u["generos_preferidos"]))
                print("  Data de Registo  : " + u["data_registro"])
                print("  Estado da Conta  : " + u["estado_conta"])
                print("  Seguidores       : " + str(len(u["seguidores"])))
                print("  Seguindo         : " + str(len(u["seguidos"])))
                if len(u["seguidos"]) > 0:
                    print("  Artistas seguidos: " + ", ".join(u["seguidos"]))
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "4":
            nome = input("Nome a pesquisar: ")
            rc = pesquisar_utilizadores(nome)
            if rc[0] == 200:
                for id_u, u in rc[1].items():
                    print(id_u + " | " + u["nome_exibicao"] + " | " + u["nome_utilizador"] + " | " + u["estado_conta"])
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "5":
            id_u    = input("ID do utilizador: ")
            nome    = input("Novo nome (enter para manter): ")
            foto    = input("Nova URL da foto (enter para manter): ")
            pais    = input("Novo pais (enter para manter): ")
            estado  = input("Novo estado (enter para manter): ").lower()
            generos = input("Novos generos (enter para manter): ")
            rc = atualizar_utilizador(
                id_u,
                nome    if nome    else None,
                foto    if foto    else None,
                pais    if pais    else None,
                estado  if estado  else None,
                generos if generos else None
            )
            if rc[0] == 200:
                print("Utilizador atualizado com sucesso.")
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "6":
            id_u = input("ID do utilizador: ")
            rc = remover_utilizador(id_u)
            if rc[0] == 200:
                print("Utilizador removido com sucesso.")
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "7":
            id_u = input("ID do utilizador: ")
            id_a = input("ID do artista a deixar de seguir: ")
            rc = unfollow_artista(id_u, id_a)
            if rc[0] == 200:
                print("Deixou de seguir o artista com sucesso.")
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

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
            rc = criar_artista(nome, bio, imagem, imagem_capa, genero, verificado)
            if rc[0] == 201:
                print("Artista criado com sucesso. ID: " + rc[1])
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "2":
            rc = listar_artistas()
            if rc[0] == 200:
                for id_a, a in rc[1].items():
                    verificado_str = "Sim" if a["verificado"] else "Nao"
                    print(id_a + " | " + a["nome"] + " | " + a["genero"] + " | " + str(a["ouvintes_mensais"]) + " ouvintes | Verificado: " + verificado_str)
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "3":
            id_a = input("ID do artista: ")
            rc = consultar_artista(id_a)
            if rc[0] == 200:
                a = rc[1]
                verificado_str = "Sim" if a["verificado"] else "Nao"
                print("\n  ID               : " + a["id_artista"])
                print("  Nome             : " + a["nome"])
                print("  Genero           : " + a["genero"])
                print("  Verificado       : " + verificado_str)
                print("  Biografia        : " + a["bio"])
                print("  Ouvintes Mensais : " + str(a["ouvintes_mensais"]))
                print("  Seguidores       : " + str(len(a["seguidores"])))
                print("  Discografia      : " + str(len(a["discografia"])) + " lancamento(s)")
                print("  Top Faixas       : " + str(len(a["top_faixas"])) + " faixa(s)")
                print("  Escolha Artista  : " + (a["escolha_artista"] if a["escolha_artista"] else "Nao definido"))
                if len(a["discografia"]) > 0:
                    print("\n  --- Discografia ---")
                    for d in a["discografia"]:
                        print("    " + d["tipo"].upper() + " | " + d["titulo"] + " (" + d["ano"] + ")")
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "4":
            nome = input("Nome a pesquisar: ")
            rc = pesquisar_artistas(nome)
            if rc[0] == 200:
                for id_a, a in rc[1].items():
                    print(id_a + " | " + a["nome"] + " | " + a["genero"])
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

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
            rc = atualizar_artista(
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
            if rc[0] == 200:
                print("Artista atualizado com sucesso.")
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "6":
            id_a   = input("ID do artista: ")
            titulo = input("Titulo do lancamento: ")
            tipo   = input("Tipo (album/ep/single): ").lower()
            ano    = input("Ano (ex: 2023): ")
            rc = adicionar_lancamento(id_a, titulo, tipo, ano)
            if rc[0] == 200:
                print("Lancamento adicionado com sucesso.")
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "7":
            id_a  = input("ID do artista: ")
            faixa = input("Nome da faixa: ")
            rc = adicionar_top_faixa(id_a, faixa)
            if rc[0] == 200:
                print("Faixa adicionada ao top com sucesso.")
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "8":
            id_a = input("ID do artista: ")
            rc = remover_artista(id_a)
            if rc[0] == 200:
                print("Artista removido com sucesso.")
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "9":
            id_u = input("ID do utilizador: ")
            id_a = input("ID do artista: ")
            rc = seguir_artista(id_u, id_a)
            if rc[0] == 200:
                print("Utilizador agora segue o artista.")
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

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
