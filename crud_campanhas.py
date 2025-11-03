"""
MÓDULO CAMPANHAS - CRUD COM VALIDAÇÃO SÓLIDA
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
from tkcalendar import DateEntry
from logger_config import log_execution, safe_operation, app_logger
from config import COLORS
from crud_validators import CRUDValidator, ValidationError

class CampanhasCRUD:
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

        ctk.CTkLabel(title_frame, text="Gestão de Campanhas", font=("Arial", 22, "bold"), text_color=COLORS['text_primary']).pack(side="left")

        self.create_toolbar(container)
        self.create_campanhas_table(container)

    @log_execution
    def create_toolbar(self, parent):
        toolbar = ctk.CTkFrame(parent, fg_color=COLORS['dark_card'], corner_radius=10, height=70)
        toolbar.pack(fill="x", pady=(0, 20))
        toolbar.pack_propagate(False)

        btn_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame.pack(expand=True, padx=20, pady=12)

        buttons = [
            ("Nova Campanha", self.nova_campanha, COLORS['success']),
            ("Editar", self.editar_campanha, COLORS['primary']),
            ("Excluir", self.excluir_campanha, COLORS['danger']),
            ("Atualizar", self.load_data, COLORS['accent']),
        ]

        for text, command, color in buttons:
            btn = ctk.CTkButton(btn_frame, text=text, command=command, font=("Arial", 12, "bold"),
                               fg_color=color, hover_color=self.darken_color(color), width=140, height=38, corner_radius=8)
            btn.pack(side="left", padx=8)

    @log_execution
    def create_campanhas_table(self, parent):
        table_frame = ctk.CTkFrame(parent, fg_color=COLORS['dark_card'], corner_radius=12)
        table_frame.pack(fill="both", expand=True, pady=10)

        header_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=15)

        ctk.CTkLabel(header_frame, text="Lista de Campanhas", font=("Arial", 18, "bold"), text_color=COLORS['text_primary']).pack(side="left")

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

        columns = ('Código', 'Título', 'Anunciante', 'Orçamento', 'Início', 'Término', 'Status')
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=12)

        widths = [80, 200, 150, 120, 100, 100, 100]
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

        self.tree.bind('<Double-1>', lambda e: self.editar_campanha())

    @safe_operation()
    def load_data(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            query = """
            SELECT c.Cod_camp, c.Titulo, a.Nome_razao_soc, c.Orc_alocado,
                   TO_CHAR(c.Data_inicio, 'DD/MM/YYYY'), TO_CHAR(c.Data_termino, 'DD/MM/YYYY'),
                   CASE WHEN c.Data_termino >= SYSDATE THEN 'Ativa' ELSE 'Finalizada' END
            FROM Campanha_dados c
            JOIN Anunciante_dados a ON c.Num_id_fiscal = a.Num_id_fiscal
            ORDER BY c.Data_inicio DESC
            """
            result = self.db.execute_query(query)

            if result and result[1]:
                for row in result[1]:
                    self.tree.insert('', 'end', values=(
                        str(row[0]), row[1], row[2], f"MT {row[3]:,.2f}", row[4], row[5], row[6]
                    ))
                self.logger.info(f"Carregadas {len(result[1])} campanhas")
        except Exception as e:
            self.logger.error(f"Erro ao carregar campanhas: {str(e)}")

    def clear_content(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

    def nova_campanha(self):
        self.open_form(mode='create')

    def editar_campanha(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma campanha.")
            return
        cod = self.tree.item(selected[0])['values'][0]
        self.open_form(mode='edit', cod_camp=cod)

    def open_form(self, mode='create', cod_camp=None):
        form_window = ctk.CTkToplevel(self.parent)
        form_window.title("Nova Campanha" if mode == 'create' else "Editar Campanha")
        form_window.geometry("850x750")

        form_window.update_idletasks()
        x = (form_window.winfo_screenwidth() // 2) - (850 // 2)
        y = (form_window.winfo_screenheight() // 2) - (750 // 2)
        form_window.geometry(f"850x750+{x}+{y}")

        form_window.transient(self.parent)
        form_window.grab_set()

        form_container = ctk.CTkScrollableFrame(form_window, fg_color=COLORS['dark_bg'])
        form_container.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(form_container, text="Nova Campanha" if mode == 'create' else "Editar Campanha",
                    font=("Arial", 20, "bold"), text_color=COLORS['text_primary']).pack(pady=(0, 20))

        form_frame = ctk.CTkFrame(form_container, fg_color=COLORS['dark_card'], corner_radius=10)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        fields = {}
        row = 0

        if mode == 'edit':
            self.create_form_field(form_frame, "Código:", row, 'cod_camp', fields, readonly=True)
            row += 1

        label = ctk.CTkLabel(form_frame, text="Anunciante:*", font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        fields['anunciante'] = ctk.CTkComboBox(form_frame, values=self.get_anunciantes(), width=300, height=35)
        fields['anunciante'].grid(row=row, column=1, padx=20, pady=10, sticky="w")
        row += 1

        self.create_form_field(form_frame, "Título:*", row, 'titulo', fields, width=500)
        row += 1

        label = ctk.CTkLabel(form_frame, text="Objetivo:*", font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="nw")
        fields['objectivo'] = ctk.CTkTextbox(form_frame, width=500, height=60)
        fields['objectivo'].grid(row=row, column=1, padx=20, pady=10, sticky="w")
        row += 1

        self.create_form_field(form_frame, "Público-Alvo:*", row, 'pub_alvo', fields, width=500)
        row += 1

        self.create_form_field(form_frame, "Orçamento Alocado (MT):*", row, 'orc_alocado', fields, width=200)
        row += 1

        label = ctk.CTkLabel(form_frame, text="Data Início:*", font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        fields['data_inicio'] = DateEntry(form_frame, width=25, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        fields['data_inicio'].grid(row=row, column=1, padx=20, pady=10, sticky="w")
        row += 1

        label = ctk.CTkLabel(form_frame, text="Data Término:*", font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        fields['data_termino'] = DateEntry(form_frame, width=25, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        fields['data_termino'].grid(row=row, column=1, padx=20, pady=10, sticky="w")
        row += 1

        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=row, column=0, columnspan=2, pady=30)

        ctk.CTkButton(btn_frame, text="Salvar", command=lambda: self.save_campanha(mode, fields, cod_camp, form_window),
                     font=("Arial", 14, "bold"), fg_color=COLORS['success'], width=150, height=40).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Cancelar", command=form_window.destroy, font=("Arial", 14, "bold"),
                     fg_color=COLORS['danger'], width=150, height=40).pack(side="left", padx=10)

        if mode == 'edit' and cod_camp:
            self.load_form_data(fields, cod_camp)

    def create_form_field(self, parent, label_text, row, field_name, fields, width=300, readonly=False):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 12, "bold"), text_color=COLORS['text_primary'])
        label.grid(row=row, column=0, padx=20, pady=10, sticky="w")
        entry = ctk.CTkEntry(parent, width=width, height=35)
        entry.grid(row=row, column=1, padx=20, pady=10, sticky="w")
        if readonly:
            entry.configure(state="disabled")
        fields[field_name] = entry

    def get_anunciantes(self):
        query = "SELECT Num_id_fiscal, Nome_razao_soc FROM Anunciante_dados ORDER BY Nome_razao_soc"
        result = self.db.execute_query(query)
        if result and result[1]:
            return [f"{row[0]} - {row[1]}" for row in result[1]]
        return []

    def load_form_data(self, fields, cod_camp):
        query = """
        SELECT Cod_camp, Num_id_fiscal, Titulo, Objectivo, Pub_alvo, Orc_alocado, Data_inicio, Data_termino
        FROM Campanha_dados WHERE Cod_camp = :cod
        """
        result = self.db.execute_query(query, {'cod': cod_camp})
        if result and result[1]:
            data = result[1][0]
            fields['cod_camp'].configure(state="normal")
            fields['cod_camp'].insert(0, str(data[0]))
            fields['cod_camp'].configure(state="disabled")
            fields['anunciante'].set(f"{data[1]} - {self.get_anunciante_name(data[1])}")
            fields['titulo'].insert(0, data[2] or '')
            fields['objectivo'].insert("1.0", data[3] or '')
            fields['pub_alvo'].insert(0, data[4] or '')
            fields['orc_alocado'].insert(0, str(data[5] or 0))
            if data[6]:
                fields['data_inicio'].set_date(data[6])
            if data[7]:
                fields['data_termino'].set_date(data[7])

    def get_anunciante_name(self, fiscal):
        query = "SELECT Nome_razao_soc FROM Anunciante_dados WHERE Num_id_fiscal = :fiscal"
        result = self.db.execute_query(query, {'fiscal': fiscal})
        return result[1][0][0] if result and result[1] else ""

    def save_campanha(self, mode, fields, cod_camp, form_window):
        try:
            anunciante_str = fields['anunciante'].get()
            if not anunciante_str or " - " not in anunciante_str:
                messagebox.showerror("Erro", "Selecione um anunciante válido.")
                return

            num_fiscal = int(anunciante_str.split(" - ")[0])

            data = {
                'anunciante': num_fiscal,
                'titulo': fields['titulo'].get(),
                'objectivo': fields['objectivo'].get("1.0", "end-1c"),
                'pub_alvo': fields['pub_alvo'].get(),
                'orc_alocado': fields['orc_alocado'].get(),
                'data_inicio': fields['data_inicio'].get_date().strftime('%d/%m/%Y'),
                'data_termino': fields['data_termino'].get_date().strftime('%d/%m/%Y')
            }

            CRUDValidator.validate_campanha(data)

            if mode == 'create':
                # 🆕 USA SEQUENCE EM VEZ DE MAX()+1
                query_cod = "SELECT seq_campanha.NEXTVAL FROM DUAL"
                result = self.db.execute_query(query_cod)
                novo_cod = result[1][0][0] if result and result[1] else 8000001

                query = """
                        INSERT INTO Campanha_dados (Cod_camp, Num_id_fiscal, Titulo, Objectivo, Pub_alvo, Orc_alocado, \
                                                    Data_inicio, Data_termino)
                        VALUES (:cod, :fiscal, :titulo, :obj, :pub, :orc, TO_DATE(:dt_ini, 'DD/MM/YYYY'), \
                                TO_DATE(:dt_fim, 'DD/MM/YYYY')) \
                        """
                params = {
                    'cod': novo_cod,
                    'fiscal': data['anunciante'],
                    'titulo': data['titulo'],
                    'obj': data['objectivo'],
                    'pub': data['pub_alvo'],
                    'orc': float(data['orc_alocado']),
                    'dt_ini': data['data_inicio'],
                    'dt_fim': data['data_termino']
                }
                self.db.execute_query(query, params, fetch=False)
                messagebox.showinfo("Sucesso", f"✅ Campanha criada com ID: {novo_cod}")
            else:
                query = """
                UPDATE Campanha_dados SET Num_id_fiscal = :fiscal, Titulo = :titulo, Objectivo = :obj,
                Pub_alvo = :pub, Orc_alocado = :orc, Data_inicio = TO_DATE(:dt_ini, 'DD/MM/YYYY'),
                Data_termino = TO_DATE(:dt_fim, 'DD/MM/YYYY') WHERE Cod_camp = :cod
                """
                params = {
                    'cod': cod_camp,
                    'fiscal': data['anunciante'],
                    'titulo': data['titulo'],
                    'obj': data['objectivo'],
                    'pub': data['pub_alvo'],
                    'orc': float(data['orc_alocado']),
                    'dt_ini': data['data_inicio'],
                    'dt_fim': data['data_termino']
                }
                self.db.execute_query(query, params, fetch=False)
                messagebox.showinfo("Sucesso", "Campanha atualizada com sucesso!")

            form_window.destroy()
            self.load_data()

        except ValidationError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            self.logger.error(f"Erro ao salvar campanha: {str(e)}")
            messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")

    def excluir_campanha(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione uma campanha.")
            return

        cod = self.tree.item(selected[0])['values'][0]
        titulo = self.tree.item(selected[0])['values'][1]

        if messagebox.askyesno("Confirmar", f"Excluir '{titulo}'? Esta ação não pode ser desfeita."):
            try:
                query = "DELETE FROM Campanha_dados WHERE Cod_camp = :cod"
                self.db.execute_query(query, {'cod': cod}, fetch=False)
                messagebox.showinfo("Sucesso", "Campanha excluída!")
                self.load_data()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir: {str(e)}")

    @staticmethod
    def darken_color(color):
        color = color.lstrip('#')
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(max(0, c - 30) for c in rgb)
        return '#%02x%02x%02x' % darker_rgb

def show_campanhas_module(parent, db, main_app):
    CampanhasCRUD(parent, db, main_app)
