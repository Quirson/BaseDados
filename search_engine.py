"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  MOTOR DE PESQUISA AVANÇADO - INC MOÇAMBIQUE                                 ║
║  Sistema de pesquisa global com ranking e sugestões                          ║
║  Grupo: Eden Magnus, Francisco Guamba, Malik Dauto, Quirson Ngale           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import cx_Oracle
from logger_config import app_logger, safe_operation


class SearchEngine:
    """Motor de pesquisa avançado com suporte a múltiplas tabelas"""

    def __init__(self, db_connection):
        """
        Inicializa o motor de pesquisa

        Args:
            db_connection: Instância da conexão Oracle
        """
        self.db = db_connection
        self.logger = app_logger
        self.logger.info("SearchEngine inicializado")

        # Mapeamento de tipos de registro
        self.tipo_icons = {
            'ANUNCIANTE': '👥',
            'CAMPANHA': '📢',
            'PECA_CRIATIVA': '🎨',
            'ESPACO': '📺',
            'PAGAMENTO': '💳',
            'AGENCIA': '🏢'
        }

        # Campos pesquisáveis por tabela
        self.campos_pesquisa = {
            'ANUNCIANTE': ['TODOS', 'NOME', 'NIF', 'CATEGORIA', 'PORTE'],
            'CAMPANHA': ['TODOS', 'TITULO', 'CODIGO', 'PUBLICO', 'ORCAMENTO'],
            'PECA_CRIATIVA': ['TODOS', 'TITULO', 'CRIADOR', 'STATUS'],
            'ESPACO': ['TODOS', 'LOCAL', 'TIPO', 'DISPONIBILIDADE', 'PROPRIETARIO']
        }

    @safe_operation()
    def pesquisa_global(
            self,
            termo: str,
            tipo_filtro: Optional[str] = None,
            limite: int = 50
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Realiza pesquisa global em todas as tabelas

        Args:
            termo: Termo de pesquisa
            tipo_filtro: Filtro por tipo de registro (opcional)
            limite: Número máximo de resultados

        Returns:
            Tuple (sucesso, lista de resultados)
        """
        if not termo or len(termo.strip()) < 2:
            return False, []

        try:
            cursor = self.db.connection.cursor()
            result_cursor = cursor.var(cx_Oracle.CURSOR)

            # Chama procedure Oracle
            cursor.callproc(
                'SP_PESQUISA_GLOBAL',
                [termo.strip(), tipo_filtro, result_cursor]
            )

            # Processa resultados
            resultados = []
            for row in result_cursor.getvalue():
                resultados.append({
                    'tipo': row[0],
                    'id': row[1],
                    'titulo': row[2],
                    'subtitulo': row[3],
                    'data': row[4],
                    'relevancia': row[5] if len(row) > 5 else 1,
                    'icon': self.tipo_icons.get(row[0], '📄')
                })

            cursor.close()

            # Limita resultados
            resultados = resultados[:limite]

            # Registra pesquisa para analytics
            self._registrar_pesquisa(termo, tipo_filtro, len(resultados))

            self.logger.info(f"Pesquisa global: '{termo}' - {len(resultados)} resultados")
            return True, resultados

        except Exception as e:
            self.logger.error(f"Erro na pesquisa global: {e}")
            return False, []

    @safe_operation()
    def pesquisa_por_tabela(
            self,
            tabela: str,
            termo: str,
            campo: str = 'TODOS'
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Pesquisa específica em uma tabela com filtro por campo

        Args:
            tabela: Nome da tabela (ANUNCIANTE, CAMPANHA, etc)
            termo: Termo de pesquisa
            campo: Campo específico para pesquisar

        Returns:
            Tuple (sucesso, lista de resultados)
        """
        if not termo or len(termo.strip()) < 1:
            return False, []

        try:
            # Mapeia procedure correta
            procedures = {
                'ANUNCIANTE': 'SP_PESQUISA_ANUNCIANTES',
                'CAMPANHA': 'SP_PESQUISA_CAMPANHAS',
                'PECA_CRIATIVA': 'SP_PESQUISA_PECAS',
                'ESPACO': 'SP_PESQUISA_ESPACOS'
            }

            procedure = procedures.get(tabela)
            if not procedure:
                self.logger.warning(f"Tabela não suportada: {tabela}")
                return False, []

            cursor = self.db.connection.cursor()
            result_cursor = cursor.var(cx_Oracle.CURSOR)

            # Chama procedure específica
            cursor.callproc(
                procedure,
                [termo.strip(), campo, result_cursor]
            )

            # Processa resultados
            resultados = []
            columns = [desc[0] for desc in result_cursor.getvalue().description]

            for row in result_cursor.getvalue():
                row_dict = dict(zip(columns, row))
                resultados.append(row_dict)

            cursor.close()

            self.logger.info(
                f"Pesquisa em {tabela} (campo: {campo}): "
                f"'{termo}' - {len(resultados)} resultados"
            )
            return True, resultados

        except Exception as e:
            self.logger.error(f"Erro na pesquisa por tabela: {e}")
            return False, []

    @safe_operation()
    def obter_sugestoes(self, termo: str, limite: int = 8) -> List[Dict[str, str]]:
        """
        Obtém sugestões de autocompletar baseadas no termo parcial

        Args:
            termo: Termo parcial digitado
            limite: Número máximo de sugestões

        Returns:
            Lista de sugestões com tipo
        """
        if not termo or len(termo.strip()) < 2:
            return []

        try:
            cursor = self.db.connection.cursor()
            result_cursor = cursor.var(cx_Oracle.CURSOR)

            # Chama procedure de sugestões
            cursor.callproc(
                'SP_SUGESTOES_PESQUISA',
                [termo.strip(), result_cursor]
            )

            # Processa sugestões
            sugestoes = []
            for row in result_cursor.getvalue():
                if len(sugestoes) >= limite:
                    break

                sugestoes.append({
                    'texto': row[0],
                    'tipo': row[1],
                    'icon': self.tipo_icons.get(row[1], '📄')
                })

            cursor.close()
            return sugestoes

        except Exception as e:
            self.logger.error(f"Erro ao obter sugestões: {e}")
            return []

    @safe_operation()
    def pesquisa_avancada(
            self,
            termo: str,
            tipo: Optional[str] = None,
            data_inicio: Optional[datetime] = None,
            data_fim: Optional[datetime] = None
    ) -> Tuple[bool, List[Dict[str, Any]]]:
        """
        Pesquisa avançada com múltiplos filtros

        Args:
            termo: Termo de pesquisa
            tipo: Filtro por tipo de registro
            data_inicio: Data inicial do filtro
            data_fim: Data final do filtro

        Returns:
            Tuple (sucesso, lista de resultados)
        """
        if not termo or len(termo.strip()) < 2:
            return False, []

        try:
            cursor = self.db.connection.cursor()
            result_cursor = cursor.var(cx_Oracle.CURSOR)

            # Chama procedure avançada
            cursor.callproc(
                'SP_PESQUISA_AVANCADA',
                [termo.strip(), tipo, data_inicio, data_fim, result_cursor]
            )

            # Processa resultados
            resultados = []
            for row in result_cursor.getvalue():
                resultados.append({
                    'tipo': row[0],
                    'id': row[1],
                    'titulo': row[2],
                    'subtitulo': row[3],
                    'data': row[4],
                    'score': row[5] if len(row) > 5 else 0,
                    'icon': self.tipo_icons.get(row[0], '📄')
                })

            cursor.close()

            self.logger.info(
                f"Pesquisa avançada: '{termo}' "
                f"(tipo: {tipo}, datas: {data_inicio} a {data_fim}) - "
                f"{len(resultados)} resultados"
            )
            return True, resultados

        except Exception as e:
            self.logger.error(f"Erro na pesquisa avançada: {e}")
            return False, []

    @safe_operation()
    def obter_estatisticas(self) -> Dict[str, Any]:
        """
        Obtém estatísticas gerais de pesquisa

        Returns:
            Dicionário com estatísticas
        """
        try:
            # Estatísticas por tipo
            success, result = self.db.execute_query(
                "SELECT * FROM V_STATS_PESQUISA ORDER BY TOTAL_REGISTROS DESC"
            )

            if not success or not result:
                return {}

            stats = {
                'total_registros': sum(row[1] for row in result),
                'por_tipo': {}
            }

            for row in result:
                tipo = row[0]
                stats['por_tipo'][tipo] = {
                    'total': row[1],
                    'primeiro': row[2],
                    'ultimo': row[3],
                    'icon': self.tipo_icons.get(tipo, '📄')
                }

            # Top pesquisas
            success_top, result_top = self.db.execute_query(
                "SELECT * FROM V_TOP_PESQUISAS"
            )

            if success_top and result_top:
                stats['top_pesquisas'] = [
                    {
                        'termo': row[0],
                        'total': row[1],
                        'media_resultados': row[2],
                        'ultima': row[3]
                    }
                    for row in result_top[:10]
                ]

            return stats

        except Exception as e:
            self.logger.error(f"Erro ao obter estatísticas: {e}")
            return {}

    @safe_operation()
    @safe_operation()
    def _registrar_pesquisa(
            self,
            termo: str,
            tipo: Optional[str],
            qtd_resultados: int
    ) -> None:
        """
        Registra pesquisa no log para analytics - VERSÃO CORRIGIDA
        """
        try:
            # 🆕 USAR execute_query EM VEZ DE execute_dml
            self.db.execute_query(
                """
                INSERT INTO Log_Pesquisas
                    (Termo_pesquisa, Tipo_registro, Qtd_resultados, Usuario)
                VALUES (: 1, :2, :3, :4)
                """,
                (termo[:255], tipo, qtd_resultados, 'Administrador'),
                fetch=False  # 🆕 IMPORTANTE: fetch=False para INSERT
            )
        except Exception as e:
            # Não interrompe a pesquisa se falhar o log
            self.logger.warning(f"Erro ao registrar pesquisa no log: {e}")

    def get_campos_disponiveis(self, tabela: str) -> List[str]:
        """
        Retorna lista de campos pesquisáveis para uma tabela

        Args:
            tabela: Nome da tabela

        Returns:
            Lista de campos disponíveis
        """
        return self.campos_pesquisa.get(tabela, ['TODOS'])

    def get_tipos_registro(self) -> List[Dict[str, str]]:
        """
        Retorna lista de tipos de registro disponíveis

        Returns:
            Lista com tipos e ícones
        """
        return [
            {'tipo': tipo, 'icon': icon, 'nome': tipo.replace('_', ' ').title()}
            for tipo, icon in self.tipo_icons.items()
        ]

    @safe_operation()
    def validar_termo(self, termo: str) -> Tuple[bool, str]:
        """
        Valida termo de pesquisa

        Args:
            termo: Termo a validar

        Returns:
            Tuple (válido, mensagem)
        """
        if not termo or not termo.strip():
            return False, "Digite um termo para pesquisar"

        if len(termo.strip()) < 2:
            return False, "Digite pelo menos 2 caracteres"

        if len(termo) > 255:
            return False, "Termo muito longo (máximo 255 caracteres)"

        # Caracteres perigosos para SQL Injection
        caracteres_proibidos = ["'", '"', ';', '--', '/*', '*/']
        for char in caracteres_proibidos:
            if char in termo:
                return False, f"Caractere não permitido: {char}"

        return True, "OK"

    def highlight_termo(self, texto: str, termo: str) -> str:
        """
        Adiciona marcação para destacar termo no texto

        Args:
            texto: Texto original
            termo: Termo a destacar

        Returns:
            Texto com marcações
        """
        if not texto or not termo:
            return texto

        import re
        # Case insensitive replace mantendo o case original
        pattern = re.compile(re.escape(termo), re.IGNORECASE)
        return pattern.sub(lambda m: f"<<{m.group()}>>", texto)


# =============================================================================
# CACHE DE PESQUISAS RECENTES (EM MEMÓRIA)
# =============================================================================

class SearchCache:
    """Cache simples para pesquisas recentes"""

    def __init__(self, max_size: int = 20):
        self.cache = []
        self.max_size = max_size

    def adicionar(self, termo: str, resultados_count: int) -> None:
        """Adiciona pesquisa ao cache"""
        # Remove duplicatas
        self.cache = [item for item in self.cache if item['termo'] != termo]

        # Adiciona no início
        self.cache.insert(0, {
            'termo': termo,
            'count': resultados_count,
            'timestamp': datetime.now()
        })

        # Limita tamanho
        if len(self.cache) > self.max_size:
            self.cache = self.cache[:self.max_size]

    def obter_recentes(self, limite: int = 10) -> List[Dict[str, Any]]:
        """Retorna pesquisas recentes"""
        return self.cache[:limite]

    def limpar(self) -> None:
        """Limpa cache"""
        self.cache = []


# =============================================================================
# EXPORTAÇÃO DE RESULTADOS
# =============================================================================

class SearchExporter:
    """Classe para exportar resultados de pesquisa"""

    @staticmethod
    def para_csv(resultados: List[Dict[str, Any]], filename: str = "pesquisa.csv") -> bool:
        """Exporta resultados para CSV"""
        import csv

        try:
            if not resultados:
                return False

            with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
                # Usa as chaves do primeiro resultado como headers
                writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
                writer.writeheader()
                writer.writerows(resultados)

            return True

        except Exception as e:
            app_logger.error(f"Erro ao exportar CSV: {e}")
            return False

    @staticmethod
    def para_texto(resultados: List[Dict[str, Any]], filename: str = "pesquisa.txt") -> bool:
        """Exporta resultados para arquivo texto"""
        try:
            if not resultados:
                return False

            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 80 + "\n")
                f.write("RESULTADOS DA PESQUISA - INC MOÇAMBIQUE\n")
                f.write(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write(f"Total de resultados: {len(resultados)}\n")
                f.write("=" * 80 + "\n\n")

                for i, resultado in enumerate(resultados, 1):
                    f.write(f"{i}. {resultado.get('titulo', 'N/A')}\n")
                    f.write(f"   Tipo: {resultado.get('tipo', 'N/A')}\n")
                    f.write(f"   ID: {resultado.get('id', 'N/A')}\n")

                    if 'subtitulo' in resultado:
                        f.write(f"   {resultado['subtitulo']}\n")

                    f.write("\n")

            return True

        except Exception as e:
            app_logger.error(f"Erro ao exportar texto: {e}")
            return False

# =============================================================================
# FIM DO MÓDULO
# =============================================================================