
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
from utils import (
    validar_nome,
    validar_url,
    validar_pais,
    validar_data,
    validar_generos,
    validar_estado_conta,
    validar_genero,
    validar_verificado,
    validar_biografia,
    validar_ouvintes,
    validar_ano,
    validar_tipo_lancamento,
    validar_titulo,
    validar_faixa,
    validar_pesquisa,
    validar_escolha
)


# ==============================
# HELPERS OBRIGATORIOS (campo nao pode ficar vazio)
# usados no CREATE — pedem o campo ate o utilizador acertar
# ==============================

def pedir_nome(mensagem):
    while True:
        valor = input(mensagem)
        if validar_nome(valor):
            return valor
        print("Erro: Minimo 2 caracteres.")


def pedir_url(mensagem):
    while True:
        valor = input(mensagem)
        if validar_url(valor):
            return valor
        print("Erro: URL invalido. Tem de comecar com http:// ou https://")


def pedir_pais(mensagem):
    while True:
        valor = input(mensagem)
        if validar_pais(valor):
            return valor
        print("Erro: Pais invalido. Nao pode conter numeros.")


def pedir_data(mensagem):
    while True:
        valor = input(mensagem)
        if validar_data(valor):
            return valor
        print("Erro: Data invalida. Use DD/MM/AAAA (ex: 15/03/2000).")


def pedir_generos(mensagem):
    while True:
        valor = input(mensagem)
        if validar_generos(valor):
            return valor
        print("Erro: Generos invalidos. Minimo 2 caracteres por genero.")


def pedir_estado_conta(mensagem):
    while True:
        valor = input(mensagem).lower()
        if validar_estado_conta(valor):
            return valor
        print("Erro: Estado invalido. Opcoes: ativo, inativo, premium.")


def pedir_genero(mensagem):
    while True:
        valor = input(mensagem)
        if validar_genero(valor):
            return valor
        print("Erro: Genero invalido. Nao pode conter numeros.")


def pedir_verificado(mensagem):
    while True:
        valor = input(mensagem).lower()
        if validar_verificado(valor):
            return valor
        print("Erro: Resposta invalida. Use s ou n.")


def pedir_biografia(mensagem):
    while True:
        valor = input(mensagem)
        if validar_biografia(valor):
            return valor
        print("Erro: Biografia demasiado curta. Minimo 5 caracteres.")


def pedir_ouvintes(mensagem):
    while True:
        valor = input(mensagem)
        if validar_ouvintes(valor):
            return valor
        print("Erro: Valor invalido. Introduza um numero positivo.")


def pedir_ano(mensagem):
    while True:
        valor = input(mensagem)
        if validar_ano(valor):
            return valor
        print("Erro: Ano invalido. Use 4 digitos numericos entre 1900 e 2025.")


def pedir_tipo_lancamento(mensagem):
    while True:
        valor = input(mensagem).lower()
        if validar_tipo_lancamento(valor):
            return valor
        print("Erro: Tipo invalido. Opcoes: album, ep, single.")


def pedir_titulo(mensagem):
    while True:
        valor = input(mensagem)
        if validar_titulo(valor):
            return valor
        print("Erro: Titulo nao pode estar vazio.")


def pedir_faixa(mensagem):
    while True:
        valor = input(mensagem)
        if validar_faixa(valor):
            return valor
        print("Erro: Nome da faixa nao pode estar vazio.")


def pedir_pesquisa(mensagem):
    while True:
        valor = input(mensagem)
        if validar_pesquisa(valor):
            return valor
        print("Erro: Introduza um termo para pesquisar.")


# ==============================
# HELPERS OPCIONAIS (enter = manter valor atual)
# usados no UPDATE — retornam None se o utilizador deixar vazio
# ==============================

def pedir_nome_opcional(mensagem):
    valor = input(mensagem).strip()
    if not valor:
        return None
    while not validar_nome(valor):
        print("Erro: Minimo 2 caracteres.")
        valor = input(mensagem).strip()
        if not valor:
            return None
    return valor


def pedir_url_opcional(mensagem):
    valor = input(mensagem).strip()
    if not valor:
        return None
    while not validar_url(valor):
        print("Erro: URL invalido. Tem de comecar com http:// ou https://")
        valor = input(mensagem).strip()
        if not valor:
            return None
    return valor


def pedir_pais_opcional(mensagem):
    valor = input(mensagem).strip()
    if not valor:
        return None
    while not validar_pais(valor):
        print("Erro: Pais invalido. Nao pode conter numeros.")
        valor = input(mensagem).strip()
        if not valor:
            return None
    return valor


def pedir_estado_conta_opcional(mensagem):
    valor = input(mensagem).strip().lower()
    if not valor:
        return None
    while not validar_estado_conta(valor):
        print("Erro: Estado invalido. Opcoes: ativo, inativo, premium.")
        valor = input(mensagem).strip().lower()
        if not valor:
            return None
    return valor


def pedir_generos_opcional(mensagem):
    valor = input(mensagem).strip()
    if not valor:
        return None
    while not validar_generos(valor):
        print("Erro: Generos invalidos. Minimo 2 caracteres por genero.")
        valor = input(mensagem).strip()
        if not valor:
            return None
    return valor


def pedir_genero_opcional(mensagem):
    valor = input(mensagem).strip()
    if not valor:
        return None
    while not validar_genero(valor):
        print("Erro: Genero invalido. Nao pode conter numeros.")
        valor = input(mensagem).strip()
        if not valor:
            return None
    return valor


def pedir_verificado_opcional(mensagem):
    valor = input(mensagem).strip().lower()
    if not valor:
        return None
    while not validar_verificado(valor):
        print("Erro: Resposta invalida. Use s ou n.")
        valor = input(mensagem).strip().lower()
        if not valor:
            return None
    return valor


def pedir_biografia_opcional(mensagem):
    valor = input(mensagem).strip()
    if not valor:
        return None
    while not validar_biografia(valor):
        print("Erro: Biografia demasiado curta. Minimo 5 caracteres.")
        valor = input(mensagem).strip()
        if not valor:
            return None
    return valor


def pedir_ouvintes_opcional(mensagem):
    valor = input(mensagem).strip()
    if not valor:
        return None
    while not validar_ouvintes(valor):
        print("Erro: Valor invalido. Introduza um numero positivo.")
        valor = input(mensagem).strip()
        if not valor:
            return None
    return valor


def pedir_escolha_opcional(mensagem):
    valor = input(mensagem).strip()
    if not valor:
        return None
    while not validar_escolha(valor):
        print("Erro: Escolha nao pode estar vazia.")
        valor = input(mensagem).strip()
        if not valor:
            return None
    return valor


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
            nome      = pedir_nome("Nome de exibicao: ")
            nome_util = pedir_nome("Nome de utilizador (interno): ")
            # nome de exibicao nao pode ser igual ao nome interno
            while nome.lower() == nome_util.lower():
                print("Erro: Nome de exibicao nao pode ser igual ao nome de utilizador.")
                nome_util = pedir_nome("Nome de utilizador (interno): ")
            foto      = pedir_url("URL da foto de perfil: ")
            pais      = pedir_pais("Pais: ")
            data_nasc = pedir_data("Data de nascimento (DD/MM/AAAA): ")
            generos   = pedir_generos("Generos preferidos (separados por virgula): ")
            estado    = pedir_estado_conta("Estado da conta (ativo/inativo/premium): ")
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
            nome = pedir_pesquisa("Nome a pesquisar: ")
            rc = pesquisar_utilizadores(nome)
            if rc[0] == 200:
                for id_u, u in rc[1].items():
                    print(id_u + " | " + u["nome_exibicao"] + " | " + u["nome_utilizador"] + " | " + u["estado_conta"])
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "5":
            id_u    = input("ID do utilizador: ")
            nome    = pedir_nome_opcional("Novo nome (enter para manter): ")
            foto    = pedir_url_opcional("Nova URL da foto (enter para manter): ")
            pais    = pedir_pais_opcional("Novo pais (enter para manter): ")
            estado  = pedir_estado_conta_opcional("Novo estado (enter para manter): ")
            generos = pedir_generos_opcional("Novos generos (enter para manter): ")
            rc = atualizar_utilizador(id_u, nome, foto, pais, estado, generos)
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
            nome        = pedir_nome("Nome do artista: ")
            bio         = pedir_biografia("Biografia: ")
            imagem      = pedir_url("URL da imagem de perfil: ")
            imagem_capa = pedir_url("URL da imagem de capa: ")
            genero      = pedir_genero("Genero musical: ")
            verificado  = pedir_verificado("Artista verificado? (s/n): ")
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
            nome = pedir_pesquisa("Nome a pesquisar: ")
            rc = pesquisar_artistas(nome)
            if rc[0] == 200:
                for id_a, a in rc[1].items():
                    print(id_a + " | " + a["nome"] + " | " + a["genero"])
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "5":
            id_a        = input("ID do artista: ")
            nome        = pedir_nome_opcional("Novo nome (enter para manter): ")
            bio         = pedir_biografia_opcional("Nova biografia (enter para manter): ")
            imagem      = pedir_url_opcional("Nova URL imagem (enter para manter): ")
            imagem_capa = pedir_url_opcional("Nova URL capa (enter para manter): ")
            genero      = pedir_genero_opcional("Novo genero (enter para manter): ")
            verificado  = pedir_verificado_opcional("Verificado s/n (enter para manter): ")
            ouvintes    = pedir_ouvintes_opcional("Ouvintes mensais (enter para manter): ")
            escolha     = pedir_escolha_opcional("Escolha do artista (enter para manter): ")
            rc = atualizar_artista(id_a, nome, bio, imagem, imagem_capa, genero, verificado, ouvintes, escolha)
            if rc[0] == 200:
                print("Artista atualizado com sucesso.")
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "6":
            id_a   = input("ID do artista: ")
            titulo = pedir_titulo("Titulo do lancamento: ")
            tipo   = pedir_tipo_lancamento("Tipo (album/ep/single): ")
            ano    = pedir_ano("Ano (ex: 2023): ")
            rc = adicionar_lancamento(id_a, titulo, tipo, ano)
            if rc[0] == 200:
                print("Lancamento adicionado com sucesso.")
            else:
                print("Erro " + str(rc[0]) + ": " + rc[1])

        elif opcao == "7":
            id_a  = input("ID do artista: ")
            faixa = pedir_faixa("Nome da faixa: ")
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
