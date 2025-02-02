import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json

# Caminho para salvar as informações dos servidores
SAVE_FILE = "servidores.json"

# Carregar os servidores salvos
def load_servers():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as file:
            return json.load(file)
    return []

# Salvar os servidores no arquivo
def save_servers(data):
    with open(SAVE_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Classe principal
class ServerManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Servidores Minecraft")
        self.servers = load_servers()

        # Lista de servidores
        self.server_frames = []
        self.create_ui()

    def create_ui(self):
        # Frame principal
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Botão para adicionar servidor
        tk.Button(self.main_frame, text="Adicionar Servidor", command=self.add_server_ui).pack(pady=5)

        # Frame para listar servidores
        self.server_list_frame = tk.Frame(self.main_frame)
        self.server_list_frame.pack(fill=tk.BOTH, expand=True)

        # Exibir os servidores carregados
        self.display_servers()

    def add_server_ui(self):
        # Nova janela para adicionar servidor
        add_window = tk.Toplevel(self.root)
        add_window.title("Adicionar Servidor")

        tk.Label(add_window, text="Nome de Identificação:").pack(pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.pack(pady=5)

        tk.Label(add_window, text="Descrição:").pack(pady=5)
        desc_entry = tk.Entry(add_window)
        desc_entry.pack(pady=5)

        tk.Label(add_window, text="Caminho do Executável (.bat):").pack(pady=5)
        path_entry = tk.Entry(add_window)
        path_entry.pack(pady=5)

        def browse_file():
            path = filedialog.askopenfilename(filetypes=[("Arquivos BAT", "*.bat")])
            if path:
                path_entry.delete(0, tk.END)
                path_entry.insert(0, path)

        tk.Button(add_window, text="Procurar", command=browse_file).pack(pady=5)

        def save_server():
            name = name_entry.get()
            desc = desc_entry.get()
            path = path_entry.get()
            if not name or not path:
                messagebox.showerror("Erro", "Nome e caminho são obrigatórios!")
                return

            server = {"name": name, "description": desc, "path": path, "visible": True}
            self.servers.append(server)
            save_servers(self.servers)
            add_window.destroy()
            self.display_servers()

        tk.Button(add_window, text="Salvar", command=save_server).pack(pady=10)

    def display_servers(self):
        # Limpar servidores existentes na interface
        for frame in self.server_frames:
            frame.destroy()
        self.server_frames.clear()

        for server in self.servers:
            frame = tk.Frame(self.server_list_frame, borderwidth=1, relief="solid", pady=5, padx=5)
            frame.pack(fill=tk.X, pady=5)

            # Informações do servidor
            tk.Label(frame, text=f"Nome: {server['name']}", font=("Arial", 12, "bold")).pack(anchor="w")
            tk.Label(frame, text=f"Descrição: {server['description']}").pack(anchor="w")
            tk.Label(frame, text=f"Caminho: {server['path']}").pack(anchor="w")

            # Botões para iniciar e desligar o servidor
            btn_frame = tk.Frame(frame)
            btn_frame.pack(anchor="e", pady=5)

            def start_server(path=server['path']):
                os.system(f'start "" "{path}"')

            def remove_server():
                self.servers.remove(server)
                save_servers(self.servers)
                self.display_servers()

            def toggle_visibility():
                server['visible'] = not server['visible']
                save_servers(self.servers)
                self.display_servers()

            tk.Button(btn_frame, text="Iniciar", command=start_server).pack(side=tk.LEFT, padx=5)
            tk.Button(btn_frame, text="Remover", command=remove_server).pack(side=tk.LEFT, padx=5)
            visibility_btn_text = "Ocultar" if server["visible"] else "Mostrar"
            tk.Button(btn_frame, text=visibility_btn_text, command=toggle_visibility).pack(side=tk.LEFT, padx=5)

            # Adicionar o frame à lista
            self.server_frames.append(frame)

# Executar a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = ServerManagerApp(root)
    root.mainloop()
