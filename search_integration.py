# search_integration.py
import customtkinter as ctk
from tkinter import messagebox
from typing import Optional, List, Dict, Any
import threading

from config import COLORS
from logger_config import app_logger, safe_operation
from search_engine import SearchEngine
from search_widget import ModernSearchBar, SearchResultsView


def integrar_pesquisa(main_app_instance):
    """
    Integra sistema de pesquisa no aplicativo principal
    """
    try:
        # Inicializa motor de pesquisa
        search_engine = SearchEngine(main_app_instance.db)
        main_app_instance.search_engine = search_engine
        app_logger.info("✅ Motor de pesquisa inicializado com sucesso")

        # Adiciona método de pesquisa global
        main_app_instance.perform_global_search = lambda termo, tipo=None: perform_search(
            main_app_instance, termo, tipo
        )

        app_logger.info("✅ Sistema de pesquisa integrado com sucesso")

    except Exception as e:
        app_logger.error(f"❌ Erro ao inicializar motor de pesquisa: {e}")
        # Cria um motor dummy para evitar erros
        main_app_instance.search_engine = None


def adicionar_barra_pesquisa_dashboard(app_instance):
    """
    Adiciona barra de pesquisa ao dashboard de forma segura
    """
    try:
        # Verifica se o motor de pesquisa está disponível
        if not hasattr(app_instance, 'search_engine') or not app_instance.search_engine:
            app_logger.warning("Motor de pesquisa não disponível para dashboard")
            return

        # Procura o container do dashboard
        dashboard_container = None
        for widget in app_instance.main_content.winfo_children():
            if isinstance(widget, ctk.CTkFrame):
                dashboard_container = widget
                break

        if not dashboard_container:
            app_logger.warning("Container do dashboard não encontrado")
            return

        # Cria barra de pesquisa
        search_bar = ModernSearchBar(
            dashboard_container,
            app_instance.search_engine,
            on_search=lambda termo, tipo=None: handle_search(app_instance, termo, tipo),
            placeholder="🔍 Pesquisar anunciantes, campanhas, peças, espaços..."
        )

        # Posiciona no topo
        search_bar.pack(side="top", fill="x", pady=(0, 20), padx=20)

        app_logger.info("✅ Barra de pesquisa adicionada ao dashboard")

    except Exception as e:
        app_logger.error(f"❌ Erro ao adicionar barra de pesquisa: {e}")


def handle_search(app_instance, termo: str, tipo: Optional[str] = None):
    """
    Manipula evento de pesquisa
    """
    # Valida termo
    if not termo or len(termo.strip()) < 2:
        messagebox.showwarning("Pesquisa", "Digite pelo menos 2 caracteres para pesquisar")
        return

    # Mostra loading
    show_loading(app_instance, termo)

    # Executa pesquisa em thread
    search_thread = threading.Thread(
        target=lambda: perform_search(app_instance, termo, tipo),
        daemon=True
    )
    search_thread.start()


def show_loading(app_instance, termo: str):
    """
    Mostra indicador de carregamento
    """
    app_instance.clear_content()
    app_instance.page_title.configure(text=f"🔍 Pesquisando: {termo}")

    loading_frame = ctk.CTkFrame(
        app_instance.main_content,
        fg_color=COLORS['dark_card'],
        corner_radius=12,
        width=400,
        height=200
    )
    loading_frame.place(relx=0.5, rely=0.5, anchor="center")

    content = ctk.CTkFrame(loading_frame, fg_color="transparent")
    content.pack(expand=True, fill="both", padx=30, pady=30)

    # Animação de loading
    loading_label = ctk.CTkLabel(
        content,
        text="🔄",
        font=("Arial", 32),
        text_color=COLORS['accent']
    )
    loading_label.pack(pady=10)

    ctk.CTkLabel(
        content,
        text="Pesquisando...",
        font=("Arial", 16, "bold"),
        text_color=COLORS['text_primary']
    ).pack(pady=5)

    ctk.CTkLabel(
        content,
        text=f"Termo: '{termo}'",
        font=("Arial", 12),
        text_color=COLORS['text_secondary']
    ).pack(pady=5)


def perform_search(app_instance, termo: str, tipo: Optional[str] = None):
    """
    Executa pesquisa e exibe resultados
    """
    try:
        # Verifica se o motor de pesquisa está disponível
        if not hasattr(app_instance, 'search_engine') or not app_instance.search_engine:
            app_instance.after(0, lambda: messagebox.showerror(
                "Erro", "Sistema de pesquisa não disponível"
            ))
            return

        # Executa pesquisa
        success, resultados = app_instance.search_engine.pesquisa_global(
            termo,
            tipo_filtro=tipo,
            limite=100
        )

        # Atualiza UI na thread principal
        app_instance.after(0, lambda: display_search_results(
            app_instance, termo, resultados, success
        ))

    except Exception as e:
        app_logger.error(f"Erro na pesquisa: {e}")
        app_instance.after(0, lambda: messagebox.showerror(
            "Erro", f"Erro ao realizar pesquisa: {str(e)}"
        ))


def display_search_results(app_instance, termo: str, resultados: List[Dict[str, Any]], success: bool):
    """
    Exibe resultados da pesquisa
    """
    if not success:
        messagebox.showerror(
            "Erro",
            "Erro ao realizar pesquisa.\nVerifique a conexão com o banco de dados."
        )
        app_instance.show_dashboard()
        return

    # Limpa conteúdo
    app_instance.clear_content()
    app_instance.page_title.configure(
        text=f"🔍 Resultados: '{termo}' ({len(resultados)} encontrado{'s' if len(resultados) != 1 else ''})"
    )

    # Container principal
    container = ctk.CTkFrame(app_instance.main_content, fg_color=COLORS['dark_bg'])
    container.pack(fill="both", expand=True, padx=20, pady=20)

    # Barra de ações
    actions_frame = ctk.CTkFrame(container, fg_color="transparent")
    actions_frame.pack(fill="x", pady=(0, 15))

    # Botão voltar
    ctk.CTkButton(
        actions_frame,
        text="← Voltar ao Dashboard",
        command=app_instance.show_dashboard,
        font=("Arial", 12),
        fg_color=COLORS['secondary'],
        hover_color=COLORS['secondary_dark'],
        width=180,
        height=35
    ).pack(side="left", padx=5)

    # Visualizador de resultados
    if hasattr(app_instance, 'search_engine'):
        results_view = SearchResultsView(container, app_instance.search_engine)
        results_view.pack(fill="both", expand=True)
        results_view.display_results(termo, resultados)
    else:
        # Fallback simples
        for resultado in resultados:
            card = ctk.CTkFrame(container, fg_color=COLORS['dark_card'], corner_radius=8)
            card.pack(fill="x", pady=5, padx=20)

            ctk.CTkLabel(
                card,
                text=f"{resultado.get('icon', '📄')} {resultado.get('titulo', 'Sem título')}",
                font=("Arial", 14, "bold"),
                text_color=COLORS['text_primary']
            ).pack(anchor="w", padx=15, pady=10)

    app_logger.info(f"✅ Exibidos {len(resultados)} resultados para '{termo}'")


def show_search_results_view(app_instance):
    """
    Mostra tela de pesquisa dedicada
    """
    app_instance.clear_content()
    app_instance.page_title.configure(text="🔍 Pesquisa Avançada")

    # Container principal
    container = ctk.CTkFrame(app_instance.main_content, fg_color=COLORS['dark_bg'])
    container.pack(fill="both", expand=True, padx=20, pady=20)

    # Título
    ctk.CTkLabel(
        container,
        text="🔍 Centro de Pesquisa",
        font=("Arial", 22, "bold"),
        text_color=COLORS['text_primary']
    ).pack(anchor="w", pady=(0, 20))

    # Barra de pesquisa
    if hasattr(app_instance, 'search_engine'):
        search_bar = ModernSearchBar(
            container,
            app_instance.search_engine,
            on_search=lambda termo, tipo: handle_search(app_instance, termo, tipo),
            placeholder="Digite sua pesquisa aqui..."
        )
        search_bar.pack(fill="x", pady=(0, 30))
    else:
        ctk.CTkLabel(
            container,
            text="Sistema de pesquisa não disponível",
            font=("Arial", 14),
            text_color=COLORS['text_secondary']
        ).pack(pady=20)