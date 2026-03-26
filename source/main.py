
from utilizadores import menu_utilizadores, carregar_utilizadores
from artistas     import menu_artistas, carregar_artistas


# ================================================================
#  FUNCAO MAIN
# ================================================================

def main():
    print("""
+------------------------------------------+
|     SISTEMA CRUD - SPOTIFY MANAGER       |
|   Abel Chongolola | GPSI 10A | N 01      |
+------------------------------------------+
""")

    # Carregamos os dados persistidos dos ficheiros JSON ao arrancar
    # Se os ficheiros nao existirem, comecamos com dados vazios
    print("A carregar dados...")
    carregar_utilizadores()
    carregar_artistas()
    print("")

    opcoes = {
        "1": menu_utilizadores,  # toda a logica de utilizadores esta em utilizadores.py
        "2": menu_artistas,      # toda a logica de artistas esta em artistas.py
    }

    while True:
        print("""
+------------------------------+
|        MENU PRINCIPAL        |
+------------------------------+
|  1. Gestao de Utilizadores   |
|  2. Gestao de Artistas       |
|  0. Sair                     |
+------------------------------+""")

        op = input("Opcao: ").strip()

        if op == "0":
            # Dados ja foram guardados automaticamente apos cada operacao
            print("\nDados guardados. Ate logo!\n")
            break
        elif op in opcoes:
            opcoes[op]()
        else:
            print("Opcao invalida.")


if __name__ == "__main__":
    main()
