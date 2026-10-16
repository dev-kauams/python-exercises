import os
import sqlite3


class SaborExpress:

    def __init__(self, caminho_banco="restaurantes.db"):
        self.caminho_banco = caminho_banco
        self.inicializar_banco()

    def inicializar_banco(self):
        conn = sqlite3.connect(self.caminho_banco)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS restaurantes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                categoria TEXT NOT NULL,
                ativo BOOLEAN NOT NULL DEFAULT 0
            )
            """
        )

        cursor.execute("SELECT COUNT(*) FROM restaurantes")
        total = cursor.fetchone()[0]

        if total == 0:
            restaurantes_iniciais = [
                ("Praça", "Japonesa", False),
                ("Pizza Suprema", "Pizza", True),
                ("Cantina", "Italiano", False),
            ]
            cursor.executemany(
                "INSERT INTO restaurantes (nome, categoria, ativo) VALUES (?, ?, ?)",
                restaurantes_iniciais,
            )
            conn.commit()

        conn.close()  # Movido para fora do IF para fechar sempre

    def cadastrar_restaurante(self, nome, categoria):
        try:
            conn = sqlite3.connect(self.caminho_banco)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO restaurantes (nome, categoria, ativo) VALUES (?, ?, ?)",
                (nome, categoria, False),
            )

            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as erro:
            print(f"Erro ao cadastrar restaurante: {erro}")
            return False

    def buscar_estado(self, nome):
        conn = sqlite3.connect(self.caminho_banco)
        cursor = conn.cursor()

        cursor.execute("SELECT ativo FROM restaurantes WHERE nome = ?", (nome,))
        resultado = cursor.fetchone()

        conn.close()
        return resultado[0] if resultado is not None else None

    def alternar_estado(self, nome):
        estado_atual = self.buscar_estado(nome)

        if estado_atual is None:
            return None

        novo_estado = not estado_atual

        conn = sqlite3.connect(self.caminho_banco)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE restaurantes SET ativo = ? WHERE nome = ?",
            (novo_estado, nome),
        )

        conn.commit()
        conn.close()

        return novo_estado

    def listar_restaurantes(self):
        conn = sqlite3.connect(self.caminho_banco)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT nome, categoria, ativo FROM restaurantes ORDER BY nome"
        )
        restaurantes = cursor.fetchall()

        conn.close()
        return restaurantes

    def restaurante_existe(self, nome):
        conn = sqlite3.connect(self.caminho_banco)
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM restaurantes WHERE nome = ?", (nome,))
        resultado = cursor.fetchone()

        conn.close()
        return resultado is not None

    def excluir_restaurante(self, nome):
        conn = sqlite3.connect(self.caminho_banco)
        cursor = conn.cursor()

        # Corrigido de SELECT para DELETE
        cursor.execute("DELETE FROM restaurantes WHERE nome = ?", (nome,))

        conn.commit()
        conn.close()


class Menu:

    def __init__(self):
        self.app = SaborExpress()

    def exibir_subtitulo(self, texto):
        os.system("cls" if os.name == "nt" else "clear")
        linha = "*" * len(texto)
        print(linha)
        print(texto)
        print(linha)
        print()

    def exibir_nome_do_programa(self):
        print(
            """
        𝕊𝕒𝕓𝕠𝕣 𝕖𝕩𝕡𝕣𝕖𝕤𝕤
        """
        )

    def exibir_opcoes(self):
        print("1. Cadastrar restaurante")
        print("2. Listar restaurante")
        print("3. Alternar estado do restaurante")
        print("4. Excluir restaurante")
        print("5. Sair\n")

    def cadastrar_novo_restaurante(self):
        self.exibir_subtitulo("Cadastro de novos restaurantes\n")
        nome = input("Digite o nome do restaurante: ")
        # Adicionado o prefixo 'f' na string abaixo
        categoria = input(f"Informe a categoria do restaurante {nome}: ")

        sucesso = self.app.cadastrar_restaurante(nome, categoria)

        if sucesso:
            print(f"O restaurante {nome} foi cadastrado com sucesso!")
        else:
            print(f"Erro ao cadastrar o restaurante {nome}.")

        self.voltar_ao_menu_principal()

    def alternar_estado_do_restaurante(self):
        self.exibir_subtitulo("Alternando estado do restaurante\n")
        nome = input(
            "Digite o nome do restaurante que deseja alternar o estado: "
        )

        novo_estado = self.app.alternar_estado(nome)

        if novo_estado is None:
            print("O restaurante não foi encontrado.")
        else:
            status = "ativado" if novo_estado else "desativado"
            print(f"O restaurante {nome} foi {status} com sucesso!")

        self.voltar_ao_menu_principal()

    def excluir_restaurante(self):
        self.exibir_subtitulo("Excluir restaurante\n")

        restaurantes = self.app.listar_restaurantes()

        if not restaurantes:
            print("Nenhum restaurante cadastrado para excluir.")
            self.voltar_ao_menu_principal()
            return

        print("Restaurantes cadastrados:")
        print("-" * 40)
        for nome, categoria, _ in restaurantes:
            print(f"• {nome} ({categoria})")
        print()

        nome = input("Digite o nome do restaurante que deseja excluir: ")

        if self.app.restaurante_existe(nome):
            confirmacao = input(
                f'Tem certeza que deseja excluir o restaurante "{nome}"? (s/n): '
            )

            if confirmacao.lower() == "s":
                self.app.excluir_restaurante(nome)
                print(f"O restaurante {nome} foi excluído com sucesso!")
            else:
                print("Exclusão cancelada.")
        else:
            print("O restaurante não foi encontrado!")

        self.voltar_ao_menu_principal()

    def listar_restaurantes(self):
        self.exibir_subtitulo("Listando os restaurantes\n")

        restaurantes = self.app.listar_restaurantes()

        if restaurantes:
            print(
                f"{'Nome do Restaurante'.ljust(21)} | {'Categoria'.ljust(20)} | Status"
            )
            print("-" * 65)

            for nome, categoria, ativo in restaurantes:
                status = "ativado" if ativo else "desativado"
                print(f"{nome.ljust(21)} | {categoria.ljust(20)} | {status}")
        else:
            print("Nenhum restaurante cadastrado.")

        self.voltar_ao_menu_principal()

    def finalizar_app(self):
        self.exibir_subtitulo("Finalizando o app\n")

    def opcao_invalida(self):
        print("Opção inválida!\n")
        self.voltar_ao_menu_principal()

    def voltar_ao_menu_principal(self):
        input("\nPressione Enter para voltar ao menu principal")
        self.main()

    def escolher_opcao(self):
        try:
            opcao_escolhida = int(input("Escolha uma opção: "))

            if opcao_escolhida == 1:
                self.cadastrar_novo_restaurante()
            elif opcao_escolhida == 2:
                self.listar_restaurantes()
            elif opcao_escolhida == 3:
                self.alternar_estado_do_restaurante()
            elif opcao_escolhida == 4:
                self.excluir_restaurante()
            elif opcao_escolhida == 5:
                self.finalizar_app()
            else:
                self.opcao_invalida()
        except ValueError:
            self.opcao_invalida()

    def main(self):
        os.system("cls" if os.name == "nt" else "clear")
        self.exibir_nome_do_programa()
        self.exibir_opcoes()
        self.escolher_opcao()


if __name__ == "__main__":
    menu = Menu()
    menu.main()