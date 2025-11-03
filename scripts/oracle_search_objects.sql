-- ============================================================================
-- SISTEMA DE PESQUISA AVANÇADO - INC MOÇAMBIQUE (VERSÃO CORRIGIDA)
-- Views, Procedures e Triggers para Pesquisa Global
-- Grupo: Eden Magnus, Francisco Guamba, Malik Dauto, Quirson Ngale
-- CORREÇÃO: ORA-01790 - Todos os campos agora são VARCHAR2
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. VIEW GLOBAL DE PESQUISA - TODOS OS DADOS UNIFICADOS (CORRIGIDA)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW V_PESQUISA_GLOBAL AS
SELECT
    'ANUNCIANTE' AS TIPO_REGISTRO,
    TO_CHAR(Num_id_fiscal) AS ID_REGISTRO,
    Nome_razao_soc AS TITULO_PRINCIPAL,
    Cat_negocio || ' | ' || Porte AS SUBTITULO,
    'NIF: ' || TO_CHAR(Num_id_fiscal) || ' | ' ||
    'Categoria: ' || Cat_negocio || ' | ' ||
    'Porte: ' || Porte || ' | ' ||
    'Endereço: ' || NVL(Endereco, 'N/A') || ' | ' ||
    'Contatos: ' || NVL(Contactos, 'N/A') AS TEXTO_PESQUISAVEL,
    TO_CHAR(SYSDATE, 'DD/MM/YYYY') AS DATA_REGISTRO
FROM Anunciante_Dados
UNION ALL
SELECT
    'CAMPANHA' AS TIPO_REGISTRO,
    TO_CHAR(Cod_camp) AS ID_REGISTRO,
    NVL(Titulo, 'Sem título') AS TITULO_PRINCIPAL,
    'Orçamento: MT ' || TO_CHAR(NVL(Orc_alocado, 0), '999G999G999D99') AS SUBTITULO,
    'Código: ' || TO_CHAR(Cod_camp) || ' | ' ||
    'Título: ' || NVL(Titulo, 'N/A') || ' | ' ||
    'Público: ' || NVL(Pub_alvo, 'N/A') || ' | ' ||
    'Orçamento: ' || TO_CHAR(NVL(Orc_alocado, 0)) AS TEXTO_PESQUISAVEL,
    TO_CHAR(Data_inicio, 'DD/MM/YYYY') AS DATA_REGISTRO
FROM Campanha_Dados
UNION ALL
SELECT
    'PECA_CRIATIVA' AS TIPO_REGISTRO,
    TO_CHAR(Id_unicopeca) AS ID_REGISTRO,
    NVL(Titulo, 'Sem título') AS TITULO_PRINCIPAL,
    'Criador: ' || NVL(Criador, 'N/A') AS SUBTITULO,
    'ID: ' || TO_CHAR(Id_unicopeca) || ' | ' ||
    'Título: ' || NVL(Titulo, 'N/A') || ' | ' ||
    'Criador: ' || NVL(Criador, 'N/A') || ' | ' ||
    'Status: ' || NVL(Status_aprov, 'N/A') || ' | ' ||
    SUBSTR(NVL(TO_CHAR(Descricao), 'N/A'), 1, 200) AS TEXTO_PESQUISAVEL,
    TO_CHAR(Data_criacao, 'DD/MM/YYYY') AS DATA_REGISTRO
FROM Pecas_Criativas
UNION ALL
SELECT
    'ESPACO' AS TIPO_REGISTRO,
    TO_CHAR(Id_espaco) AS ID_REGISTRO,
    NVL(Local_fis_dig, 'Sem localização') AS TITULO_PRINCIPAL,
    'Tipo: ' || NVL(Tipo, 'N/A') || ' | MT ' || TO_CHAR(NVL(Preco_base, 0), '999G999G999D99') AS SUBTITULO,
    'ID: ' || TO_CHAR(Id_espaco) || ' | ' ||
    'Local: ' || NVL(Local_fis_dig, 'N/A') || ' | ' ||
    'Tipo: ' || NVL(Tipo, 'N/A') || ' | ' ||
    'Dimensões: ' || NVL(Dimensoes, 'N/A') || ' | ' ||
    'Visibilidade: ' || NVL(Visibilidade, 'N/A') || ' | ' ||
    'Disponibilidade: ' || NVL(Disponibilidade, 'N/A') || ' | ' ||
    'Proprietário: ' || NVL(Proprietario, 'N/A') AS TEXTO_PESQUISAVEL,
    TO_CHAR(SYSDATE, 'DD/MM/YYYY') AS DATA_REGISTRO
FROM Espaco_Dados
UNION ALL
SELECT
    'PAGAMENTO' AS TIPO_REGISTRO,
    TO_CHAR(Cod_pagamento) AS ID_REGISTRO,
    'Pagamento #' || TO_CHAR(Cod_pagamento) AS TITULO_PRINCIPAL,
    'Método: ' || NVL(Metod_pagamento, 'N/A') AS SUBTITULO,
    'Código: ' || TO_CHAR(Cod_pagamento) || ' | ' ||
    'Método: ' || NVL(Metod_pagamento, 'N/A') || ' | ' ||
    'Preço: ' || TO_CHAR(NVL(Precos_dinam, 0)) AS TEXTO_PESQUISAVEL,
    TO_CHAR(SYSDATE, 'DD/MM/YYYY') AS DATA_REGISTRO
FROM Pagamentos
UNION ALL
SELECT
    'AGENCIA' AS TIPO_REGISTRO,
    TO_CHAR(Reg_comercial) AS ID_REGISTRO,
    NVL(Nome_age, 'Sem nome') AS TITULO_PRINCIPAL,
    'Equipe: ' || NVL(Equip_principal, 'N/A') AS SUBTITULO,
    'Registro: ' || TO_CHAR(Reg_comercial) || ' | ' ||
    'Nome: ' || NVL(Nome_age, 'N/A') || ' | ' ||
    'Equipe: ' || NVL(Equip_principal, 'N/A') || ' | ' ||
    'Capacidades: ' || NVL(Cap_tecnicas, 'N/A') AS TEXTO_PESQUISAVEL,
    TO_CHAR(SYSDATE, 'DD/MM/YYYY') AS DATA_REGISTRO
FROM Agencia_Dados;

-- Verificar se criou
SELECT 'VIEW V_PESQUISA_GLOBAL criada com sucesso!' AS STATUS FROM DUAL;

-- ----------------------------------------------------------------------------
-- 2. VIEW PARA ESTATÍSTICAS DE PESQUISA
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW V_STATS_PESQUISA AS
SELECT
    TIPO_REGISTRO,
    COUNT(*) AS TOTAL_REGISTROS,
    MIN(DATA_REGISTRO) AS PRIMEIRO_REGISTRO,
    MAX(DATA_REGISTRO) AS ULTIMO_REGISTRO
FROM V_PESQUISA_GLOBAL
GROUP BY TIPO_REGISTRO
ORDER BY TOTAL_REGISTROS DESC;

SELECT 'VIEW V_STATS_PESQUISA criada com sucesso!' AS STATUS FROM DUAL;

-- ----------------------------------------------------------------------------
-- 3. PROCEDURE: PESQUISA GLOBAL COM RANKING
-- ----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE SP_PESQUISA_GLOBAL(
    p_termo IN VARCHAR2,
    p_tipo IN VARCHAR2 DEFAULT NULL,
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
        SELECT
            TIPO_REGISTRO,
            ID_REGISTRO,
            TITULO_PRINCIPAL,
            SUBTITULO,
            DATA_REGISTRO,
            -- Cálculo de relevância (ranking)
            CASE
                WHEN UPPER(TITULO_PRINCIPAL) LIKE UPPER('%' || p_termo || '%') THEN 3
                WHEN UPPER(SUBTITULO) LIKE UPPER('%' || p_termo || '%') THEN 2
                ELSE 1
            END AS RELEVANCIA
        FROM V_PESQUISA_GLOBAL
        WHERE
            UPPER(TEXTO_PESQUISAVEL) LIKE UPPER('%' || p_termo || '%')
            AND (p_tipo IS NULL OR TIPO_REGISTRO = p_tipo)
        ORDER BY
            CASE
                WHEN UPPER(TITULO_PRINCIPAL) LIKE UPPER('%' || p_termo || '%') THEN 3
                WHEN UPPER(SUBTITULO) LIKE UPPER('%' || p_termo || '%') THEN 2
                ELSE 1
            END DESC,
            TITULO_PRINCIPAL;
END;
/

SELECT 'PROCEDURE SP_PESQUISA_GLOBAL criada com sucesso!' AS STATUS FROM DUAL;

-- ----------------------------------------------------------------------------
-- 4. PROCEDURE: PESQUISA POR TABELA ESPECÍFICA - ANUNCIANTES
-- ----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE SP_PESQUISA_ANUNCIANTES(
    p_termo IN VARCHAR2,
    p_campo IN VARCHAR2 DEFAULT 'TODOS',
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    CASE p_campo
        WHEN 'NOME' THEN
            OPEN p_cursor FOR
                SELECT * FROM Anunciante_Dados
                WHERE UPPER(Nome_razao_soc) LIKE UPPER('%' || p_termo || '%')
                ORDER BY Nome_razao_soc;

        WHEN 'NIF' THEN
            OPEN p_cursor FOR
                SELECT * FROM Anunciante_Dados
                WHERE TO_CHAR(Num_id_fiscal) LIKE '%' || p_termo || '%'
                ORDER BY Num_id_fiscal;

        WHEN 'CATEGORIA' THEN
            OPEN p_cursor FOR
                SELECT * FROM Anunciante_Dados
                WHERE UPPER(Cat_negocio) LIKE UPPER('%' || p_termo || '%')
                ORDER BY Cat_negocio;

        WHEN 'PORTE' THEN
            OPEN p_cursor FOR
                SELECT * FROM Anunciante_Dados
                WHERE UPPER(Porte) LIKE UPPER('%' || p_termo || '%')
                ORDER BY Porte;

        ELSE -- TODOS
            OPEN p_cursor FOR
                SELECT * FROM Anunciante_Dados
                WHERE UPPER(Nome_razao_soc || ' ' || NVL(Cat_negocio, '') || ' ' ||
                           NVL(Porte, '') || ' ' || NVL(Endereco, '') || ' ' || NVL(Contactos, ''))
                      LIKE UPPER('%' || p_termo || '%')
                ORDER BY Nome_razao_soc;
    END CASE;
END;
/

SELECT 'PROCEDURE SP_PESQUISA_ANUNCIANTES criada com sucesso!' AS STATUS FROM DUAL;

-- ----------------------------------------------------------------------------
-- 5. PROCEDURE: PESQUISA POR TABELA ESPECÍFICA - CAMPANHAS
-- ----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE SP_PESQUISA_CAMPANHAS(
    p_termo IN VARCHAR2,
    p_campo IN VARCHAR2 DEFAULT 'TODOS',
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    CASE p_campo
        WHEN 'TITULO' THEN
            OPEN p_cursor FOR
                SELECT * FROM Campanha_Dados
                WHERE UPPER(Titulo) LIKE UPPER('%' || p_termo || '%')
                ORDER BY Data_inicio DESC;

        WHEN 'CODIGO' THEN
            OPEN p_cursor FOR
                SELECT * FROM Campanha_Dados
                WHERE TO_CHAR(Cod_camp) LIKE '%' || p_termo || '%'
                ORDER BY Cod_camp DESC;

        WHEN 'PUBLICO' THEN
            OPEN p_cursor FOR
                SELECT * FROM Campanha_Dados
                WHERE UPPER(Pub_alvo) LIKE UPPER('%' || p_termo || '%')
                ORDER BY Data_inicio DESC;

        WHEN 'ORCAMENTO' THEN
            OPEN p_cursor FOR
                SELECT * FROM Campanha_Dados
                WHERE TO_CHAR(Orc_alocado) LIKE '%' || p_termo || '%'
                ORDER BY Orc_alocado DESC;

        ELSE -- TODOS
            OPEN p_cursor FOR
                SELECT * FROM Campanha_Dados
                WHERE UPPER(NVL(Titulo, '') || ' ' || NVL(Pub_alvo, '')) LIKE UPPER('%' || p_termo || '%')
                   OR TO_CHAR(Cod_camp) LIKE '%' || p_termo || '%'
                   OR TO_CHAR(Orc_alocado) LIKE '%' || p_termo || '%'
                ORDER BY Data_inicio DESC;
    END CASE;
END;
/

SELECT 'PROCEDURE SP_PESQUISA_CAMPANHAS criada com sucesso!' AS STATUS FROM DUAL;

-- ----------------------------------------------------------------------------
-- 6. PROCEDURE: PESQUISA POR TABELA ESPECÍFICA - PEÇAS
-- ----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE SP_PESQUISA_PECAS(
    p_termo IN VARCHAR2,
    p_campo IN VARCHAR2 DEFAULT 'TODOS',
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    CASE p_campo
        WHEN 'TITULO' THEN
            OPEN p_cursor FOR
                SELECT * FROM Pecas_Criativas
                WHERE UPPER(Titulo) LIKE UPPER('%' || p_termo || '%')
                ORDER BY Data_criacao DESC;

        WHEN 'CRIADOR' THEN
            OPEN p_cursor FOR
                SELECT * FROM Pecas_Criativas
                WHERE UPPER(Criador) LIKE UPPER('%' || p_termo || '%')
                ORDER BY Criador;

        WHEN 'STATUS' THEN
            OPEN p_cursor FOR
                SELECT * FROM Pecas_Criativas
                WHERE UPPER(Status_aprov) LIKE UPPER('%' || p_termo || '%')
                ORDER BY Status_aprov;

        ELSE -- TODOS
            OPEN p_cursor FOR
                SELECT * FROM Pecas_Criativas
                WHERE UPPER(NVL(Titulo, '') || ' ' || NVL(Criador, '') || ' ' || NVL(Status_aprov, ''))
                      LIKE UPPER('%' || p_termo || '%')
                ORDER BY Data_criacao DESC;
    END CASE;
END;
/

SELECT 'PROCEDURE SP_PESQUISA_PECAS criada com sucesso!' AS STATUS FROM DUAL;

-- ----------------------------------------------------------------------------
-- 7. PROCEDURE: PESQUISA POR TABELA ESPECÍFICA - ESPAÇOS
-- ----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE SP_PESQUISA_ESPACOS(
    p_termo IN VARCHAR2,
    p_campo IN VARCHAR2 DEFAULT 'TODOS',
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    CASE p_campo
        WHEN 'LOCAL' THEN
            OPEN p_cursor FOR
                SELECT * FROM Espaco_Dados
                WHERE UPPER(Local_fis_dig) LIKE UPPER('%' || p_termo || '%')
                ORDER BY Local_fis_dig;

        WHEN 'TIPO' THEN
            OPEN p_cursor FOR
                SELECT * FROM Espaco_Dados
                WHERE UPPER(Tipo) LIKE UPPER('%' || p_termo || '%')
                ORDER BY Tipo;

        WHEN 'DISPONIBILIDADE' THEN
            OPEN p_cursor FOR
                SELECT * FROM Espaco_Dados
                WHERE UPPER(Disponibilidade) LIKE UPPER('%' || p_termo || '%')
                ORDER BY Disponibilidade;

        WHEN 'PROPRIETARIO' THEN
            OPEN p_cursor FOR
                SELECT * FROM Espaco_Dados
                WHERE UPPER(Proprietario) LIKE UPPER('%' || p_termo || '%')
                ORDER BY Proprietario;

        ELSE -- TODOS
            OPEN p_cursor FOR
                SELECT * FROM Espaco_Dados
                WHERE UPPER(NVL(Local_fis_dig, '') || ' ' || NVL(Tipo, '') || ' ' ||
                           NVL(Visibilidade, '') || ' ' || NVL(Proprietario, ''))
                      LIKE UPPER('%' || p_termo || '%')
                ORDER BY Local_fis_dig;
    END CASE;
END;
/

SELECT 'PROCEDURE SP_PESQUISA_ESPACOS criada com sucesso!' AS STATUS FROM DUAL;

-- ----------------------------------------------------------------------------
-- 8. TABELA PARA HISTÓRICO DE PESQUISAS (ANALYTICS)
-- ----------------------------------------------------------------------------
CREATE TABLE Log_Pesquisas (
    Id_log NUMBER PRIMARY KEY,
    Termo_pesquisa VARCHAR2(255) NOT NULL,
    Tipo_registro VARCHAR2(50),
    Qtd_resultados NUMBER,
    Data_pesquisa TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Usuario VARCHAR2(100)
);

SELECT 'TABELA Log_Pesquisas criada com sucesso!' AS STATUS FROM DUAL;

-- Sequence para ID
CREATE SEQUENCE Seq_log_pesquisas START WITH 1 INCREMENT BY 1;

SELECT 'SEQUENCE Seq_log_pesquisas criada com sucesso!' AS STATUS FROM DUAL;

-- ----------------------------------------------------------------------------
-- 9. TRIGGER: REGISTRA AUTOMATICAMENTE PESQUISAS POPULARES
-- ----------------------------------------------------------------------------
CREATE OR REPLACE TRIGGER TRG_LOG_PESQUISAS
BEFORE INSERT ON Log_Pesquisas
FOR EACH ROW
BEGIN
    IF :NEW.Id_log IS NULL THEN
        SELECT Seq_log_pesquisas.NEXTVAL INTO :NEW.Id_log FROM DUAL;
    END IF;

    IF :NEW.Data_pesquisa IS NULL THEN
        :NEW.Data_pesquisa := CURRENT_TIMESTAMP;
    END IF;
END;
/

SELECT 'TRIGGER TRG_LOG_PESQUISAS criado com sucesso!' AS STATUS FROM DUAL;

-- ----------------------------------------------------------------------------
-- 10. VIEW: TOP 10 PESQUISAS MAIS REALIZADAS
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW V_TOP_PESQUISAS AS
SELECT
    Termo_pesquisa,
    COUNT(*) AS Total_pesquisas,
    AVG(Qtd_resultados) AS Media_resultados,
    MAX(Data_pesquisa) AS Ultima_pesquisa
FROM Log_Pesquisas
WHERE Data_pesquisa >= SYSDATE - 30  -- Últimos 30 dias
GROUP BY Termo_pesquisa
ORDER BY COUNT(*) DESC
FETCH FIRST 10 ROWS ONLY;

SELECT 'VIEW V_TOP_PESQUISAS criada com sucesso!' AS STATUS FROM DUAL;

-- ----------------------------------------------------------------------------
-- 11. PROCEDURE: OBTER SUGESTÕES DE PESQUISA (AUTOCOMPLETE)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE SP_SUGESTOES_PESQUISA(
    p_termo IN VARCHAR2,
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
        SELECT DISTINCT TITULO_PRINCIPAL AS SUGESTAO, TIPO_REGISTRO
        FROM V_PESQUISA_GLOBAL
        WHERE UPPER(TITULO_PRINCIPAL) LIKE UPPER(p_termo || '%')
        ORDER BY LENGTH(TITULO_PRINCIPAL), TITULO_PRINCIPAL
        FETCH FIRST 8 ROWS ONLY;
END;
/

SELECT 'PROCEDURE SP_SUGESTOES_PESQUISA criada com sucesso!' AS STATUS FROM DUAL;

-- ----------------------------------------------------------------------------
-- 12. FUNÇÃO: CALCULAR RELEVÂNCIA DE PESQUISA
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION FN_RELEVANCIA_PESQUISA(
    p_texto IN VARCHAR2,
    p_termo IN VARCHAR2
) RETURN NUMBER AS
    v_relevancia NUMBER := 0;
    v_texto_upper VARCHAR2(4000);
    v_termo_upper VARCHAR2(255);
BEGIN
    v_texto_upper := UPPER(p_texto);
    v_termo_upper := UPPER(p_termo);

    -- Correspondência exata no início
    IF v_texto_upper LIKE v_termo_upper || '%' THEN
        v_relevancia := v_relevancia + 100;
    END IF;

    -- Correspondência exata em qualquer lugar
    IF v_texto_upper LIKE '%' || v_termo_upper || '%' THEN
        v_relevancia := v_relevancia + 50;
    END IF;

    -- Conta ocorrências
    v_relevancia := v_relevancia +
        (LENGTH(v_texto_upper) - LENGTH(REPLACE(v_texto_upper, v_termo_upper, ''))) /
        GREATEST(LENGTH(v_termo_upper), 1) * 10;

    RETURN v_relevancia;
END;
/

SELECT 'FUNÇÃO FN_RELEVANCIA_PESQUISA criada com sucesso!' AS STATUS FROM DUAL;

-- ----------------------------------------------------------------------------
-- 13. PROCEDURE: PESQUISA AVANÇADA COM FILTROS MÚLTIPLOS
-- ----------------------------------------------------------------------------
CREATE OR REPLACE PROCEDURE SP_PESQUISA_AVANCADA(
    p_termo IN VARCHAR2,
    p_tipo IN VARCHAR2 DEFAULT NULL,
    p_data_inicio IN DATE DEFAULT NULL,
    p_data_fim IN DATE DEFAULT NULL,
    p_cursor OUT SYS_REFCURSOR
) AS
BEGIN
    OPEN p_cursor FOR
        SELECT
            TIPO_REGISTRO,
            ID_REGISTRO,
            TITULO_PRINCIPAL,
            SUBTITULO,
            DATA_REGISTRO,
            FN_RELEVANCIA_PESQUISA(TEXTO_PESQUISAVEL, p_termo) AS SCORE_RELEVANCIA
        FROM V_PESQUISA_GLOBAL
        WHERE
            UPPER(TEXTO_PESQUISAVEL) LIKE UPPER('%' || p_termo || '%')
            AND (p_tipo IS NULL OR TIPO_REGISTRO = p_tipo)
            AND (p_data_inicio IS NULL OR TO_DATE(DATA_REGISTRO, 'DD/MM/YYYY') >= p_data_inicio)
            AND (p_data_fim IS NULL OR TO_DATE(DATA_REGISTRO, 'DD/MM/YYYY') <= p_data_fim)
        ORDER BY
            FN_RELEVANCIA_PESQUISA(TEXTO_PESQUISAVEL, p_termo) DESC,
            TITULO_PRINCIPAL;
END;
/

SELECT 'PROCEDURE SP_PESQUISA_AVANCADA criada com sucesso!' AS STATUS FROM DUAL;

-- ----------------------------------------------------------------------------
-- 14. ÍNDICES PARA OTIMIZAÇÃO DE PERFORMANCE
-- ----------------------------------------------------------------------------
-- Índices em campos de pesquisa frequente (com verificação)
BEGIN
    EXECUTE IMMEDIATE 'CREATE INDEX IDX_ANUNC_NOME ON Anunciante_Dados(UPPER(Nome_razao_soc))';
    DBMS_OUTPUT.PUT_LINE('Índice IDX_ANUNC_NOME criado');
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE = -955 THEN
            DBMS_OUTPUT.PUT_LINE('Índice IDX_ANUNC_NOME já existe');
        ELSE
            RAISE;
        END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'CREATE INDEX IDX_CAMP_TITULO ON Campanha_Dados(UPPER(Titulo))';
    DBMS_OUTPUT.PUT_LINE('Índice IDX_CAMP_TITULO criado');
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE = -955 THEN
            DBMS_OUTPUT.PUT_LINE('Índice IDX_CAMP_TITULO já existe');
        ELSE
            RAISE;
        END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'CREATE INDEX IDX_PECA_TITULO ON Pecas_Criativas(UPPER(Titulo))';
    DBMS_OUTPUT.PUT_LINE('Índice IDX_PECA_TITULO criado');
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE = -955 THEN
            DBMS_OUTPUT.PUT_LINE('Índice IDX_PECA_TITULO já existe');
        ELSE
            RAISE;
        END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'CREATE INDEX IDX_ESPACO_LOCAL ON Espaco_Dados(UPPER(Local_fis_dig))';
    DBMS_OUTPUT.PUT_LINE('Índice IDX_ESPACO_LOCAL criado');
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE = -955 THEN
            DBMS_OUTPUT.PUT_LINE('Índice IDX_ESPACO_LOCAL já existe');
        ELSE
            RAISE;
        END IF;
END;
/

-- Índice composto para campanhas ativas
BEGIN
    EXECUTE IMMEDIATE 'CREATE INDEX IDX_CAMP_ATIVAS ON Campanha_Dados(Data_termino, Data_inicio)';
    DBMS_OUTPUT.PUT_LINE('Índice IDX_CAMP_ATIVAS criado');
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE = -955 THEN
            DBMS_OUTPUT.PUT_LINE('Índice IDX_CAMP_ATIVAS já existe');
        ELSE
            RAISE;
        END IF;
END;
/

-- ----------------------------------------------------------------------------
-- 15. TESTE RÁPIDO
-- ----------------------------------------------------------------------------
SELECT 'Testando VIEW V_PESQUISA_GLOBAL...' AS STATUS FROM DUAL;
SELECT COUNT(*) AS TOTAL_REGISTROS FROM V_PESQUISA_GLOBAL;

SELECT 'Testando VIEW V_STATS_PESQUISA...' AS STATUS FROM DUAL;
SELECT * FROM V_STATS_PESQUISA;

-- ----------------------------------------------------------------------------
-- COMMIT E MENSAGEM FINAL
-- ----------------------------------------------------------------------------
COMMIT;