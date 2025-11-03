"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  COMPONENTE DE INTERFACE DE PESQUISA - INC MOÇAMBIQUE                        ║
║  Widget moderno com sugestões e filtros avançados                           ║
║  Grupo: Eden Magnus, Francisco Guamba, Malik Dauto, Quirson Ngale           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import customtkinter as ctk
from tkinter import messagebox, ttk
from typing import Optional, Callable, List, Dict, Any
from datetime import datetime
import threading

from config import COLORS, FONTS
from search_engine import SearchEngine, SearchCache, SearchExporter
from logger_config import app_logger


class ModernSearchBar(ctk.CTkFrame):
    """Barra de pesquisa moderna com sugestões em tempo real"""

    def __init__(
        self,
        parent,
        search_engine: SearchEngine,
        on_search: Optional[Callable] = None,
        placeholder: str = "Pesquisar em tudo...",
        **kwargs
    ):
        super().__init__(parent, **kwargs)

        self.search_engine = search_engine
        self.on_search_callback = on_search
        self.cache = SearchCache()
        self.sugestoes_window = None
        self.search_thread = None

        self.configure(fg_color="transparent")
        self._create_widgets(placeholder)

    def _create_widgets(self, placeholder: str):
        """Cria componentes da barra de pesquisa"""

        # Container principal
        search_container = ctk.CTkFrame(
            self,
            fg_color=COLORS['dark_card'],
            corner_radius=25,
            border_width=2,
            border_color=COLORS['dark_border']
        )
        search_container.pack(fill="x", padx=10, pady=10)

        # Ícone de pesquisa
        ctk.CTkLabel(
            search_container,
            text="🔍",
            font=("Arial", 20),
            text_color=COLORS['text_secondary']
        ).pack(side="left", padx=(20, 10))

        # Campo de entrada
        self.search_entry = ctk.CTkEntry(
            search_container,
            placeholder_text=placeholder,
            font=("Arial", 14),
            fg_color="transparent",
            border_width=0,
            height=50
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Bind events
        self.search_entry.bind('<KeyRelease>', self._on_key_release)
        self.search_entry.bind('<Return>', self._on_enter)
        self.search_entry.bind('<FocusIn>', self._on_focus_in)
        self.search_entry.bind('<FocusOut>', self._on_focus_out)

        # Botão de filtros
        self.filter_btn = ctk.CTkButton(
            search_container,
            text="⚙️",
            width=50,
            height=50,
            font=("Arial", 18),
            fg_color="transparent",
            hover_color=COLORS['dark_hover'],
            command=self._show_advanced_filters
        )
        self.filter_btn.pack(side="right", padx=5)

        # Botão de pesquisa
        self.search_btn = ctk.CTkButton(
            search_container,
            text="Pesquisar",
            width=120,
            height=50,
            font=("Arial", 13, "bold"),
            fg_color=COLORS['accent'],
            hover_color=COLORS['primary'],
            command=self._perform_search
        )
        self.search_btn.pack(side="right", padx=(5, 15))

    def _on_key_release(self, event):
        """Evento ao soltar tecla - mostra sugestões"""
        termo = self.search_entry.get().strip()

        # Fecha sugestões se termo muito curto
        if len(termo) < 2:
            self._hide_suggestions()
            return

        # Cancela thread anterior se existir
        if self.search_thread and self.search_thread.is_alive():
            return

        # Busca sugestões em thread
        self.search_thread = threading.Thread(
            target=self._load_suggestions,
            args=(termo,),
            daemon=True
        )
        self.search_thread.start()

    def _load_suggestions(self, termo: str):
        """Carrega sugestões em background"""
        sugestoes = self.search_engine.obter_sugestoes(termo, limite=8)

        # Atualiza UI na thread principal
        self.after(0, lambda: self._show_suggestions(sugestoes))

    def _show_suggestions(self, sugestoes: List[Dict[str, str]]):
        """Mostra janela de sugestões"""
        if not sugestoes or not self.search_entry.get().strip():
            self._hide_suggestions()
            return

        # Cria/atualiza janela de sugestões
        if not self.sugestoes_window or not self.sugestoes_window.winfo_exists():
            self.sugestoes_window = ctk.CTkToplevel(self)
            self.sugestoes_window.withdraw()
            self.sugestoes_window.overrideredirect(True)

            # Frame com sombra
            self.sug_frame = ctk.CTkFrame(
                self.sugestoes_window,
                fg_color=COLORS['dark_card'],
                corner_radius=12,
                border_width=1,
                border_color=COLORS['dark_border']
            )
            self.sug_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Limpa sugestões anteriores
        for widget in self.sug_frame.winfo_children():
            widget.destroy()

        # Adiciona sugestões
        for sug in sugestoes:
            sug_btn = ctk.CTkButton(
                self.sug_frame,
                text=f"{sug['icon']}  {sug['texto']}",
                font=("Arial", 12),
                anchor="w",
                fg_color="transparent",
                hover_color=COLORS['dark_hover'],
                height=40,
                command=lambda t=sug['texto']: self._select_suggestion(t)
            )
            sug_btn.pack(fill="x", padx=5, pady=2)

        # Posiciona janela
        self._position_suggestions_window()
        self.sugestoes_window.deiconify()

    def _position_suggestions_window(self):
        """Posiciona janela de sugestões abaixo do campo"""
        self.update_idletasks()

        x = self.search_entry.winfo_rootx()
        y = self.search_entry.winfo_rooty() + self.search_entry.winfo_height() + 5
        width = self.search_entry.winfo_width() + 100

        self.sugestoes_window.geometry(f"{width}x300+{x}+{y}")

    def _hide_suggestions(self):
        """Esconde janela de sugestões"""
        if self.sugestoes_window and self.sugestoes_window.winfo_exists():
            self.sugestoes_window.withdraw()

    def _select_suggestion(self, texto: str):
        """Seleciona uma sugestão"""
        self.search_entry.delete(0, 'end')
        self.search_entry.insert(0, texto)
        self._hide_suggestions()
        self._perform_search()

    def _on_focus_in(self, event):
        """Evento ao focar no campo"""
        termo = self.search_entry.get().strip()
        if len(termo) >= 2:
            self._load_suggestions(termo)

    def _on_focus_out(self, event):
        """Evento ao desfocar do campo"""
        # Delay para permitir clique nas sugestões
        self.after(200, self._hide_suggestions)

    def _on_enter(self, event):
        """Evento ao pressionar Enter"""
        self._perform_search()

    def _perform_search(self):
        """Executa pesquisa"""
        termo = self.search_entry.get().strip()

        # Valida termo
        valido, mensagem = self.search_engine.validar_termo(termo)
        if not valido:
            messagebox.showwarning("Pesquisa", mensagem)
            return

        # Esconde sugestões
        self._hide_suggestions()

        # Callback externo
        if self.on_search_callback:
            self.on_search_callback(termo, None)

    def _show_advanced_filters(self):
        """Mostra janela de filtros avançados"""
        AdvancedSearchDialog(self, self.search_engine, self.on_search_callback)

    def get_termo(self) -> str:
        """Retorna termo atual"""
        return self.search_entry.get().strip()

    def clear(self):
        """Limpa campo de pesquisa"""
        self.search_entry.delete(0, 'end')
        self._hide_suggestions()


class AdvancedSearchDialog(ctk.CTkToplevel):
    """Janela de pesquisa avançada com filtros"""

    def __init__(self, parent, search_engine: SearchEngine, callback: Callable):
        super().__init__(parent)

        self.search_engine = search_engine
        self.callback = callback

        self.title("Pesquisa Avançada")
        self.geometry("600x500")
        self.resizable(False, False)
        self._center_window()

        self._create_widgets()

    def _center_window(self):
        """Centraliza janela"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.winfo_screenheight() // 2) - (500 // 2)
        self.geometry(f"600x500+{x}+{y}")

    def _create_widgets(self):
        """Cria interface de filtros"""

        # Header
        header = ctk.CTkFrame(self, fg_color=COLORS['primary'], height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="🔍 Pesquisa Avançada",
            font=("Arial", 20, "bold"),
            text_color=COLORS['text_primary']
        ).pack(pady=25)

        # Conteúdo
        content = ctk.CTkFrame(self, fg_color=COLORS['dark_bg'])
        content.pack(fill="both", expand=True, padx=20, pady=20)

        # Termo de pesquisa
        ctk.CTkLabel(
            content,
            text="Termo de pesquisa:",
            font=("Arial", 12, "bold"),
            text_color=COLORS['text_primary']
        ).pack(anchor="w", pady=(10, 5))

        self.termo_entry = ctk.CTkEntry(
            content,
            font=("Arial", 13),
            height=40
        )
        self.termo_entry.pack(fill="x", pady=(0, 15))

        # Tipo de registro
        ctk.CTkLabel(
            content,
            text="Tipo de registro:",
            font=("Arial", 12, "bold"),
            text_color=COLORS['text_primary']
        ).pack(anchor="w", pady=(10, 5))

        tipos = ['TODOS'] + [t['tipo'] for t in self.search_engine.get_tipos_registro()]
        self.tipo_combo = ctk.CTkComboBox(
            content,
            values=tipos,
            font=("Arial", 12),
            height=40
        )
        self.tipo_combo.set('TODOS')
        self.tipo_combo.pack(fill="x", pady=(0, 15))

        # Filtro de datas
        date_frame = ctk.CTkFrame(content, fg_color="transparent")
        date_frame.pack(fill="x", pady=(10, 15))

        # Data início
        left_frame = ctk.CTkFrame(date_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkLabel(
            left_frame,
            text="Data início:",
            font=("Arial", 11),
            text_color=COLORS['text_secondary']
        ).pack(anchor="w")

        self.data_inicio = ctk.CTkEntry(
            left_frame,
            placeholder_text="DD/MM/AAAA",
            font=("Arial", 12),
            height=35
        )
        self.data_inicio.pack(fill="x")

        # Data fim
        right_frame = ctk.CTkFrame(date_frame, fg_color="transparent")
        right_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            right_frame,
            text="Data fim:",
            font=("Arial", 11),
            text_color=COLORS['text_secondary']
        ).pack(anchor="w")

        self.data_fim = ctk.CTkEntry(
            right_frame,
            placeholder_text="DD/MM/AAAA",
            font=("Arial", 12),
            height=35
        )
        self.data_fim.pack(fill="x")

        # Botões
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", pady=20)

        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=self.destroy,
            font=("Arial", 12),
            fg_color=COLORS['secondary'],
            hover_color=COLORS['secondary_dark'],
            height=40,
            width=150
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="🔍 Pesquisar",
            command=self._execute_search,
            font=("Arial", 12, "bold"),
            fg_color=COLORS['accent'],
            hover_color=COLORS['primary'],
            height=40,
            width=150
        ).pack(side="right", padx=5)

    def _execute_search(self):
        """Executa pesquisa avançada"""
        termo = self.termo_entry.get().strip()

        if not termo:
            messagebox.showwarning("Atenção", "Digite um termo para pesquisar")
            return

        tipo = None if self.tipo_combo.get() == 'TODOS' else self.tipo_combo.get()

        # Parse datas (simplificado)
        data_inicio = None
        data_fim = None

        # Callback
        if self.callback:
            self.callback(termo, tipo, data_inicio, data_fim)

        self.destroy()


class SearchResultsView(ctk.CTkFrame):
    """Visualizador de resultados de pesquisa"""

    def __init__(self, parent, search_engine: SearchEngine, **kwargs):
        super().__init__(parent, **kwargs)

        self.search_engine = search_engine
        self.current_results = []

        self.configure(fg_color="transparent")
        self._create_widgets()

    def _create_widgets(self):
        """Cria interface de resultados"""

        # Header com estatísticas
        self.header_frame = ctk.CTkFrame(
            self,
            fg_color=COLORS['dark_card'],
            corner_radius=12,
            height=80
        )
        self.header_frame.pack(fill="x", padx=10, pady=(0, 10))
        self.header_frame.pack_propagate(False)

        header_content = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=20, pady=15)

        self.results_label = ctk.CTkLabel(
            header_content,
            text="📊 Nenhuma pesquisa realizada",
            font=("Arial", 16, "bold"),
            text_color=COLORS['text_primary']
        )
        self.results_label.pack(side="left")

        # Botões de ação
        action_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        action_frame.pack(side="right")

        self.export_btn = ctk.CTkButton(
            action_frame,
            text="📥 Exportar",
            command=self._export_results,
            font=("Arial", 11),
            fg_color=COLORS['secondary'],
            hover_color=COLORS['secondary_dark'],
            width=100,
            height=35,
            state="disabled"
        )
        self.export_btn.pack(side="right", padx=5)

        # Área de resultados com scroll
        results_container = ctk.CTkFrame(self, fg_color="transparent")
        results_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.results_scroll = ctk.CTkScrollableFrame(
            results_container,
            fg_color=COLORS['dark_bg'],
            corner_radius=0
        )
        self.results_scroll.pack(fill="both", expand=True)

    def display_results(self, termo: str, resultados: List[Dict[str, Any]]):
        """Exibe resultados da pesquisa"""
        self.current_results = resultados

        # Atualiza header
        count = len(resultados)
        self.results_label.configure(
            text=f"🔍 '{termo}' - {count} resultado{'s' if count != 1 else ''} encontrado{'s' if count != 1 else ''}"
        )

        # Habilita/desabilita exportação
        if count > 0:
            self.export_btn.configure(state="normal")
        else:
            self.export_btn.configure(state="disabled")

        # Limpa resultados anteriores
        for widget in self.results_scroll.winfo_children():
            widget.destroy()

        if not resultados:
            self._show_no_results()
            return

        # Exibe resultados
        for resultado in resultados:
            self._create_result_card(resultado)

    def _show_no_results(self):
        """Mostra mensagem de nenhum resultado"""
        no_results = ctk.CTkFrame(
            self.results_scroll,
            fg_color=COLORS['dark_card'],
            corner_radius=12,
            height=200
        )
        no_results.pack(fill="x", padx=20, pady=20)

        content = ctk.CTkFrame(no_results, fg_color="transparent")
        content.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(
            content,
            text="🔍",
            font=("Arial", 48),
            text_color=COLORS['text_secondary']
        ).pack(pady=10)

        ctk.CTkLabel(
            content,
            text="Nenhum resultado encontrado",
            font=("Arial", 16, "bold"),
            text_color=COLORS['text_primary']
        ).pack()

        ctk.CTkLabel(
            content,
            text="Tente usar termos diferentes ou filtros menos restritivos",
            font=("Arial", 11),
            text_color=COLORS['text_secondary']
        ).pack(pady=5)

    def _create_result_card(self, resultado: Dict[str, Any]):
        """Cria card para cada resultado"""
        card = ctk.CTkFrame(
            self.results_scroll,
            fg_color=COLORS['dark_card'],
            corner_radius=12,
            border_width=1,
            border_color=COLORS['dark_border']
        )
        card.pack(fill="x", padx=20, pady=8)

        # Conteúdo do card
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=15)

        # Header do card
        header = ctk.CTkFrame(content, fg_color="transparent")
        header.pack(fill="x", pady=(0, 10))

        # Ícone e tipo
        icon_label = ctk.CTkLabel(
            header,
            text=f"{resultado.get('icon', '📄')} {resultado.get('tipo', 'N/A')}",
            font=("Arial", 12),
            text_color=COLORS['accent']
        )
        icon_label.pack(side="left")

        # ID
        id_label = ctk.CTkLabel(
            header,
            text=f"ID: {resultado.get('id', 'N/A')}",
            font=("Arial", 10),
            text_color=COLORS['text_disabled']
        )
        id_label.pack(side="right")

        # Título
        title_label = ctk.CTkLabel(
            content,
            text=resultado.get('titulo', 'Sem título'),
            font=("Arial", 15, "bold"),
            text_color=COLORS['text_primary'],
            anchor="w"
        )
        title_label.pack(fill="x", pady=(0, 5))

        # Subtítulo
        if 'subtitulo' in resultado:
            subtitle_label = ctk.CTkLabel(
                content,
                text=resultado['subtitulo'],
                font=("Arial", 12),
                text_color=COLORS['text_secondary'],
                anchor="w"
            )
            subtitle_label.pack(fill="x", pady=(0, 5))

        # Footer com data e ações
        footer = ctk.CTkFrame(content, fg_color="transparent")
        footer.pack(fill="x", pady=(10, 0))

        if 'data' in resultado:
            date_label = ctk.CTkLabel(
                footer,
                text=f"📅 {resultado['data']}",
                font=("Arial", 10),
                text_color=COLORS['text_disabled']
            )
            date_label.pack(side="left")

        # Botão ver detalhes
        details_btn = ctk.CTkButton(
            footer,
            text="Ver Detalhes →",
            command=lambda r=resultado: self._show_details(r),
            font=("Arial", 11),
            fg_color="transparent",
            hover_color=COLORS['dark_hover'],
            text_color=COLORS['accent'],
            width=100,
            height=30
        )
        details_btn.pack(side="right")

    def _show_details(self, resultado: Dict[str, Any]):
        """Mostra detalhes de um resultado"""
        # TODO: Implementar janela de detalhes
        messagebox.showinfo(
            "Detalhes",
            f"Tipo: {resultado.get('tipo')}\n"
            f"ID: {resultado.get('id')}\n"
            f"Título: {resultado.get('titulo')}"
        )

    def _export_results(self):
        """Exporta resultados"""
        if not self.current_results:
            return

        # Dialog simples de exportação
        exporter = SearchExporter()

        if messagebox.askyesno("Exportar", "Deseja exportar os resultados para CSV?"):
            success = exporter.para_csv(self.current_results, "pesquisa_resultados.csv")

            if success:
                messagebox.showinfo("Sucesso", "Resultados exportados com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao exportar resultados")


# =============================================================================
# FIM DO MÓDULO
# =============================================================================