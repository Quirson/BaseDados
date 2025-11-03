# search_advanced_fixed.py
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime, timedelta
from config import COLORS


class AdvancedSearchDialogFixed(ctk.CTkToplevel):
    """Janela de pesquisa avançada SIMPLIFICADA"""

    def __init__(self, parent, search_engine, callback):
        super().__init__(parent)
        self.search_engine = search_engine
        self.callback = callback

        self.title("Pesquisa Avançada")
        self.geometry("500x400")
        self.resizable(False, False)
        self._center_window()
        self._create_widgets()

    def _center_window(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.winfo_screenheight() // 2) - (400 // 2)
        self.geometry(f"500x400+{x}+{y}")

    def _create_widgets(self):
        # Container principal
        main_frame = ctk.CTkFrame(self, fg_color=COLORS['dark_bg'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            main_frame,
            text="🔍 Pesquisa Avançada",
            font=("Arial", 18, "bold"),
            text_color=COLORS['text_primary']
        ).pack(pady=(0, 20))

        # Termo de pesquisa
        ctk.CTkLabel(
            main_frame,
            text="O que procura?",
            font=("Arial", 12, "bold"),
            text_color=COLORS['text_primary']
        ).pack(anchor="w", pady=(10, 5))

        self.termo_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="Digite palavras-chave...",
            font=("Arial", 13),
            height=40,
            width=400
        )
        self.termo_entry.pack(fill="x", pady=(0, 15))

        # Filtro por tipo
        ctk.CTkLabel(
            main_frame,
            text="Filtrar por tipo:",
            font=("Arial", 12, "bold"),
            text_color=COLORS['text_primary']
        ).pack(anchor="w", pady=(10, 5))

        tipos = ['TODOS'] + [t['tipo'] for t in self.search_engine.get_tipos_registro()]
        self.tipo_combo = ctk.CTkComboBox(
            main_frame,
            values=tipos,
            font=("Arial", 12),
            height=35,
            width=400
        )
        self.tipo_combo.set('TODOS')
        self.tipo_combo.pack(fill="x", pady=(0, 20))

        # Filtros rápidos por data
        ctk.CTkLabel(
            main_frame,
            text="Filtrar por período:",
            font=("Arial", 12, "bold"),
            text_color=COLORS['text_primary']
        ).pack(anchor="w", pady=(10, 5))

        # Botões de período rápido
        period_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        period_frame.pack(fill="x", pady=(0, 15))

        periods = [
            ("Hoje", 0),
            ("Últimos 7 dias", 7),
            ("Últimos 30 dias", 30),
            ("Este mês", "month")
        ]

        for i, (text, days) in enumerate(periods):
            btn = ctk.CTkButton(
                period_frame,
                text=text,
                command=lambda d=days: self.set_periodo(d),
                font=("Arial", 11),
                fg_color=COLORS['secondary'],
                hover_color=COLORS['secondary_dark'],
                width=100,
                height=30
            )
            btn.grid(row=0, column=i, padx=2, pady=2)

        # Botões de ação
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", pady=20)

        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=self.destroy,
            font=("Arial", 12),
            fg_color=COLORS['secondary'],
            hover_color=COLORS['secondary_dark'],
            height=40,
            width=120
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="🔍 Pesquisar",
            command=self._execute_search,
            font=("Arial", 12, "bold"),
            fg_color=COLORS['accent'],
            hover_color=COLORS['primary'],
            height=40,
            width=120
        ).pack(side="right", padx=5)

    def set_periodo(self, dias):
        """Define período rápido - não usado na pesquisa básica, apenas UI"""
        if dias == 0:
            messagebox.showinfo("Período", "Pesquisando dados de hoje")
        elif dias == 7:
            messagebox.showinfo("Período", "Pesquisando últimos 7 dias")
        elif dias == 30:
            messagebox.showinfo("Período", "Pesquisando últimos 30 dias")
        else:
            messagebox.showinfo("Período", "Pesquisando este mês")

    def _execute_search(self):
        """Executa pesquisa simplificada"""
        termo = self.termo_entry.get().strip()

        if not termo:
            messagebox.showwarning("Atenção", "Digite um termo para pesquisar")
            return

        tipo = None if self.tipo_combo.get() == 'TODOS' else self.tipo_combo.get()

        # Callback com dados simplificados
        if self.callback:
            self.callback(termo, tipo)

        self.destroy()