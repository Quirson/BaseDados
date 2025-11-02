"""
MÓDULO ANUNCIANTES - CRUD COMPLETO COM VALIDAÇÃO SÓLIDA
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
from logger_config import log_execution, safe_operation, app_logger
from config import COLORS
from crud_validators import CRUDValidator, ValidationError

class AnunciantesCRUD:
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

        ctk.CTkLabel(
            title_frame,
            text="Gestão de Anunciantes",
            font=("Arial", 22, "bold"),
            text_color=COLORS['text_primary']
        ).pack(side="left")

        self.create_toolbar(container)
        self.create_anunciantes_table(container)

    @log_execution
    def create_toolbar(self, parent):
        toolbar = ctk.CTkFrame(parent, fg_color=COLORS['dark_card'],
                              corner_radius=10, height=70)
        toolbar.pack(fill="x", pady=(0, 20))
        toolbar.pack_propagate(False)

        btn_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame.pack(expand=True, padx=20, pady=12)

        buttons = [
            ("Novo Anunciante", self.novo_anunciante, COLORS['success']),
            ("Editar", self.editar_anunciante, COLORS['primary']),
            ("Excluir", self.excluir_anunciante, COLORS['danger']),
            ("Atualizar", self.load_data, COLORS['accent']),
        ]

        for text, command, color in buttons:
            btn = ctk.CTkButton(
                btn_frame,
                text=text,
                command=command,
                font=("Arial", 12, "bold"),
                fg_color=color,
                hover_color=self.darken_color(color),
                width=140,
                height=38,
                corner_radius=8
            )
            btn.pack(side="left", padx=8)

    @log_execution
    def create_anunciantes_table(self, parent):
        table_frame = ctk.CTkFrame(parent, fg_color=COLORS['dark_card'], corner_radius=12)
        table_frame.pack(fill="both", expand=True, pady=10)

        header_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(
            header_frame,
            text="Lista de Anunciantes",
            font=("Arial", 18, "bold"),
            text_color=COLORS['text_primary']
        ).pack(side="left")

        table_container = ctk.CTkFrame(table_frame, fg_color="transparent")
        table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.create_treeview(table_container)

    @log_execution
    def create_treeview(self, parent):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=COLORS['dark_card'],
                        foreground=COLORS['text_primary'],
                        fieldbackground=COLORS['dark_card'],
                        rowheight=35)
        style.configure("Treeview.Heading",
                        background=COLORS['primary'],
                        foreground=COLORS['text_primary'],
                        font=("Arial", 11, "bold"))
        style.map("Treeview", background=[('selected', COLORS['accent'])])

        columns = ('NIF', 'Nome', 'Categoria', 'Contacto', 'Limite')
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=12)

        widths = [80, 220, 120, 150, 120]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="w" if col == 'Nome' else "center")

        v_scroll = ttk.Scrollbar(parent, orient="vertical", command=self.tree.yview)
        h_scroll = ttk.Scrollbar(parent, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")

        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.tree.bind('<Double-1>', lambda e: self.editar_anunciante())

    @safe_operation()
    def load_data(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            query = """
            SELECT Num_id_fiscal, Nome_razao_soc, Cat_negocio, Contactos, Lim_cred_aprov
            FROM Anunciante_Dados 
            ORDER BY Nome_razao_soc
            """
            result = self.db.execute_query(query)

            if result and result[1]:
                for row in result[1]:
                    self.tree.insert('', 'end', values=(
                        row[0],
                        row[1],
                        row[2] if row[2] else "N/A",
                        row[3] if row[3] else "N/A",
                        f"MT {row[4]:,.2f}" if row[4] else "MT 0.00"
                    ))
                self.logger.info(f"Carregados {len(result[1])} anunciantes")
        except Exception as e:
            self.logger.error(f"Erro ao carregar anunciantes: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")

    def clear_content(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def novo_anunciante(self):
        self.open_form(mode='create')

    def editar_anunciante(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um anunciante para editar.")
            return
        item = self.tree.item(selected[0])
        fiscal = item['values'][0]
        self.open_form(mode='edit', fiscal=fiscal)

    def open_form(self, mode='create', fiscal=None):
        """Abre formulário profissional com validação"""
        form_window = ctk.CTkToplevel(self.parent)
        form_window.title("Novo Anunciante" if mode == 'create' else "Editar Anunciante")
        form_window.geometry("800x600")

        form_window.update_idletasks()
        x = (form_window.winfo_screenwidth() // 2) - (800 // 2)
        y = (form_window.winfo_screenheight() // 2) - (600 // 2)
        form_window.geometry(f"800x600+{x}+{y}")

        form_window.transient(self.parent)
        form_window.grab_set()

        form_container = ctk.CTkScrollableFrame(form_window, fg_color=COLORS['dark_bg'])
        form_container.pack(fill="both", expand=True, padx=20, pady=20)

        title_text = "Novo Anunciante" if mode == 'create' else "Editar Anunciante"
        title = ctk.CTkLabel(
            form_container,
            text=title_text,
            font=("Arial", 20, "bold"),
            text_color=COLORS['text_primary']
        )
        title.pack(pady=(0, 20))

        form_frame = ctk.CTkFrame(form_container, fg_color=COLORS['dark_card'], corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        fields = {}
        row = 0

        if mode == 'create':
            self.create_form_field(form_frame, "NIF (Número de ID Fiscal):*", row, 'fiscal', fields, width=250)
            row += 1
        else:
            self.create_form_field(form_frame, "NIF:*", row, 'fiscal', fields, width=250, readonly=True)
            row += 1

        self.create_form_field(form_frame, "Nome/Razão Social:*", row, 'nome', fields, width=500)
        row += 1

        label = ctk.CTkLabel(form_frame, text="Categoria de Negócio:*", font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        fields['categoria'] = ctk.CTkComboBox(form_frame, values=['Telecomunicações', 'Varejo', 'Alimentação', 'Saúde', 'Educação', 'Tecnologia', 'Outro'], width=350, height=35)
        fields['categoria'].grid(row=row, column=1, padx=20, pady=10, sticky="w")
        row += 1

        self.create_form_field(form_frame, "Porte da Empresa:*", row, 'porte', fields, width=250)
        row += 1

        self.create_form_field(form_frame, "Endereço:*", row, 'endereco', fields, width=500)
        row += 1

        self.create_form_field(form_frame, "Contactos (Tel/Email):*", row, 'contactos', fields, width=350)
        row += 1

        self.create_form_field(form_frame, "Representante Legal:*", row, 'rep_legal', fields, width=350)
        row += 1

        self.create_form_field(form_frame, "Limite de Crédito Aprovado (MT):*", row, 'limite', fields, width=300)
        row += 1

        label = ctk.CTkLabel(form_frame, text="Classificação Confidencial:*", font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        fields['classif'] = ctk.CTkComboBox(form_frame, values=['Confidencial', 'Público', 'Interno'], width=250, height=35)
        fields['classif'].grid(row=row, column=1, padx=20, pady=10, sticky="w")
        row += 1

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=row, column=0, columnspan=2, pady=30)

        save_btn = ctk.CTkButton(
            btn_frame,
            text="Salvar",
            command=lambda: self.save_anunciante(mode, fields, fiscal, form_window),
            font=("Arial", 14, "bold"),
            fg_color=COLORS['success'],
            width=150,
            height=40
        )
        save_btn.pack(side="left", padx=10)

        cancel_btn = ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=form_window.destroy,
            font=("Arial", 14, "bold"),
            fg_color=COLORS['danger'],
            width=150,
            height=40
        )
        cancel_btn.pack(side="left", padx=10)

        if mode == 'edit' and fiscal:
            self.load_form_data(fields, fiscal)

        self.form_fields = fields

    def create_form_field(self, parent, label_text, row, field_name, fields, width=300, readonly=False):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")

        entry = ctk.CTkEntry(parent, width=width, height=35)
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="w")

        if readonly:
            entry.configure(state="disabled")

        fields[field_name] = entry

    def load_form_data(self, fields, fiscal):
        query = """
        SELECT Num_id_fiscal, Nome_razao_soc, Cat_negocio, Porte, Endereco, 
               Contactos, Rep_legal, Lim_cred_aprov, Classif_conf
        FROM Anunciante_Dados 
        WHERE Num_id_fiscal = :fiscal
        """
        result = self.db.execute_query(query, {'fiscal': fiscal})

        if result and result[1]:
            data = result[1][0]
            fields['fiscal'].configure(state="normal")
            fields['fiscal'].insert(0, str(data[0]))
            fields['fiscal'].configure(state="disabled")
            fields['nome'].insert(0, data[1] or '')
            fields['categoria'].set(data[2] if data[2] else 'Outro')
            fields['porte'].insert(0, data[3] or '')
            fields['endereco'].insert(0, data[4] or '')
            fields['contactos'].insert(0, data[5] or '')
            fields['rep_legal'].insert(0, data[6] or '')
            fields['limite'].insert(0, str(data[7] or 0))
            fields['classif'].set(data[8] if data[8] else 'Confidencial')

    def save_anunciante(self, mode, fields, fiscal, form_window):
        """Salva com validação sólida antes de inserir na BD"""
        try:
            data = {
                'fiscal': fields.get('fiscal').get() if fields.get('fiscal').cget('state') != 'disabled' else fiscal,
                'nome': fields['nome'].get(),
                'categoria': fields['categoria'].get(),
                'porte': fields['porte'].get(),
                'endereco': fields['endereco'].get(),
                'contactos': fields['contactos'].get(),
                'rep_legal': fields['rep_legal'].get(),
                'limite': fields['limite'].get(),
                'classif': fields['classif'].get()
            }

            CRUDValidator.validate_anunciante(data)

            if mode == 'create':
                query = """
                INSERT INTO Anunciante_Dados 
                (Num_id_fiscal, Nome_razao_soc, Cat_negocio, Porte, Endereco, 
                 Contactos, Rep_legal, Lim_cred_aprov, Classif_conf)
                VALUES (:fiscal, :nome, :categoria, :porte, :endereco, 
                        :contactos, :rep_legal, :limite, :classif)
                """
                params = {
                    'fiscal': int(data['fiscal']),
                    'nome': data['nome'],
                    'categoria': data['categoria'],
                    'porte': data['porte'],
                    'endereco': data['endereco'],
                    'contactos': data['contactos'],
                    'rep_legal': data['rep_legal'],
                    'limite': float(data['limite']),
                    'classif': data['classif']
                }
                result = self.db.execute_query(query, params, fetch=False)
                if result:
                    messagebox.showinfo("Sucesso", "Anunciante criado com sucesso!")
            else:
                query = """
                UPDATE Anunciante_Dados
                SET Nome_razao_soc = :nome, Cat_negocio = :categoria, Porte = :porte,
                    Endereco = :endereco, Contactos = :contactos, Rep_legal = :rep_legal,
                    Lim_cred_aprov = :limite, Classif_conf = :classif
                WHERE Num_id_fiscal = :fiscal
                """
                params = {
                    'fiscal': fiscal,
                    'nome': data['nome'],
                    'categoria': data['categoria'],
                    'porte': data['porte'],
                    'endereco': data['endereco'],
                    'contactos': data['contactos'],
                    'rep_legal': data['rep_legal'],
                    'limite': float(data['limite']),
                    'classif': data['classif']
                }
                result = self.db.execute_query(query, params, fetch=False)
                if result:
                    messagebox.showinfo("Sucesso", "Anunciante atualizado com sucesso!")

            form_window.destroy()
            self.load_data()

        except ValidationError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            self.logger.error(f"Erro ao salvar anunciante: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def excluir_anunciante(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um anunciante para excluir.")
            return

        item = self.tree.item(selected[0])
        fiscal = item['values'][0]
        nome = item['values'][1]

        if messagebox.askyesno("Confirmar", f"Excluir '{nome}'? Esta ação não pode ser desfeita."):
            try:
                query = "DELETE FROM Anunciante_Dados WHERE Num_id_fiscal = :fiscal"
                result = self.db.execute_query(query, {'fiscal': fiscal}, fetch=False)
                if result:
                    messagebox.showinfo("Sucesso", "Anunciante excluído!")
                    self.load_data()
            except Exception as e:
                self.logger.error(f"Erro ao excluir: {str(e)}")
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")

    @staticmethod
    def darken_color(color):
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(max(0, c - 30) for c in rgb)
        return '#%02x%02x%02x' % darker_rgb

def show_anunciantes_module(parent, db, main_app):
    AnunciantesCRUD(parent, db, main_app)
