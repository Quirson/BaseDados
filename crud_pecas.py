"""
MÓDULO PEÇAS CRIATIVAS - CRUD COMPLETO COM VALIDAÇÃO
Gerencia todos os tipos de peças: visuais, audiovisuais e interativas
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
from logger_config import log_execution, safe_operation, app_logger
from config import COLORS
from crud_validators import CRUDValidator, ValidationError

class PecasCRUD:
    def __init__(self, parent, db, main_app):
        self.parent = parent
        self.db = db
        self.main_app = main_app
        self.logger = app_logger
        self.create_interface()
        self.load_data()

    @log_execution
    def create_interface(self):
        self.clear_content()

        container = ctk.CTkFrame(self.parent, fg_color=COLORS['dark_bg'])
        container.pack(fill="both", expand=True, padx=20, pady=20)

        title_frame = ctk.CTkFrame(container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 25))

        ctk.CTkLabel(title_frame, text="Gestão de Peças Criativas", font=("Arial", 22, "bold"), text_color=COLORS['text_primary']).pack(side="left")

        self.create_toolbar(container)
        self.create_pecas_table(container)

    @log_execution
    def create_toolbar(self, parent):
        toolbar = ctk.CTkFrame(parent, fg_color=COLORS['dark_card'], corner_radius=10, height=70)
        toolbar.pack(fill="x", pady=(0, 20))
        toolbar.pack_propagate(False)

        btn_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame.pack(expand=True, padx=20, pady=12)

        buttons = [
            ("Nova Peça", self.nova_peca, COLORS['success']),
            ("Editar", self.editar_peca, COLORS['primary']),
            ("Excluir", self.excluir_peca, COLORS['danger']),
            ("Atualizar", self.load_data, COLORS['accent']),
        ]

        for text, command, color in buttons:
            btn = ctk.CTkButton(btn_frame, text=text, command=command, font=("Arial", 12, "bold"),
                               fg_color=color, hover_color=self.darken_color(color), width=140, height=38, corner_radius=8)
            btn.pack(side="left", padx=8)

    @log_execution
    def create_pecas_table(self, parent):
        table_frame = ctk.CTkFrame(parent, fg_color=COLORS['dark_card'], corner_radius=12)
        table_frame.pack(fill="both", expand=True, pady=10)

        header_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(header_frame, text="Lista de Peças Criativas", font=("Arial", 18, "bold"), text_color=COLORS['text_primary']).pack(side="left")

        table_container = ctk.CTkFrame(table_frame, fg_color="transparent")
        table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.create_treeview(table_container)

    @log_execution
    def create_treeview(self, parent):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=COLORS['dark_card'], foreground=COLORS['text_primary'], fieldbackground=COLORS['dark_card'], rowheight=35)
        style.configure("Treeview.Heading", background=COLORS['primary'], foreground=COLORS['text_primary'], font=("Arial", 11, "bold"))
        style.map("Treeview", background=[('selected', COLORS['accent'])])

        columns = ('ID', 'Título', 'Criador', 'Data Criação', 'Status', 'Classificação')
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=12)

        widths = [60, 200, 150, 120, 100, 120]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")

        v_scroll = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(parent, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.tree.bind('<Double-1>', lambda e: self.editar_peca())

    @safe_operation()
    def load_data(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            query = """
            SELECT Id_unicopeca, Titulo, Criador, TO_CHAR(Data_criacao, 'DD/MM/YYYY'),
                   Status_aprov, Classif_conteudo
            FROM Pecas_criativas
            ORDER BY Data_criacao DESC
            """
            result = self.db.execute_query(query)

            if result and result[1]:
                for row in result[1]:
                    self.tree.insert('', 'end', values=(
                        str(row[0]),
                        row[1] or "N/A",
                        row[2] or "N/A",
                        row[3] or "N/A",
                        row[4] or "Pendente",
                        str(row[5] or 0)
                    ))
                self.logger.info(f"Carregadas {len(result[1])} peças criativas")
        except Exception as e:
            self.logger.error(f"Erro ao carregar peças: {str(e)}")

    def clear_content(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def nova_peca(self):
        self.open_form(mode='create')

    def editar_peca(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma peça para editar.")
            return
        item = self.tree.item(selected[0])
        id_peca = item['values'][0]
        self.open_form(mode='edit', id_peca=id_peca)

    def open_form(self, mode='create', id_peca=None):
        form_window = ctk.CTkToplevel(self.parent)
        form_window.title("Nova Peça" if mode == 'create' else "Editar Peça")
        form_window.geometry("750x700")

        form_window.update_idletasks()
        x = (form_window.winfo_screenwidth() // 2) - (750 // 2)
        y = (form_window.winfo_screenheight() // 2) - (700 // 2)
        form_window.geometry(f"750x700+{x}+{y}")

        form_window.transient(self.parent)
        form_window.grab_set()

        form_container = ctk.CTkScrollableFrame(form_window, fg_color=COLORS['dark_bg'])
        form_container.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(form_container, text="Nova Peça Criativa" if mode == 'create' else "Editar Peça",
                    font=("Arial", 20, "bold"), text_color=COLORS['text_primary']).pack(pady=(0, 20))

        form_frame = ctk.CTkFrame(form_container, fg_color=COLORS['dark_card'], corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        fields = {}
        row = 0

        if mode == 'edit':
            self.create_form_field(form_frame, "ID:", row, 'id_peca', fields, readonly=True)
            row += 1

        self.create_form_field(form_frame, "Título:*", row, 'titulo', fields, width=500)
        row += 1

        label = ctk.CTkLabel(form_frame, text="Descrição:*", font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="nw")
        fields['descricao'] = ctk.CTkTextbox(form_frame, width=500, height=80)
        fields['descricao'].grid(row=row, column=1, padx=20, pady=10, sticky="w")
        row += 1

        self.create_form_field(form_frame, "Criador:*", row, 'criador', fields, width=400)
        row += 1

        label = ctk.CTkLabel(form_frame, text="Status de Aprovação:*", font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        fields['status'] = ctk.CTkComboBox(form_frame, values=['Pendente', 'Aprovado', 'Rejeitado', 'Em Revisão'], width=350, height=35)
        fields['status'].grid(row=row, column=1, padx=20, pady=10, sticky="w")
        row += 1

        self.create_form_field(form_frame, "Classificação de Conteúdo (0-18):*", row, 'classif', fields, width=150)
        row += 1

        label = ctk.CTkLabel(form_frame, text="Direitos Autorais:", font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="nw")
        fields['direitos'] = ctk.CTkTextbox(form_frame, width=500, height=60)
        fields['direitos'].grid(row=row, column=1, padx=20, pady=10, sticky="w")
        row += 1

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=row, column=0, columnspan=2, pady=30)

        ctk.CTkButton(btn_frame, text="Salvar", command=lambda: self.save_peca(mode, fields, id_peca, form_window),
                     font=("Arial", 14, "bold"), fg_color=COLORS['success'], width=150, height=40).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", command=form_window.destroy, font=("Arial", 14, "bold"),
                     fg_color=COLORS['danger'], width=150, height=40).pack(side="left", padx=10)

        if mode == 'edit' and id_peca:
            self.load_form_data(fields, id_peca)

    def create_form_field(self, parent, label_text, row, field_name, fields, width=300, readonly=False):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")

        entry = ctk.CTkEntry(parent, width=width, height=35)
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="w")

        if readonly:
            entry.configure(state="disabled")

        fields[field_name] = entry

    def load_form_data(self, fields, id_peca):
        query = """
        SELECT Id_unicopeca, Titulo, Descricao, Criador, Status_aprov, Classif_conteudo, Direitos_autorais
        FROM Pecas_criativas WHERE Id_unicopeca = :id
        """
        result = self.db.execute_query(query, {'id': id_peca})

        if result and result[1]:
            data = result[1][0]
            fields['id_peca'].configure(state="normal")
            fields['id_peca'].insert(0, str(data[0]))
            fields['id_peca'].configure(state="disabled")
            fields['titulo'].insert(0, data[1] or '')
            fields['descricao'].insert("1.0", data[2] or '')
            fields['criador'].insert(0, data[3] or '')
            fields['status'].set(data[4] if data[4] else 'Pendente')
            fields['classif'].insert(0, str(data[5] or 0))
            fields['direitos'].insert("1.0", data[6] or '')

    def save_peca(self, mode, fields, id_peca, form_window):
        try:
            data = {
                'titulo': fields['titulo'].get(),
                'descricao': fields['descricao'].get("1.0", "end-1c"),
                'criador': fields['criador'].get(),
                'status': fields['status'].get(),
                'classif': fields['classif'].get(),
                'direitos': fields['direitos'].get("1.0", "end-1c")
            }

            CRUDValidator.validate_peca(data)

            if mode == 'create':
                query = """
                INSERT INTO Pecas_criativas (Titulo, Descricao, Criador, Status_aprov, Classif_conteudo, Direitos_autorais, Data_criacao)
                VALUES (:titulo, :descricao, :criador, :status, :classif, :direitos, SYSDATE)
                """
                params = {
                    'titulo': data['titulo'],
                    'descricao': data['descricao'],
                    'criador': data['criador'],
                    'status': data['status'],
                    'classif': int(data['classif']),
                    'direitos': data['direitos']
                }
                self.db.execute_query(query, params, fetch=False)
                messagebox.showinfo("Sucesso", "Peça criada com sucesso!")
            else:
                query = """
                UPDATE Pecas_criativas SET Titulo = :titulo, Descricao = :descricao, Criador = :criador,
                Status_aprov = :status, Classif_conteudo = :classif, Direitos_autorais = :direitos
                WHERE Id_unicopeca = :id
                """
                params = {
                    'id': id_peca,
                    'titulo': data['titulo'],
                    'descricao': data['descricao'],
                    'criador': data['criador'],
                    'status': data['status'],
                    'classif': int(data['classif']),
                    'direitos': data['direitos']
                }
                self.db.execute_query(query, params, fetch=False)
                messagebox.showinfo("Sucesso", "Peça atualizada com sucesso!")

            form_window.destroy()
            self.load_data()

        except ValidationError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            self.logger.error(f"Erro ao salvar peça: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def excluir_peca(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma peça para excluir.")
            return

        item = self.tree.item(selected[0])
        id_peca = item['values'][0]
        titulo = item['values'][1]

        if messagebox.askyesno("Confirmar", f"Excluir '{titulo}'? Esta ação não pode ser desfeita."):
            try:
                query = "DELETE FROM Pecas_criativas WHERE Id_unicopeca = :id"
                self.db.execute_query(query, {'id': id_peca}, fetch=False)
                messagebox.showinfo("Sucesso", "Peça excluída!")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")

    @staticmethod
    def darken_color(color):
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(max(0, c - 30) for c in rgb)
        return '#%02x%02x%02x' % darker_rgb

def show_pecas_module(parent, db, main_app):
    PecasCRUD(parent, db, main_app)
