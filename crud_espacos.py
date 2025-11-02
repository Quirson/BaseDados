"""
MÓDULO ESPAÇOS - CRUD COMPLETO COM VALIDAÇÃO
Gerencia espaços de publicidade (físicos e digitais)
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
from logger_config import log_execution, safe_operation, app_logger
from config import COLORS
from crud_validators import CRUDValidator, ValidationError

class EspacosCRUD:
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

        ctk.CTkLabel(title_frame, text="Gestão de Espaços", font=("Arial", 22, "bold"), text_color=COLORS['text_primary']).pack(side="left")

        self.create_toolbar(container)
        self.create_espacos_table(container)

    @log_execution
    def create_toolbar(self, parent):
        toolbar = ctk.CTkFrame(parent, fg_color=COLORS['dark_card'], corner_radius=10, height=70)
        toolbar.pack(fill="x", pady=(0, 20))
        toolbar.pack_propagate(False)

        btn_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame.pack(expand=True, padx=20, pady=12)

        buttons = [
            ("Novo Espaço", self.novo_espaco, COLORS['success']),
            ("Editar", self.editar_espaco, COLORS['primary']),
            ("Excluir", self.excluir_espaco, COLORS['danger']),
            ("Atualizar", self.load_data, COLORS['accent']),
        ]

        for text, command, color in buttons:
            btn = ctk.CTkButton(btn_frame, text=text, command=command, font=("Arial", 12, "bold"),
                               fg_color=color, hover_color=self.darken_color(color), width=140, height=38, corner_radius=8)
            btn.pack(side="left", padx=8)

    @log_execution
    def create_espacos_table(self, parent):
        table_frame = ctk.CTkFrame(parent, fg_color=COLORS['dark_card'], corner_radius=12)
        table_frame.pack(fill="both", expand=True, pady=10)

        header_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(header_frame, text="Lista de Espaços", font=("Arial", 18, "bold"), text_color=COLORS['text_primary']).pack(side="left")

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

        columns = ('ID', 'Localização', 'Tipo', 'Dimensões', 'Preço Base', 'Disponibilidade', 'Proprietário')
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=12)

        widths = [50, 180, 100, 100, 100, 120, 150]
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

        self.tree.bind('<Double-1>', lambda e: self.editar_espaco())

    @safe_operation()
    def load_data(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            query = """
            SELECT Id_espaco, Local_fis_dig, Tipo, Dimensoes, Preco_base, Disponibilidade, Proprietario
            FROM Espaco_dados
            ORDER BY Local_fis_dig
            """
            result = self.db.execute_query(query)

            if result and result[1]:
                for row in result[1]:
                    self.tree.insert('', 'end', values=(
                        str(row[0]),
                        row[1] or "N/A",
                        row[2] or "N/A",
                        row[3] or "N/A",
                        f"MT {row[4]:,.2f}" if row[4] else "MT 0.00",
                        row[5] or "Indisponível",
                        row[6] or "N/A"
                    ))
                self.logger.info(f"Carregados {len(result[1])} espaços")
        except Exception as e:
            self.logger.error(f"Erro ao carregar espaços: {str(e)}")

    def clear_content(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def novo_espaco(self):
        self.open_form(mode='create')

    def editar_espaco(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um espaço para editar.")
            return
        item = self.tree.item(selected[0])
        id_espaco = item['values'][0]
        self.open_form(mode='edit', id_espaco=id_espaco)

    def open_form(self, mode='create', id_espaco=None):
        form_window = ctk.CTkToplevel(self.parent)
        form_window.title("Novo Espaço" if mode == 'create' else "Editar Espaço")
        form_window.geometry("700x600")

        form_window.update_idletasks()
        x = (form_window.winfo_screenwidth() // 2) - (700 // 2)
        y = (form_window.winfo_screenheight() // 2) - (600 // 2)
        form_window.geometry(f"700x600+{x}+{y}")

        form_window.transient(self.parent)
        form_window.grab_set()

        form_container = ctk.CTkScrollableFrame(form_window, fg_color=COLORS['dark_bg'])
        form_container.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(form_container, text="Novo Espaço" if mode == 'create' else "Editar Espaço",
                    font=("Arial", 20, "bold"), text_color=COLORS['text_primary']).pack(pady=(0, 20))

        form_frame = ctk.CTkFrame(form_container, fg_color=COLORS['dark_card'], corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        fields = {}
        row = 0

        if mode == 'edit':
            self.create_form_field(form_frame, "ID:", row, 'id_espaco', fields, readonly=True)
            row += 1

        self.create_form_field(form_frame, "Localização (Física/Digital):*", row, 'local', fields, width=500)
        row += 1

        label = ctk.CTkLabel(form_frame, text="Tipo de Espaço:*", font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        fields['tipo'] = ctk.CTkComboBox(form_frame, values=['Billboard', 'Digital Screen', 'Rádio', 'Online', 'Impressa', 'Outro'], width=350, height=35)
        fields['tipo'].grid(row=row, column=1, padx=20, pady=10, sticky="w")
        row += 1

        self.create_form_field(form_frame, "Dimensões:*", row, 'dimensoes', fields, width=300)
        row += 1

        self.create_form_field(form_frame, "Resolução (se digital):", row, 'resolucao', fields, width=300)
        row += 1

        self.create_form_field(form_frame, "Visibilidade:*", row, 'visibilidade', fields, width=400)
        row += 1

        self.create_form_field(form_frame, "Preço Base (MT):*", row, 'preco_base', fields, width=200)
        row += 1

        label = ctk.CTkLabel(form_frame, text="Disponibilidade:*", font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        fields['disponibilidade'] = ctk.CTkComboBox(form_frame, values=['Disponível', 'Indisponível', 'Em Manutenção'], width=300, height=35)
        fields['disponibilidade'].grid(row=row, column=1, padx=20, pady=10, sticky="w")
        row += 1

        self.create_form_field(form_frame, "Proprietário:*", row, 'proprietario', fields, width=400)
        row += 1

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=row, column=0, columnspan=2, pady=30)

        ctk.CTkButton(btn_frame, text="Salvar", command=lambda: self.save_espaco(mode, fields, id_espaco, form_window),
                     font=("Arial", 14, "bold"), fg_color=COLORS['success'], width=150, height=40).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", command=form_window.destroy, font=("Arial", 14, "bold"),
                     fg_color=COLORS['danger'], width=150, height=40).pack(side="left", padx=10)

        if mode == 'edit' and id_espaco:
            self.load_form_data(fields, id_espaco)

    def create_form_field(self, parent, label_text, row, field_name, fields, width=300, readonly=False):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")

        entry = ctk.CTkEntry(parent, width=width, height=35)
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="w")

        if readonly:
            entry.configure(state="disabled")

        fields[field_name] = entry

    def load_form_data(self, fields, id_espaco):
        query = """
        SELECT Id_espaco, Local_fis_dig, Tipo, Dimensoes, Resolucao, Visibilidade, Preco_base, Disponibilidade, Proprietario
        FROM Espaco_dados WHERE Id_espaco = :id
        """
        result = self.db.execute_query(query, {'id': id_espaco})

        if result and result[1]:
            data = result[1][0]
            fields['id_espaco'].configure(state="normal")
            fields['id_espaco'].insert(0, str(data[0]))
            fields['id_espaco'].configure(state="disabled")
            fields['local'].insert(0, data[1] or '')
            fields['tipo'].set(data[2] if data[2] else 'Outro')
            fields['dimensoes'].insert(0, data[3] or '')
            fields['resolucao'].insert(0, data[4] or '')
            fields['visibilidade'].insert(0, data[5] or '')
            fields['preco_base'].insert(0, str(data[6] or 0))
            fields['disponibilidade'].set(data[7] if data[7] else 'Disponível')
            fields['proprietario'].insert(0, data[8] or '')

    def save_espaco(self, mode, fields, id_espaco, form_window):
        try:
            data = {
                'local': fields['local'].get(),
                'tipo': fields['tipo'].get(),
                'dimensoes': fields['dimensoes'].get(),
                'resolucao': fields['resolucao'].get(),
                'visibilidade': fields['visibilidade'].get(),
                'preco_base': fields['preco_base'].get(),
                'disponibilidade': fields['disponibilidade'].get(),
                'proprietario': fields['proprietario'].get()
            }

            CRUDValidator.validate_espaco(data)

            if mode == 'create':
                query = """
                INSERT INTO Espaco_dados (Local_fis_dig, Tipo, Dimensoes, Resolucao, Visibilidade, Preco_base, Disponibilidade, Proprietario)
                VALUES (:local, :tipo, :dim, :res, :vis, :preco, :disp, :prop)
                """
                params = {
                    'local': data['local'],
                    'tipo': data['tipo'],
                    'dim': data['dimensoes'],
                    'res': data['resolucao'] or None,
                    'vis': data['visibilidade'],
                    'preco': float(data['preco_base']),
                    'disp': data['disponibilidade'],
                    'prop': data['proprietario']
                }
                self.db.execute_query(query, params, fetch=False)
                messagebox.showinfo("Sucesso", "Espaço criado com sucesso!")
            else:
                query = """
                UPDATE Espaco_dados SET Local_fis_dig = :local, Tipo = :tipo, Dimensoes = :dim,
                Resolucao = :res, Visibilidade = :vis, Preco_base = :preco, Disponibilidade = :disp,
                Proprietario = :prop WHERE Id_espaco = :id
                """
                params = {
                    'id': id_espaco,
                    'local': data['local'],
                    'tipo': data['tipo'],
                    'dim': data['dimensoes'],
                    'res': data['resolucao'] or None,
                    'vis': data['visibilidade'],
                    'preco': float(data['preco_base']),
                    'disp': data['disponibilidade'],
                    'prop': data['proprietario']
                }
                self.db.execute_query(query, params, fetch=False)
                messagebox.showinfo("Sucesso", "Espaço atualizado com sucesso!")

            form_window.destroy()
            self.load_data()

        except ValidationError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            self.logger.error(f"Erro ao salvar espaço: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def excluir_espaco(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um espaço para excluir.")
            return

        item = self.tree.item(selected[0])
        id_espaco = item['values'][0]
        local = item['values'][1]

        if messagebox.askyesno("Confirmar", f"Excluir espaço em '{local}'? Esta ação não pode ser desfeita."):
            try:
                query = "DELETE FROM Espaco_dados WHERE Id_espaco = :id"
                self.db.execute_query(query, {'id': id_espaco}, fetch=False)
                messagebox.showinfo("Sucesso", "Espaço excluído!")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")

    @staticmethod
    def darken_color(color):
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(max(0, c - 30) for c in rgb)
        return '#%02x%02x%02x' % darker_rgb

def show_espacos_module(parent, db, main_app):
    EspacosCRUD(parent, db, main_app)
