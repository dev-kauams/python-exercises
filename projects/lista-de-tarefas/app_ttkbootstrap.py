import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import tkinter as tk

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tarefas (To-do List)")
        self.root.geometry("600x500")

        self.tasks = []

        self._montar_interface()
        self._atualizar_placeholder()

    def _montar_interface(self):
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=BOTH, expand=True)

        titulo = ttk.Label(
            self.main_frame,
            text="Tarefas",
            font=("Arial", 24, "bold"),
            bootstyle="info"
        )
        titulo.pack(pady=10)

        entrada_frame = ttk.Frame(self.main_frame)
        entrada_frame.pack(fill=X, pady=10)

        self.campo_tarefa = ttk.Entry(
            entrada_frame,
            bootstyle="info",
            font=("Arial", 12)
        )
        self.campo_tarefa.pack(side=LEFT, fill=X, expand=True, padx=(0, 10))
        self.campo_tarefa.bind("<Return>", self.adicionar_tarefa)
        self.campo_tarefa.focus()

        self.botao_adicionar = ttk.Button(
            entrada_frame,
            text="Adicionar",
            command=self.adicionar_tarefa,
            bootstyle="success"
        )
        self.botao_adicionar.pack(side=LEFT)

        lista_frame = ttk.Frame(self.main_frame)
        lista_frame.pack(fill=BOTH, expand=True, pady=10)

        scrollbar = ttk.Scrollbar(lista_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas = tk.Canvas(
            lista_frame,
            yscrollcommand=scrollbar.set,
            bg="#f0f0f0",
            highlightthickness=0
        )
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=self.canvas.yview)

        self.tarefas_frame = ttk.Frame(self.canvas)
        self.window = self.canvas.create_window((0, 0), window=self.tarefas_frame, anchor="nw")

        self.tarefas_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        self.label_vazio = ttk.Label(
            self.tarefas_frame,
            text="Nenhuma tarefa adicionada",
            font=("Arial", 12),
            bootstyle="secondary"
        )

    def _on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def adicionar_tarefa(self, event=None):
        texto = self.campo_tarefa.get().strip()

        if not texto:
            messagebox.showwarning("Aviso", "Por favor, digite uma tarefa!")
            return

        self.campo_tarefa.delete(0, END)
        self._criar_linha(texto)
        self._atualizar_placeholder()
        self.campo_tarefa.focus()

    def _criar_linha(self, texto):
        """Cria apenas a linha da nova tarefa, sem redesenhar as demais."""
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

        item.update({"var": var_check, "frame": tarefa_frame, "checkbox": checkbox})
        self.tasks.append(item)

    def _alternar_estilo(self, item):
        estilo = "success-strikethrough" if item["var"].get() else "success"
        item["checkbox"].configure(bootstyle=estilo)

    def remover_tarefa(self, item):
        item["frame"].destroy()
        self.tasks.remove(item)
        self._atualizar_placeholder()

    def _atualizar_placeholder(self):
        if self.tasks:
            self.label_vazio.pack_forget()
        else:
            self.label_vazio.pack(pady=20)


if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = TodoApp(root)

    menubar = tk.Menu(root)

    file_menu = tk.Menu(menubar, tearoff=False)
    file_menu.add_command(label="New", command=lambda: print("new"))
    file_menu.add_command(label="Open…", command=lambda: print("open"))
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.destroy)
    menubar.add_cascade(label="File", menu=file_menu)

    edit_menu = tk.Menu(menubar, tearoff=False)
    edit_menu.add_command(label="Undo", command=lambda: print("undo"))
    menubar.add_cascade(label="Edit", menu=edit_menu)

    root.configure(menu=menubar)

    root.mainloop()

