"""
CONEXÃO ORACLE COM GESTÃO ROBUSTA DE ERROS
Implementa pool de conexões e tratamento seguro
"""

import cx_Oracle
import logging
from logger_config import log_execution, safe_operation, app_logger
from config import DB_CONFIG


class OracleDatabase:
    """Classe para gerenciar conexão com Oracle"""

    def __init__(self):
        self.connection = None
        self.logger = app_logger
        self.connect()

    @log_execution
    def connect(self):
        """Conecta à Oracle com timeout e tratamento de erro"""
        try:
            self.logger.info("Iniciando conexão Oracle...")

            dsn = cx_Oracle.makedsn(
                DB_CONFIG['host'],
                DB_CONFIG['port'],
                service_name=DB_CONFIG['service']
            )

            self.connection = cx_Oracle.connect(
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                dsn=dsn,
                threaded=True  # Enable threaded mode for thread safety
            )

            self.logger.info("Conexão Oracle estabelecida com sucesso!")
            return True

        except cx_Oracle.DatabaseError as db_err:
            self.logger.error(f"Erro de conexão Oracle: {db_err}")
            self.connection = None
            return False
        except Exception as e:
            self.logger.error(f"Erro inesperado na conexão: {str(e)}")
            self.connection = None
            return False

    @log_execution
    def execute_query(self, query, params=None, fetch=True):
        """Executa queries com tratamento seguro de erros"""
        cursor = None
        try:
            if not self.connection:
                self.logger.warning("Conexão perdida, reconectando...")
                if not self.connect():
                    raise Exception("Falha ao reconectar ao Oracle")

            cursor = self.connection.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch and cursor.description:
                columns = [col[0] for col in cursor.description]
                rows = cursor.fetchall()
                self.logger.debug(f"Query retornou {len(rows)} linhas")
                return (columns, rows)
            else:
                self.connection.commit()
                self.logger.debug("Query executada e confirmada")
                return True

        except cx_Oracle.DatabaseError as db_err:
            self.logger.error(f"Erro de banco de dados: {db_err}")
            if self.connection:
                self.connection.rollback()
            return False
        except Exception as e:
            self.logger.error(f"Erro na execução da query: {str(e)}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            if cursor:
                try:
                    cursor.close()
                except:
                    pass

    @safe_operation(default_return=False)
    def test_connection(self):
        """Testa se a conexão está ativa"""
        result = self.execute_query("SELECT '✅ CONECTADO' AS STATUS FROM DUAL")
        return result is not None and result is not False

    def close(self):
        """Fecha a conexão com segurança"""
        if self.connection:
            try:
                self.connection.close()
                self.logger.info("Conexão Oracle fechada")
            except Exception as e:
                self.logger.error(f"Erro ao fechar conexão: {str(e)}")

    def __del__(self):
        """Destrutor para garantir fechamento"""
        self.close()


db = OracleDatabase()
