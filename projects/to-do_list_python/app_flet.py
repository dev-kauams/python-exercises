import flet as ft


def main(page: ft.Page):
    page.title = "Lista de Tarefas (To-do List)"
    page.vertical_alignment = ft.MainAxisAlignment.START

    campo_tarefa = ft.TextField(
        hint_text="O que você precisa fazer?",
        width=300,
        autofocus=True,
        on_submit=lambda e: adicionar_tarefa(e),
    )
    lista_de_tarefas = ft.Column()

    def remover_tarefa(linha):
        lista_de_tarefas.controls.remove(linha)
        lista_de_tarefas.update()

    def criar_linha(texto):
        checkbox = ft.Checkbox(label=texto)

        linha = ft.Row(
            controls=[
                checkbox,
                ft.IconButton(
                    icon=ft.Icons.DELETE_OUTLINE,
                    icon_color=ft.Colors.RED_400,
                    tooltip="Remover tarefa",
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        linha.controls[1].on_click = lambda e: remover_tarefa(linha)
        return linha

    def adicionar_tarefa(e):
        texto = campo_tarefa.value.strip()

        if texto:
            lista_de_tarefas.controls.append(criar_linha(texto))
            campo_tarefa.value = ""
            campo_tarefa.error_text = None
            lista_de_tarefas.update()
            campo_tarefa.update()
            campo_tarefa.focus()
        else:
            campo_tarefa.error_text = "Digite uma tarefa antes de adicionar"
            campo_tarefa.update()

    botao_adicionar = ft.ElevatedButton("Adicionar", on_click=adicionar_tarefa)
    linha_superior = ft.Row([campo_tarefa, botao_adicionar])

    page.add(linha_superior, lista_de_tarefas)


ft.app(target=main)