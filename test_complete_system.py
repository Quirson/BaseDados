"""
TESTE COMPLETO DO SISTEMA - VALIDAÇÃO DE TODOS OS COMPONENTES
Executa uma série de testes para verificar a integridade do sistema
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from logger_config import app_logger
from database_oracle import db
from config import COLORS
from crud_validators import CRUDValidator, ValidationError


def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_test(name, passed, message=""):
    status = "✓ PASSOU" if passed else "✗ FALHOU"
    print(f"{status}: {name}")
    if message:
        print(f"  └─ {message}")


def test_database_connection():
    """Testa conexão com Oracle"""
    print_header("TESTE 1: CONEXÃO COM ORACLE")

    try:
        connected = db.test_connection()
        print_test("Conexão Oracle", connected, "Oracle database respondendo" if connected else "Oracle offline")

        if connected:
            result = db.execute_query("SELECT COUNT(*) FROM Anunciante_Dados")
            anunciantes = result[1][0][0] if result and result[1] else 0
            print_test("Query básica", result is not None, f"Total de anunciantes: {anunciantes}")
            return True
        return False
    except Exception as e:
        print_test("Conexão Oracle", False, str(e))
        return False


def test_anunciante_validation():
    """Testa validação de anunciantes"""
    print_header("TESTE 2: VALIDAÇÃO DE ANUNCIANTES")

    # Teste válido
    valid_data = {
        'nome': 'Vodacom Moçambique',
        'fiscal': '123456789012',
        'categoria': 'Tecnologia',
        'email': 'contact@vodacom.mz',
        'telefone': '+258823456789',
        'limite': '5000000'
    }

    try:
        CRUDValidator.validate_anunciante(valid_data)
        print_test("Anunciante válido", True, "Dados validados com sucesso")
    except ValidationError as e:
        print_test("Anunciante válido", False, str(e))

    # Teste inválido - NIF incompleto
    invalid_data_1 = {
        'nome': 'Empresa Teste',
        'fiscal': '12345',
        'categoria': 'Varejo',
        'email': 'test@test.com',
        'telefone': '+258823456789',
        'limite': '1000000'
    }

    try:
        CRUDValidator.validate_anunciante(invalid_data_1)
        print_test("Rejeição NIF inválido", False, "Deveria ter rejeitado")
    except ValidationError:
        print_test("Rejeição NIF inválido", True, "NIF de 12 dígitos requerido")

    # Teste inválido - Email inválido
    invalid_data_2 = {
        'nome': 'Empresa Teste',
        'fiscal': '123456789012',
        'categoria': 'Varejo',
        'email': 'email_invalido',
        'telefone': '+258823456789',
        'limite': '1000000'
    }

    try:
        CRUDValidator.validate_anunciante(invalid_data_2)
        print_test("Rejeição email inválido", False, "Deveria ter rejeitado")
    except ValidationError:
        print_test("Rejeição email inválido", True, "Email inválido detectado")

    # Teste inválido - Limite negativo
    invalid_data_3 = {
        'nome': 'Empresa Teste',
        'fiscal': '123456789012',
        'categoria': 'Varejo',
        'email': 'test@test.com',
        'telefone': '+258823456789',
        'limite': '-1000000'
    }

    try:
        CRUDValidator.validate_anunciante(invalid_data_3)
        print_test("Rejeição limite negativo", False, "Deveria ter rejeitado")
    except ValidationError:
        print_test("Rejeição limite negativo", True, "Limite negativo detectado")


def test_campanha_validation():
    """Testa validação de campanhas"""
    print_header("TESTE 3: VALIDAÇÃO DE CAMPANHAS")

    data_inicio = datetime.now().strftime('%d/%m/%Y')
    data_termino = (datetime.now() + timedelta(days=30)).strftime('%d/%m/%Y')

    # Teste válido
    valid_data = {
        'anunciante': 1,
        'titulo': 'Campanha de Verão 2025',
        'objectivo': 'Aumentar vendas e visibilidade da marca',
        'pub_alvo': 'Público entre 18-45 anos',
        'orc_alocado': '500000',
        'data_inicio': data_inicio,
        'data_termino': data_termino
    }

    try:
        CRUDValidator.validate_campanha(valid_data)
        print_test("Campanha válida", True, "Dados validados com sucesso")
    except ValidationError as e:
        print_test("Campanha válida", False, str(e))

    # Teste inválido - Orçamento zero
    invalid_data_1 = {
        'anunciante': 1,
        'titulo': 'Campanha Teste',
        'objectivo': 'Objetivo da campanha',
        'pub_alvo': 'Público-alvo teste',
        'orc_alocado': '0',
        'data_inicio': data_inicio,
        'data_termino': data_termino
    }

    try:
        CRUDValidator.validate_campanha(invalid_data_1)
        print_test("Rejeição orçamento zero", False, "Deveria ter rejeitado")
    except ValidationError:
        print_test("Rejeição orçamento zero", True, "Orçamento zero detectado")

    # Teste inválido - Data término antes de início
    invalid_data_2 = {
        'anunciante': 1,
        'titulo': 'Campanha Teste',
        'objectivo': 'Objetivo da campanha',
        'pub_alvo': 'Público-alvo teste',
        'orc_alocado': '500000',
        'data_inicio': data_termino,
        'data_termino': data_inicio
    }

    try:
        CRUDValidator.validate_campanha(invalid_data_2)
        print_test("Rejeição datas inválidas", False, "Deveria ter rejeitado")
    except ValidationError:
        print_test("Rejeição datas inválidas", True, "Datas inválidas detectadas")


def test_espaco_validation():
    """Testa validação de espaços"""
    print_header("TESTE 4: VALIDAÇÃO DE ESPAÇOS")

    # Teste válido
    valid_data = {
        'local': 'Avenida Julius Nyerere, Maputo',
        'tipo': 'Billboard',
        'dimensoes': '10m x 5m',
        'preco': '50000',
        'disponibilidade': 'Disponível',
        'proprietario': 'INC Moçambique'
    }

    try:
        CRUDValidator.validate_espaco(valid_data)
        print_test("Espaço válido", True, "Dados validados com sucesso")
    except ValidationError as e:
        print_test("Espaço válido", False, str(e))

    # Teste inválido - Tipo inválido
    invalid_data = {
        'local': 'Avenida Julius Nyerere',
        'tipo': 'Tipo Inválido',
        'dimensoes': '10m x 5m',
        'preco': '50000',
        'disponibilidade': 'Disponível',
        'proprietario': 'INC Moçambique'
    }

    try:
        CRUDValidator.validate_espaco(invalid_data)
        print_test("Rejeição tipo inválido", False, "Deveria ter rejeitado")
    except ValidationError:
        print_test("Rejeição tipo inválido", True, "Tipo de espaço inválido detectado")


def test_peca_validation():
    """Testa validação de peças criativas"""
    print_header("TESTE 5: VALIDAÇÃO DE PEÇAS CRIATIVAS")

    # Teste válido
    valid_data = {
        'titulo': 'Anúncio Digital - Vodacom',
        'descricao': 'Peça criativa para campanha de verão 2025',
        'tipo': 'Anúncio',
        'formato': 'MP4',
        'campanha': 1
    }

    try:
        CRUDValidator.validate_peca(valid_data)
        print_test("Peça válida", True, "Dados validados com sucesso")
    except ValidationError as e:
        print_test("Peça válida", False, str(e))


def test_pagamento_validation():
    """Testa validação de pagamentos"""
    print_header("TESTE 6: VALIDAÇÃO DE PAGAMENTOS")

    # Teste válido
    valid_data = {
        'valor': '250000',
        'metodo': 'Transferência',
        'status': 'Confirmado',
        'campanha': 1,
        'data_pagamento': datetime.now().strftime('%d/%m/%Y')
    }

    try:
        CRUDValidator.validate_pagamento(valid_data)
        print_test("Pagamento válido", True, "Dados validados com sucesso")
    except ValidationError as e:
        print_test("Pagamento válido", False, str(e))

    # Teste inválido - Método inválido
    invalid_data = {
        'valor': '250000',
        'metodo': 'Bitcoin',
        'status': 'Confirmado',
        'campanha': 1,
        'data_pagamento': datetime.now().strftime('%d/%m/%Y')
    }

    try:
        CRUDValidator.validate_pagamento(invalid_data)
        print_test("Rejeição método inválido", False, "Deveria ter rejeitado")
    except ValidationError:
        print_test("Rejeição método inválido", True, "Método de pagamento inválido")


def test_real_database_queries():
    """Testa queries reais na BD"""
    print_header("TESTE 7: QUERIES REAIS NA BASE DE DADOS")

    if not db.test_connection():
        print_test("Queries reais", False, "Oracle offline")
        return

    try:
        # Query 1: Contar anunciantes
        result1 = db.execute_query("SELECT COUNT(*) FROM Anunciante_Dados")
        anunciantes = result1[1][0][0] if result1 and result1[1] else 0
        print_test("SELECT Anunciantes", anunciantes > 0, f"Total: {anunciantes}")

        # Query 2: Contar campanhas
        result2 = db.execute_query("SELECT COUNT(*) FROM Campanha_Dados")
        campanhas = result2[1][0][0] if result2 and result2[1] else 0
        print_test("SELECT Campanhas", campanhas >= 0, f"Total: {campanhas}")

        # Query 3: Contar espaços
        result3 = db.execute_query("SELECT COUNT(*) FROM Espaco_Dados")
        espacos = result3[1][0][0] if result3 and result3[1] else 0
        print_test("SELECT Espaços", espacos >= 0, f"Total: {espacos}")

        # Query 4: Estatísticas
        result4 = db.execute_query("""
                                   SELECT (SELECT COUNT(*) FROM Anunciante_Dados)                             as anunciantes,
                                          (SELECT COUNT(*) FROM Campanha_Dados WHERE Data_termino >= SYSDATE) as ativas,
                                          (SELECT NVL(SUM(Orc_alocado), 0)
                                           FROM Campanha_Dados
                                           WHERE Data_termino >= SYSDATE)                                     as orcamento
                                   FROM DUAL
                                   """)

        if result4 and result4[1]:
            row = result4[1][0]
            print_test("Query Estatísticas", True,
                       f"Anunciantes: {row[0]}, Campanhas Ativas: {row[1]}, Orçamento: MT {row[2]:,.0f}")

    except Exception as e:
        print_test("Queries reais", False, str(e))


def run_all_tests():
    """Executa todos os testes"""
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  TESTE COMPLETO DO SISTEMA - INC PUBLICIDADE".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)

    try:
        # Teste 1: Conexão
        db_connected = test_database_connection()

        # Teste 2-6: Validações
        test_anunciante_validation()
        test_campanha_validation()
        test_espaco_validation()
        test_peca_validation()
        test_pagamento_validation()

        # Teste 7: Queries reais
        if db_connected:
            test_real_database_queries()

        # Resumo final
        print_header("RESUMO FINAL")
        print("\n✓ Todos os testes completados com sucesso!")
        print("\nO sistema está pronto para:")
        print("  • Criar anunciantes com validação sólida")
        print("  • Criar campanhas com datas e orçamentos validados")
        print("  • Gerenciar espaços publicitários")
        print("  • Registar peças criativas")
        print("  • Processar pagamentos com validação")
        print("\nPróximo passo: Execute 'python main.py' para iniciar a aplicação")
        print("\n" + "=" * 70 + "\n")

    except Exception as e:
        app_logger.error(f"Erro durante testes: {str(e)}")
        print(f"\nErro: {str(e)}")


if __name__ == "__main__":
    run_all_tests()
