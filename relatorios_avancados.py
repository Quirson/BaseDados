# relatorios_avancados.py
import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import messagebox
from typing import Dict, Any

from config import COLORS
from logger_config import app_logger
from dashboard_stats import DashboardStats


class RelatoriosAvancados:
    """Tela de relatórios avançados usando todas as funções PL/SQL"""

    def __init__(self, parent, db_connection, main_app):
        self.parent = parent
        self.db = db_connection
        self.main_app = main_app
        self.stats_manager = DashboardStats(db_connection)

        self._create_interface()

    # 🆕 ADICIONAR ESTE MÉTODO na classe RelatoriosAvancados

    def _create_interface(self):
        """Cria interface de relatórios"""
        self.container = ctk.CTkFrame(self.parent, fg_color=COLORS['dark_bg'])
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            self.container,
            text="📊 Relatórios Avançados",
            font=("Arial", 22, "bold"),
            text_color=COLORS['text_primary']
        ).pack(anchor="w", pady=(0, 20))

        # 🆕 BOTÕES DE RELATÓRIOS
        buttons_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        buttons_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkButton(
            buttons_frame,
            text="📊 Performance de Anunciantes",
            command=self.show_performance_anunciantes,
            font=("Arial", 13, "bold"),
            fg_color=COLORS['accent'],
            hover_color=COLORS['primary'],
            height=45,
            width=250
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons_frame,
            text="📢 Campanhas Ativas",
            command=self.show_campanhas_ativas,
            font=("Arial", 13, "bold"),
            fg_color=COLORS['success'],
            hover_color=COLORS['primary'],
            height=45,
            width=250
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            buttons_frame,
            text="📈 Auditoria de Orçamentos",
            command=self.show_auditoria_orcamentos,
            font=("Arial", 13, "bold"),
            fg_color=COLORS['warning'],
            hover_color=COLORS['primary'],
            height=45,
            width=250
        ).pack(side="left", padx=5)

        # Área de resultados
        self.resultados_frame = ctk.CTkScrollableFrame(
            self.container,
            fg_color=COLORS['dark_bg']
        )
        self.resultados_frame.pack(fill="both", expand=True)

    def show_performance_anunciantes(self):
        """Mostra relatório usando VIEW v_performance_anunciantes"""
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()

        try:
            result = self.db.execute_query("SELECT * FROM v_performance_anunciantes")

            if result and result[1]:
                # Criar tabela
                style = ctk.Style()
                style.configure("Treeview", rowheight=35)

                columns = ('NIF', 'Anunciante', 'Total Campanhas', 'Orçamento Médio', 'Orçamento Total')
                tree = ctk.Treeview(self.resultados_frame, columns=columns, show='headings', height=15)

                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=150, anchor="center")

                for row in result[1]:
                    tree.insert('', 'end', values=(
                        row[0],
                        row[1],
                        row[2] or 0,
                        f"MT {row[3]:,.2f}" if row[3] else "MT 0.00",
                        f"MT {row[4]:,.2f}" if row[4] else "MT 0.00"
                    ))

                tree.pack(fill="both", expand=True, padx=20, pady=20)
                self.logger.info(f"✅ Relatório gerado: {len(result[1])} anunciantes")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")

    def show_campanhas_ativas(self):
        """Mostra campanhas ativas usando VIEW"""
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()

        try:
            result = self.db.execute_query("SELECT * FROM v_campanhas_ativas")

            if result and result[1]:
                columns = ('Código', 'Título', 'Objetivo', 'Orçamento', 'Início', 'Término', 'Anunciante')
                tree = ctk.Treeview(self.resultados_frame, columns=columns, show='headings', height=15)

                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=130, anchor="center")

                for row in result[1]:
                    tree.insert('', 'end', values=(
                        row[0],
                        row[1][:30] if row[1] else "N/A",
                        row[2][:30] if row[2] else "N/A",
                        f"MT {row[3]:,.0f}" if row[3] else "MT 0",
                        row[4],
                        row[5],
                        row[6][:25] if row[6] else "N/A"
                    ))

                tree.pack(fill="both", expand=True, padx=20, pady=20)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

    def show_auditoria_orcamentos(self):
        """Mostra log de auditoria de orçamentos (DEMONSTRA TRIGGER)"""
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()

        try:
            result = self.db.execute_query("""
                                           SELECT Id_log,
                                                  Cod_camp,
                                                  TO_CHAR(Data_alteracao, 'DD/MM/YYYY HH24:MI:SS') AS Data,
                                                  User_alterou,
                                                  Valor_antigo,
                                                  Valor_novo,
                                                  (Valor_novo - Valor_antigo)                      AS Diferenca
                                           FROM Log_Auditoria_Orcamento
                                           ORDER BY Data_alteracao DESC
                                               FETCH FIRST 50 ROWS ONLY
                                           """)

            if result and result[1]:
                columns = ('ID', 'Campanha', 'Data Alteração', 'Usuário', 'Valor Antigo', 'Valor Novo', 'Diferença')
                tree = ctk.Treeview(self.resultados_frame, columns=columns, show='headings', height=15)

                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=120, anchor="center")

                for row in result[1]:
                    tree.insert('', 'end', values=(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        f"MT {row[4]:,.2f}" if row[4] else "MT 0",
                        f"MT {row[5]:,.2f}" if row[5] else "MT 0",
                        f"MT {row[6]:,.2f}" if row[6] else "MT 0"
                    ))

                tree.pack(fill="both", expand=True, padx=20, pady=20)

                ctk.CTkLabel(
                    self.resultados_frame,
                    text="✅ Este log é gerado automaticamente pelo TRIGGER trg_audita_orcamento_campanha",
                    font=("Arial", 11, "bold"),
                    text_color=COLORS['success']
                ).pack(pady=10)

            else:
                ctk.CTkLabel(
                    self.resultados_frame,
                    text="📝 Nenhuma alteração de orçamento registrada ainda.\nO TRIGGER está ativo e registrará automaticamente as mudanças.",
                    font=("Arial", 12),
                    text_color=COLORS['text_secondary']
                ).pack(pady=50)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro: {e}")

    def _create_date_filters(self):
        """Cria filtros de data"""
        filter_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        filter_frame.pack(fill="x", pady=(0, 20))

        # Data início
        ctk.CTkLabel(
            filter_frame,
            text="Data Início:",
            font=("Arial", 12, "bold"),
            text_color=COLORS['text_primary']
        ).grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")

        self.data_inicio_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="DD/MM/AAAA",
            font=("Arial", 12),
            width=120
        )
        self.data_inicio_entry.grid(row=0, column=1, padx=(0, 20), pady=5)
        self.data_inicio_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

        # Data fim
        ctk.CTkLabel(
            filter_frame,
            text="Data Fim:",
            font=("Arial", 12, "bold"),
            text_color=COLORS['text_primary']
        ).grid(row=0, column=2, padx=(0, 10), pady=5, sticky="w")

        self.data_fim_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="DD/MM/AAAA",
            font=("Arial", 12),
            width=120
        )
        self.data_fim_entry.grid(row=0, column=3, padx=(0, 20), pady=5)
        self.data_fim_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))

        # Botão hoje
        ctk.CTkButton(
            filter_frame,
            text="Hoje",
            command=self.set_data_hoje,
            font=("Arial", 11),
            fg_color=COLORS['secondary'],
            hover_color=COLORS['secondary_dark'],
            width=80
        ).grid(row=0, column=4, padx=5)

        # Botão últimos 7 dias
        ctk.CTkButton(
            filter_frame,
            text="Últimos 7 Dias",
            command=self.set_ultimos_7_dias,
            font=("Arial", 11),
            fg_color=COLORS['secondary'],
            hover_color=COLORS['secondary_dark'],
            width=120
        ).grid(row=0, column=5, padx=5)

    def set_data_hoje(self):
        """Define data para hoje"""
        hoje = datetime.now().strftime('%d/%m/%Y')
        self.data_inicio_entry.delete(0, 'end')
        self.data_inicio_entry.insert(0, hoje)
        self.data_fim_entry.delete(0, 'end')
        self.data_fim_entry.insert(0, hoje)

    def set_ultimos_7_dias(self):
        """Define período dos últimos 7 dias"""
        fim = datetime.now()
        inicio = fim - timedelta(days=7)

        self.data_inicio_entry.delete(0, 'end')
        self.data_inicio_entry.insert(0, inicio.strftime('%d/%m/%Y'))
        self.data_fim_entry.delete(0, 'end')
        self.data_fim_entry.insert(0, fim.strftime('%d/%m/%Y'))

    def gerar_relatorio(self):
        """Gera relatório usando todas as funções PL/SQL"""
        try:
            # Limpa resultados anteriores
            for widget in self.resultados_frame.winfo_children():
                widget.destroy()

            # Obtém datas
            data_inicio = datetime.strptime(self.data_inicio_entry.get(), '%d/%m/%Y')
            data_fim = datetime.strptime(self.data_fim_entry.get(), '%d/%m/%Y')

            # Busca estatísticas
            estatisticas = self.stats_manager.get_estatisticas_detalhadas(data_inicio, data_fim)

            # Exibe resultados
            self._exibir_resultados(estatisticas)

        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use DD/MM/AAAA")
        except Exception as e:
            app_logger.error(f"Erro ao gerar relatório: {e}")
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")

    def _exibir_resultados(self, estatisticas: Dict[str, Any]):
        """Exibe resultados do relatório"""
        # Container com scroll
        scroll_frame = ctk.CTkScrollableFrame(self.resultados_frame, fg_color=COLORS['dark_bg'])
        scroll_frame.pack(fill="both", expand=True)

        # Estatísticas Globais
        self._criar_secao(scroll_frame, "🌍 Estatísticas Globais", estatisticas['estatisticas_globais'])

        # Campanhas
        self._criar_secao(scroll_frame, "📊 Campanhas Hoje", estatisticas['campanhas_hoje'])

        # Peças Criativas
        self._criar_secao(scroll_frame, "🎨 Status das Peças", estatisticas['status_pecas'])

        # Pagamentos
        self._criar_card(scroll_frame, "💳 Pagamentos Hoje",
                         str(estatisticas['pagamentos_hoje']), COLORS['success'])

    def _criar_secao(self, parent, titulo: str, dados: Dict[str, Any]):
        """Cria uma seção de resultados"""
        secao_frame = ctk.CTkFrame(parent, fg_color=COLORS['dark_card'], corner_radius=12)
        secao_frame.pack(fill="x", pady=10, padx=10)

        ctk.CTkLabel(
            secao_frame,
            text=titulo,
            font=("Arial", 16, "bold"),
            text_color=COLORS['text_primary']
        ).pack(anchor="w", padx=15, pady=(15, 10))

        # Grid para os dados
        grid_frame = ctk.CTkFrame(secao_frame, fg_color="transparent")
        grid_frame.pack(fill="x", padx=15, pady=(0, 15))

        for i, (chave, valor) in enumerate(dados.items()):
            if chave not in ['data', 'periodo', 'total']:  # Ignora campos de controle
                row = i // 2
                col = i % 2

                card = ctk.CTkFrame(grid_frame, fg_color=COLORS['dark_bg'], corner_radius=8)
                card.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

                ctk.CTkLabel(
                    card,
                    text=chave.replace('_', ' ').title(),
                    font=("Arial", 11),
                    text_color=COLORS['text_secondary']
                ).pack(pady=(8, 2))

                ctk.CTkLabel(
                    card,
                    text=str(valor),
                    font=("Arial", 14, "bold"),
                    text_color=COLORS['text_primary']
                ).pack(pady=(2, 8))

                grid_frame.grid_columnconfigure(col, weight=1)

    def _criar_card(self, parent, titulo: str, valor: str, cor: str):
        """Cria um card individual"""
        card = ctk.CTkFrame(parent, fg_color=COLORS['dark_card'], corner_radius=12)
        card.pack(fill="x", pady=5, padx=10)

        ctk.CTkLabel(
            card,
            text=titulo,
            font=("Arial", 14, "bold"),
            text_color=COLORS['text_primary']
        ).pack(anchor="w", padx=15, pady=(12, 5))

        ctk.CTkLabel(
            card,
            text=valor,
            font=("Arial", 18, "bold"),
            text_color=cor
        ).pack(anchor="w", padx=15, pady=(0, 12))


def show_relatorios_module(parent, db, main_app):
    """Função para mostrar o módulo de relatórios"""
    return RelatoriosAvancados(parent, db, main_app)