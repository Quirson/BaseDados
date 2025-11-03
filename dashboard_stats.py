# dashboard_stats.py
from datetime import datetime
from typing import Dict, Any
from logger_config import app_logger, safe_operation


class DashboardStats:
    """Classe para gerenciar estatísticas do dashboard usando funções PL/SQL"""

    def __init__(self, db_connection):
        self.db = db_connection
        self.logger = app_logger

    @safe_operation()
    def get_global_stats(self) -> Dict[str, Any]:
        """Obtém estatísticas globais usando a VIEW"""
        try:
            result = self.db.execute_query("SELECT * FROM V_DASHBOARD_ESTATISTICAS")
            if result and result[1]:
                row = result[1][0]
                return {
                    'total_anunciantes': row[0] or 0,
                    'campanhas_ativas': row[1] or 0,
                    'orcamento_total': float(row[2]) if row[2] else 0,
                    'espacos_disponiveis': row[3] or 0,
                    'pecas_aprovadas': row[4] or 0,
                    'pecas_rejeitadas': row[5] or 0,
                    'total_pagamentos': row[6] or 0
                }
        except Exception as e:
            self.logger.error(f"Erro ao buscar estatísticas globais: {e}")

        return self._get_fallback_stats()

    @safe_operation()
    def get_campaigns_by_date(self, data: datetime) -> Dict[str, int]:
        """Usa as funções para contar campanhas por data"""
        try:
            data_str = data.strftime('%d/%m/%Y')

            # Chama as funções PL/SQL
            result_iniciadas = self.db.execute_query(
                f"SELECT FN_CAMPANHAS_INICIADAS_DATA(TO_DATE('{data_str}', 'DD/MM/YYYY')) FROM DUAL"
            )
            result_terminadas = self.db.execute_query(
                f"SELECT FN_CAMPANHAS_TERMINADAS_DATA(TO_DATE('{data_str}', 'DD/MM/YYYY')) FROM DUAL"
            )

            iniciadas = result_iniciadas[1][0][0] if result_iniciadas and result_iniciadas[1] else 0
            terminadas = result_terminadas[1][0][0] if result_terminadas and result_terminadas[1] else 0

            return {
                'iniciadas': iniciadas,
                'terminadas': terminadas,
                'data': data_str
            }

        except Exception as e:
            self.logger.error(f"Erro ao buscar campanhas por data: {e}")
            return {'iniciadas': 0, 'terminadas': 0, 'data': data.strftime('%d/%m/%Y')}

    @safe_operation()
    def get_pecas_status(self) -> Dict[str, int]:
        """Usa a função para contar peças por status"""
        try:
            result_aprovadas = self.db.execute_query(
                "SELECT FN_CONTAR_PECAS_STATUS('APROVADO') FROM DUAL"
            )
            result_rejeitadas = self.db.execute_query(
                "SELECT FN_CONTAR_PECAS_STATUS('REJEITADO') FROM DUAL"
            )

            aprovadas = result_aprovadas[1][0][0] if result_aprovadas and result_aprovadas[1] else 0
            rejeitadas = result_rejeitadas[1][0][0] if result_rejeitadas and result_rejeitadas[1] else 0

            return {
                'aprovadas': aprovadas,
                'rejeitadas': rejeitadas,
                'total': aprovadas + rejeitadas
            }

        except Exception as e:
            self.logger.error(f"Erro ao buscar status das peças: {e}")
            return {'aprovadas': 0, 'rejeitadas': 0, 'total': 0}

    @safe_operation()
    def get_pagamentos_por_data(self, data: datetime) -> int:
        """Usa a função para contar pagamentos por data"""
        try:
            data_str = data.strftime('%d/%m/%Y')
            result = self.db.execute_query(
                f"SELECT FN_PAGAMENTOS_DATA(TO_DATE('{data_str}', 'DD/MM/YYYY')) FROM DUAL"
            )

            return result[1][0][0] if result and result[1] else 0

        except Exception as e:
            self.logger.error(f"Erro ao buscar pagamentos por data: {e}")
            return 0

    @safe_operation()
    def get_estatisticas_detalhadas(self, data_inicio: datetime = None, data_fim: datetime = None) -> Dict[str, Any]:
        """Estatísticas detalhadas usando todas as funções"""
        if data_inicio is None:
            data_inicio = datetime.now()
        if data_fim is None:
            data_fim = datetime.now()

        return {
            'estatisticas_globais': self.get_global_stats(),
            'campanhas_hoje': self.get_campaigns_by_date(datetime.now()),
            'status_pecas': self.get_pecas_status(),
            'pagamentos_hoje': self.get_pagamentos_por_data(datetime.now()),
            'periodo': {
                'inicio': data_inicio.strftime('%d/%m/%Y'),
                'fim': data_fim.strftime('%d/%m/%Y')
            }
        }

    def _get_fallback_stats(self):
        """Estatísticas de fallback"""
        return {
            'total_anunciantes': 0,
            'campanhas_ativas': 0,
            'orcamento_total': 0,
            'espacos_disponiveis': 0,
            'pecas_aprovadas': 0,
            'pecas_rejeitadas': 0,
            'total_pagamentos': 0
        }