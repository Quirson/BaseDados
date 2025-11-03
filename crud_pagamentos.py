"""
MÓDULO PAGAMENTOS - CRUD COMPLETO COM VALIDAÇÃO
Gerencia pagamentos, modalidades de cobrança e reconciliação financeira
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
from logger_config import log_execution, safe_operation, app_logger
from config import COLORS
from crud_validators import CRUDValidator, ValidationError

class PagamentosCRUD:
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

        ctk.CTkLabel(title_frame, text="Gestão de Pagamentos", font=("Arial", 22, "bold"), text_color=COLORS['text_primary']).pack(side="left")

        self.create_toolbar(container)
        self.create_pagamentos_table(container)

    @log_execution
    def create_toolbar(self, parent):
        toolbar = ctk.CTkFrame(parent, fg_color=COLORS['dark_card'], corner_radius=10, height=70)
        toolbar.pack(fill="x", pady=(0, 20))
        toolbar.pack_propagate(False)

        btn_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame.pack(expand=True, padx=20, pady=12)

        buttons = [
            ("Novo Pagamento", self.novo_pagamento, COLORS['success']),
            ("Editar", self.editar_pagamento, COLORS['primary']),
            ("Excluir", self.excluir_pagamento, COLORS['danger']),
            ("Atualizar", self.load_data, COLORS['accent']),
        ]

        for text, command, color in buttons:
            btn = ctk.CTkButton(btn_frame, text=text, command=command, font=("Arial", 12, "bold"),
                               fg_color=color, hover_color=self.darken_color(color), width=140, height=38, corner_radius=8)
            btn.pack(side="left", padx=8)

    @log_execution
    def create_pagamentos_table(self, parent):
        table_frame = ctk.CTkFrame(parent, fg_color=COLORS['dark_card'], corner_radius=12)
        table_frame.pack(fill="both", expand=True, pady=10)

        header_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(header_frame, text="Lista de Pagamentos", font=("Arial", 18, "bold"), text_color=COLORS['text_primary']).pack(side="left")

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

        columns = ('Código', 'Preço Dinâmico', 'Método', 'Comprovante', 'Reconciliação')
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=12)

        widths = [80, 140, 120, 180, 150]
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

        self.tree.bind('<Double-1>', lambda e: self.editar_pagamento())

    @safe_operation()
    def load_data(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            query = """
            SELECT Cod_pagamento, Precos_dinam, Metod_pagamento, Comprov_veic, Reconc_financ
            FROM Pagamentos
            ORDER BY Cod_pagamento DESC
            """
            result = self.db.execute_query(query)

            if result and result[1]:
                for row in result[1]:
                    self.tree.insert('', 'end', values=(
                        str(row[0]),
                        f"MT {row[1]:,.2f}" if row[1] else "MT 0.00",
                        row[2] or "N/A",
                        row[3] or "Não enviado",
                        row[4] or "Pendente"
                    ))
                self.logger.info(f"Carregados {len(result[1])} pagamentos")
        except Exception as e:
            self.logger.error(f"Erro ao carregar pagamentos: {str(e)}")

    def clear_content(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def novo_pagamento(self):
        self.open_form(mode='create')

    def editar_pagamento(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um pagamento para editar.")
            return
        item = self.tree.item(selected[0])
        cod_pagamento = item['values'][0]
        self.open_form(mode='edit', cod_pagamento=cod_pagamento)

    def open_form(self, mode='create', cod_pagamento=None):
        form_window = ctk.CTkToplevel(self.parent)
        form_window.title("Novo Pagamento" if mode == 'create' else "Editar Pagamento")
        form_window.geometry("700x600")

        form_window.update_idletasks()
        x = (form_window.winfo_screenwidth() // 2) - (700 // 2)
        y = (form_window.winfo_screenheight() // 2) - (600 // 2)
        form_window.geometry(f"700x600+{x}+{y}")

        form_window.transient(self.parent)
        form_window.grab_set()

        form_container = ctk.CTkScrollableFrame(form_window, fg_color=COLORS['dark_bg'])
        form_container.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(form_container, text="Novo Pagamento" if mode == 'create' else "Editar Pagamento",
                    font=("Arial", 20, "bold"), text_color=COLORS['text_primary']).pack(pady=(0, 20))

        form_frame = ctk.CTkFrame(form_container, fg_color=COLORS['dark_card'], corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        fields = {}
        row = 0

        if mode == 'edit':
            self.create_form_field(form_frame, "Código:", row, 'cod_pagamento', fields, readonly=True)
            row += 1

        self.create_form_field(form_frame, "Preço Dinâmico (MT):*", row, 'preco_dinam', fields, width=300)
        row += 1

        label = ctk.CTkLabel(form_frame, text="Método de Pagamento:*", font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        fields['metodo'] = ctk.CTkComboBox(form_frame, values=['Transferência Bancária', 'Dinheiro', 'Cheque', 'Cartão de Crédito', 'Outra'], width=350, height=35)
        fields['metodo'].grid(row=row, column=1, padx=20, pady=10, sticky="w")
        row += 1

        self.create_form_field(form_frame, "Comprovante de Veiculação:", row, 'comprov', fields, width=400)
        row += 1

        label = ctk.CTkLabel(form_frame, text="Reconciliação Financeira:*", font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        fields['reconc'] = ctk.CTkComboBox(form_frame, values=['Pendente', 'Conciliado', 'Não Conciliado', 'Em Revisão'], width=350, height=35)
        fields['reconc'].grid(row=row, column=1, padx=20, pady=10, sticky="w")
        row += 1

        label = ctk.CTkLabel(form_frame, text="Modalidade de Cobrança:", font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        fields['modalidade'] = ctk.CTkComboBox(form_frame, values=self.get_modalidades(), width=350, height=35)
        fields['modalidade'].grid(row=row, column=1, padx=20, pady=10, sticky="w")
        row += 1

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=row, column=0, columnspan=2, pady=30)

        ctk.CTkButton(btn_frame, text="Salvar", command=lambda: self.save_pagamento(mode, fields, cod_pagamento, form_window),
                     font=("Arial", 14, "bold"), fg_color=COLORS['success'], width=150, height=40).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", command=form_window.destroy, font=("Arial", 14, "bold"),
                     fg_color=COLORS['danger'], width=150, height=40).pack(side="left", padx=10)

        if mode == 'edit' and cod_pagamento:
            self.load_form_data(fields, cod_pagamento)

    def create_form_field(self, parent, label_text, row, field_name, fields, width=300, readonly=False):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")

        entry = ctk.CTkEntry(parent, width=width, height=35)
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="w")

        if readonly:
            entry.configure(state="disabled")

        fields[field_name] = entry

    def get_modalidades(self):
        query = "SELECT Cod_modalidade, Modal_cobranca FROM Modalidade_cobranca ORDER BY Modal_cobranca"
        result = self.db.execute_query(query)
        if result and result[1]:
            return [f"{row[0]} - {row[1]}" for row in result[1]]
        return ['Sem Modalidades']

    def load_form_data(self, fields, cod_pagamento):
        query = """
        SELECT Cod_pagamento, Precos_dinam, Metod_pagamento, Comprov_veic, Reconc_financ, Cod_modalidade
        FROM Pagamentos WHERE Cod_pagamento = :cod
        """
        result = self.db.execute_query(query, {'cod': cod_pagamento})

        if result and result[1]:
            data = result[1][0]
            fields['cod_pagamento'].configure(state="normal")
            fields['cod_pagamento'].insert(0, str(data[0]))
            fields['cod_pagamento'].configure(state="disabled")
            fields['preco_dinam'].insert(0, str(data[1] or 0))
            fields['metodo'].set(data[2] if data[2] else 'Transferência Bancária')
            fields['comprov'].insert(0, data[3] or '')
            fields['reconc'].set(data[4] if data[4] else 'Pendente')
            if data[5]:
                modalidades = self.get_modalidades()
                for mod in modalidades:
                    if mod.startswith(str(data[5])):
                        fields['modalidade'].set(mod)
                        break

    def save_pagamento(self, mode, fields, cod_pagamento, form_window):
        try:
            data = {
                'preco_dinam': fields['preco_dinam'].get(),
                'metodo': fields['metodo'].get(),
                'comprov': fields['comprov'].get(),
                'reconc': fields['reconc'].get(),
                'modalidade': fields['modalidade'].get()
            }

            CRUDValidator.validate_pagamento(data)

            modalidade_id = None
            if data['modalidade'] and " - " in data['modalidade']:
                modalidade_id = int(data['modalidade'].split(" - ")[0])

            if mode == 'create':
                query = """
                        INSERT INTO Pagamentos (Cod_pagamento, Cod_modalidade, Precos_dinam, Metod_pagamento, \
                                                Comprov_veic, Reconc_financ)
                        VALUES (seq_pagamento.NEXTVAL, :modalidade, :preco, :metodo, :comprov, :reconc) \
                        """
                params = {
                    'modalidade': modalidade_id,
                    'preco': float(data['preco_dinam']),
                    'metodo': data['metodo'],
                    'comprov': data['comprov'] or None,
                    'reconc': data['reconc']
                }
                self.db.execute_query(query, params, fetch=False)
                messagebox.showinfo("Sucesso", "✅ Pagamento criado com SEQUENCE!")
            else:
                query = """
                UPDATE Pagamentos SET Cod_modalidade = :modalidade, Precos_dinam = :preco,
                Metod_pagamento = :metodo, Comprov_veic = :comprov, Reconc_financ = :reconc
                WHERE Cod_pagamento = :cod
                """
                params = {
                    'cod': cod_pagamento,
                    'modalidade': modalidade_id,
                    'preco': float(data['preco_dinam']),
                    'metodo': data['metodo'],
                    'comprov': data['comprov'] or None,
                    'reconc': data['reconc']
                }
                self.db.execute_query(query, params, fetch=False)
                messagebox.showinfo("Sucesso", "Pagamento atualizado com sucesso!")

            form_window.destroy()
            self.load_data()

        except ValidationError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            self.logger.error(f"Erro ao salvar pagamento: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def excluir_pagamento(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um pagamento para excluir.")
            return

        item = self.tree.item(selected[0])
        cod_pagamento = item['values'][0]
        preco = item['values'][1]

        if messagebox.askyesno("Confirmar", f"Excluir pagamento de {preco}? Esta ação não pode ser desfeita."):
            try:
                query = "DELETE FROM Pagamentos WHERE Cod_pagamento = :cod"
                self.db.execute_query(query, {'cod': cod_pagamento}, fetch=False)
                messagebox.showinfo("Sucesso", "Pagamento excluído!")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")

    @staticmethod
    def darken_color(color):
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(max(0, c - 30) for c in rgb)
        return '#%02x%02x%02x' % darker_rgb

def show_pagamentos_module(parent, db, main_app):
    PagamentosCRUD(parent, db, main_app)
