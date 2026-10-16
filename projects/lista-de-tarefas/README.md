# Lista de Tarefas em Python — Flet e TTKBootstrap

Este projeto mostra duas formas de fazer uma lista de tarefas em Python.

A primeira usa **Flet** e a segunda usa **TTKBootstrap**, que funciona sobre o **Tkinter**. A ideia é comparar as duas abordagens usando praticamente o mesmo aplicativo.

---

## Sumário

- [Antes de começar: o que são essas bibliotecas?](#antes-de-começar-o-que-são-essas-bibliotecas)
- [Flet](#flet)
  - [O campo de texto e o Enter](#o-campo-de-texto-e-o-enter)
  - [Cada tarefa é uma linha](#cada-tarefa-é-uma-linha)
  - [Remover uma tarefa](#remover-uma-tarefa)
  - [Adicionar uma tarefa](#adicionar-uma-tarefa)
  - [Rodando o projeto Flet](#rodando-o-projeto-flet)
- [TTKBootstrap](#ttkbootstrap)
  - [A base: janela e tema](#a-base-janela-e-tema)
  - [Guardando cada tarefa](#guardando-cada-tarefa)
  - [Riscar uma tarefa concluída](#riscar-uma-tarefa-concluída)
  - [Remover uma tarefa](#remover-uma-tarefa-1)
  - [A mensagem de lista vazia](#a-mensagem-de-lista-vazia)
  - [Scroll do mouse](#scroll-do-mouse)
  - [Rodando o projeto TTKBootstrap](#rodando-o-projeto-ttkbootstrap)
- [Comparando os dois](#comparando-os-dois)
- [Temas do TTKBootstrap](#temas-do-ttkbootstrap)
- [Links úteis](#links-úteis)

---

## Antes de começar: o que são essas bibliotecas?

Antes de olhar o código, vale entender o papel de cada uma.

### Tkinter

**Tkinter** é a biblioteca gráfica que acompanha o Python. Ela permite criar programas com janelas, botões, campos de texto, menus, caixas de seleção e outros elementos de interface.

Por exemplo, com Tkinter você pode criar uma janela e colocar um botão dentro dela.

A principal vantagem é que ele já faz parte da instalação padrão do Python em muitas plataformas. A desvantagem é que a aparência dos widgets pode parecer mais simples e antiga quando comparada com ferramentas mais modernas.

O TTKBootstrap entra justamente nessa parte.

### ttk

O **ttk** é o conjunto de widgets temáticos do Tkinter. Ele oferece componentes como `Frame`, `Button`, `Label`, `Checkbutton` e outros, com uma aparência um pouco mais moderna que os widgets básicos do Tkinter.

O `ttkbootstrap` trabalha principalmente em cima dessa estrutura.

### TTKBootstrap

**TTKBootstrap** é uma biblioteca que adiciona temas e estilos ao Tkinter/ttk.

Ela não substitui o Tkinter. Você continua usando a mesma ideia de janela, widgets e eventos, mas ganha temas prontos e uma forma mais prática de estilizar os componentes.

Os temas lembram o visual do Bootstrap. Existem opções como `darkly`, `flatly`, `litera`, `minty` e `superhero`.

É uma boa opção para quem já conhece Tkinter e quer melhorar a aparência do aplicativo sem precisar montar todo o estilo do zero.

### Flet

**Flet** é um framework para criar interfaces usando Python. Ele tem seus próprios componentes, como `TextField`, `Checkbox`, `Button`, `Row` e `Column`.

A proposta é diferente do Tkinter: em vez de trabalhar diretamente com os widgets tradicionais do sistema operacional, o Flet oferece uma estrutura própria para montar a interface.

Ele também permite criar aplicações para desktop e dispositivos móveis.

O código costuma ser mais direto para quem está começando, principalmente porque os elementos da tela ficam organizados como controles dentro de outros controles.

### Resumindo

| Tecnologia | O que é? | Base |
| --- | --- | --- |
| Tkinter | Biblioteca gráfica do Python | Tk |
| ttk | Widgets temáticos do Tkinter | Tkinter |
| TTKBootstrap | Temas e estilos para Tkinter/ttk | Tkinter + ttk |
| Flet | Framework para criação de interfaces | Componentes próprios |

Neste projeto, portanto, a comparação é principalmente entre **Flet** e **TTKBootstrap**. O TTKBootstrap usa o Tkinter por baixo, enquanto o Flet segue outra abordagem.

---

## Flet

Arquivo: `app_flet.py`

```python
import flet as ft


def main(page: ft.Page):
    page.title = "Lista de Tarefas (To-do List)"
    page.vertical_alignment = ft.MainAxisAlignment.START
```

No Flet, a função `main` recebe um objeto `page`. Ele representa a página principal da aplicação.

Os elementos que aparecem na tela são adicionados nessa estrutura.

### O campo de texto e o Enter

```python
campo_tarefa = ft.TextField(
    hint_text="O que você precisa fazer?",
    width=300,
    autofocus=True,
    on_submit=lambda e: adicionar_tarefa(e),
)
```

`TextField` cria um campo onde o usuário pode digitar.

`autofocus=True` faz com que o campo já receba o foco quando o aplicativo abrir.

Já `on_submit` define o que acontece quando o usuário confirma o campo. Neste caso, pressionar Enter chama `adicionar_tarefa`.

### Cada tarefa é uma linha

```python
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
```

A função cria uma linha com duas coisas: um `Checkbox` e um botão de excluir.

O `Row` organiza os elementos na horizontal.

O `SPACE_BETWEEN` coloca um elemento de cada lado da linha, deixando o espaço entre eles.

O botão de excluir recebe uma função no `on_click`. Essa função sabe qual linha deve ser removida porque recebe a própria variável `linha`.

### Remover uma tarefa

```python
def remover_tarefa(linha):
    lista_de_tarefas.controls.remove(linha)
    lista_de_tarefas.update()
```

Aqui a linha é removida da lista de controles.

Depois, `update()` avisa ao Flet que aquele controle precisa ser atualizado na tela.

### Adicionar uma tarefa

```python
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
```

`strip()` remove espaços no começo e no final do texto. Assim, uma entrada formada apenas por espaços não vira uma tarefa.

Se houver texto, uma nova linha é criada e adicionada à lista. Depois o campo é limpo e recebe o foco novamente.

Se o campo estiver vazio, `error_text` mostra uma mensagem abaixo dele.

Também dá para perceber que não é necessário atualizar a página inteira. O código atualiza os controles que realmente mudaram.

### Rodando o projeto Flet

```bash
pip install flet
python app_flet.py
```

---

## TTKBootstrap

Arquivo: `app_ttkbootstrap.py`

O TTKBootstrap usa os widgets do Tkinter/ttk e adiciona estilos e temas.

Neste projeto, a aplicação é organizada dentro de uma classe chamada `TodoApp`. Essa organização ajuda a manter os widgets e as funções relacionadas à lista no mesmo lugar.

### A base: janela e tema

```python
if __name__ == "__main__":
    root = ttk.Window(themename="darkly")
    app = TodoApp(root)
    root.mainloop()
```

`ttk.Window` cria a janela principal já com o tema escolhido.

Neste caso, o tema é `darkly`.

O `mainloop()` mantém a aplicação funcionando e esperando eventos, como cliques e teclas pressionadas.

### Guardando cada tarefa

```python
self.tasks = []
```

A lista `self.tasks` guarda as tarefas criadas.

Cada tarefa é representada por um dicionário com as informações e widgets relacionados a ela.

```python
def _criar_linha(self, texto):
    item = {"texto": texto}

    tarefa_frame = ttk.Frame(self.tarefas_frame, bootstyle="light")
    tarefa_frame.pack(fill=X, pady=5, padx=5)

    var_check = tk.BooleanVar()

    checkbox = ttk.Checkbutton(
        tarefa_frame,
        text=texto,
        variable=var_check,
        bootstyle="success",
        command=lambda: self._alternar_estilo(item)
    )
    checkbox.pack(side=LEFT, fill=X, expand=True, padx=5, pady=5)

    botao_remover = ttk.Button(
        tarefa_frame,
        text="✕",
        command=lambda: self.remover_tarefa(item),
        bootstyle="danger",
        width=3
    )
    botao_remover.pack(side=RIGHT, padx=5, pady=5)

    item.update({
        "var": var_check,
        "frame": tarefa_frame,
        "checkbox": checkbox
    })

    self.tasks.append(item)
```

Cada item guarda o seu próprio `Frame`, `Checkbutton` e variável de controle.

Isso facilita bastante na hora de remover ou alterar uma tarefa, porque o programa já sabe quais widgets pertencem àquele item.

### Riscar uma tarefa concluída

```python
def _alternar_estilo(self, item):
    estilo = "success-strikethrough" if item["var"].get() else "success"
    item["checkbox"].configure(bootstyle=estilo)
```

Quando o checkbox muda, essa função é chamada.

Se estiver marcado, o estilo `success-strikethrough` coloca um risco no texto. Se estiver desmarcado, volta para o estilo normal.

### Remover uma tarefa

```python
def remover_tarefa(self, item):
    item["frame"].destroy()
    self.tasks.remove(item)
    self._atualizar_placeholder()
```

Em vez de reconstruir toda a lista, o código destrói somente o `Frame` daquela tarefa.

Depois, o item é removido de `self.tasks`.

### A mensagem de lista vazia

```python
self.label_vazio = ttk.Label(
    self.tarefas_frame,
    text="Nenhuma tarefa adicionada",
    font=("Arial", 12),
    bootstyle="secondary"
)
```

O texto de lista vazia é criado uma vez.

Depois, uma função decide quando ele deve aparecer:

```python
def _atualizar_placeholder(self):
    if self.tasks:
        self.label_vazio.pack_forget()
    else:
        self.label_vazio.pack(pady=20)
```

Se existir pelo menos uma tarefa, `pack_forget()` esconde a mensagem.

Se não existir nenhuma, `pack()` mostra o texto.

### Scroll do mouse

```python
self.canvas.bind(
    "<Enter>",
    lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
)

self.canvas.bind(
    "<Leave>",
    lambda e: self.canvas.unbind_all("<MouseWheel>")
)
```

Aqui o scroll do mouse é ativado quando o cursor entra na área da lista.

Quando o cursor sai, o evento é desativado.

Isso evita que o scroll da lista fique interferindo em outras partes da janela.

### Rodando o projeto TTKBootstrap

```bash
pip install ttkbootstrap
python app_ttkbootstrap.py
```

---

## Comparando os dois

| | Flet | TTKBootstrap |
| --- | --- | --- |
| Base | Framework próprio | Tkinter + ttk |
| Celular | Sim | Não |
| Widgets | Componentes do Flet | Widgets do Tkinter/ttk |
| Estilo | Componentes e propriedades do Flet | Temas do TTKBootstrap |
| Organização usada no projeto | Funções e controles | Classe `TodoApp` |
| Atualização | `.update()` | Métodos do Tkinter, como `.pack()` e `.destroy()` |
| Estilo de programação | Mais próximo de uma estrutura declarativa | Mais próximo do Tkinter tradicional |

Não existe uma opção que seja obrigatoriamente melhor.

Se você já conhece Tkinter e quer continuar usando a biblioteca com uma aparência melhor, TTKBootstrap é uma alternativa interessante.

Se prefere trabalhar com os componentes do próprio framework e quer também considerar aplicações para celular, Flet pode fazer mais sentido.

---

## Temas do TTKBootstrap

Para mudar o tema, basta alterar a criação da janela:

```python
root = ttk.Window(themename="darkly")
```

Alguns temas disponíveis incluem:

- `darkly`
- `flatly`
- `litera`
- `minty`
- `solar`
- `superhero`
- `sandstone`

---

## Links úteis

- Documentação do Flet: https://flet.dev/
- Documentação do TTKBootstrap: https://ttkbootstrap.readthedocs.io/
- Documentação do Tkinter: https://docs.python.org/3/library/tkinter.html
