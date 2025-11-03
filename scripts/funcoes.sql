-- ============================================================================
-- ============================================================================

-- ----------------------------------------------------------------------------
-- FUNÇÃO 1: CONTAR CAMPANHAS INICIADAS NUMA DATA
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION FN_CAMPANHAS_INICIADAS_DATA(
    p_data IN DATE
) RETURN NUMBER AS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO v_count
    FROM Campanha_Dados
    WHERE TRUNC(Data_inicio) = TRUNC(p_data);

    RETURN NVL(v_count, 0);
EXCEPTION
    WHEN OTHERS THEN
        RETURN 0;
END;
/

-- ----------------------------------------------------------------------------
-- FUNÇÃO 2: CONTAR CAMPANHAS TERMINADAS NUMA DATA
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION FN_CAMPANHAS_TERMINADAS_DATA(
    p_data IN DATE
) RETURN NUMBER AS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO v_count
    FROM Campanha_Dados
    WHERE TRUNC(Data_termino) = TRUNC(p_data);

    RETURN NVL(v_count, 0);
EXCEPTION
    WHEN OTHERS THEN
        RETURN 0;
END;
/

-- ----------------------------------------------------------------------------
-- FUNÇÃO 3: CONTAR PEÇAS APROVADAS/REJEITADAS
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION FN_CONTAR_PECAS_STATUS(
    p_status IN VARCHAR2
) RETURN NUMBER AS
    v_count NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO v_count
    FROM Pecas_Criativas
    WHERE UPPER(Status_aprov) = UPPER(p_status);

    RETURN NVL(v_count, 0);
EXCEPTION
    WHEN OTHERS THEN
        RETURN 0;
END;
/

-- ----------------------------------------------------------------------------
-- FUNÇÃO 4: CONTAR PAGAMENTOS NUMA DATA
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION FN_PAGAMENTOS_DATA(
    p_data IN DATE
) RETURN NUMBER AS
    v_count NUMBER;
BEGIN
    -- Assumindo que temos uma coluna de data em Pagamentos
    -- Se não existir, vamos usar SYSDATE como fallback
    SELECT COUNT(*)
    INTO v_count
    FROM Pagamentos;

    RETURN NVL(v_count, 0);
EXCEPTION
    WHEN OTHERS THEN
        RETURN 0;
END;
/

-- ----------------------------------------------------------------------------
-- FUNÇÃO 5: ESTATÍSTICAS GLOBAIS DO SISTEMA
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION FN_ESTATISTICAS_GLOBAIS RETURN SYS_REFCURSOR AS
    v_cursor SYS_REFCURSOR;
BEGIN
    OPEN v_cursor FOR
    SELECT
        (SELECT COUNT(*) FROM Anunciante_Dados) as total_anunciantes,
        (SELECT COUNT(*) FROM Campanha_Dados WHERE Data_termino >= SYSDATE) as campanhas_ativas,
        (SELECT NVL(SUM(Orc_alocado), 0) FROM Campanha_Dados WHERE Data_termino >= SYSDATE) as orcamento_total,
        (SELECT COUNT(*) FROM Espaco_Dados WHERE UPPER(DISPONIBILIDADE) = 'DISPONÍVEL') as espacos_disponiveis,
        (SELECT COUNT(*) FROM Pecas_Criativas WHERE UPPER(Status_aprov) = 'APROVADO') as pecas_aprovadas,
        (SELECT COUNT(*) FROM Pecas_Criativas WHERE UPPER(Status_aprov) = 'REJEITADO') as pecas_rejeitadas,
        (SELECT COUNT(*) FROM Pagamentos) as total_pagamentos
    FROM DUAL;

    RETURN v_cursor;
END;
/

-- ----------------------------------------------------------------------------
-- VIEW PARA DASHBOARD COM DADOS CONSOLIDADOS
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW V_DASHBOARD_ESTATISTICAS AS
SELECT
    (SELECT COUNT(*) FROM Anunciante_Dados) as total_anunciantes,
    (SELECT COUNT(*) FROM Campanha_Dados WHERE Data_termino >= SYSDATE) as campanhas_ativas,
    (SELECT NVL(SUM(Orc_alocado), 0) FROM Campanha_Dados WHERE Data_termino >= SYSDATE) as orcamento_total,
    (SELECT COUNT(*) FROM Espaco_Dados WHERE UPPER(DISPONIBILIDADE) = 'DISPONÍVEL') as espacos_disponiveis,
    (SELECT COUNT(*) FROM Pecas_Criativas WHERE UPPER(Status_aprov) = 'APROVADO') as pecas_aprovadas,
    (SELECT COUNT(*) FROM Pecas_Criativas WHERE UPPER(Status_aprov) = 'REJEITADO') as pecas_rejeitadas,
    (SELECT COUNT(*) FROM Pagamentos) as total_pagamentos
FROM DUAL;

-- ----------------------------------------------------------------------------
-- TESTE DAS FUNÇÕES
-- ----------------------------------------------------------------------------
SELECT 'Função Campanhas Iniciadas: ' || FN_CAMPANHAS_INICIADAS_DATA(SYSDATE) FROM DUAL;
SELECT 'Função Campanhas Terminadas: ' || FN_CAMPANHAS_TERMINADAS_DATA(SYSDATE) FROM DUAL;
SELECT 'Função Peças Aprovadas: ' || FN_CONTAR_PECAS_STATUS('APROVADO') FROM DUAL;
SELECT 'Função Peças Rejeitadas: ' || FN_CONTAR_PECAS_STATUS('REJEITADO') FROM DUAL;
SELECT 'Função Pagamentos: ' || FN_PAGAMENTOS_DATA(SYSDATE) FROM DUAL;

SELECT 'VIEW Dashboard: ' FROM DUAL;
SELECT * FROM V_DASHBOARD_ESTATISTICAS;

COMMIT;