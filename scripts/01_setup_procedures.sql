-- 🚀 PROCEDURES CRÍTICAS PARA O SISTEMA

-- 1. PROCEDURE: GESTÃO COMPLETA DE CAMPANHAS
CREATE OR REPLACE PROCEDURE sp_inserir_campanha_completa (
    p_num_id_fiscal    IN Campanha_Dados.Num_id_fiscal%TYPE,
    p_titulo          IN Campanha_Dados.Titulo%TYPE,
    p_objectivo       IN Campanha_Dados.Objectivo%TYPE,
    p_pub_alvo        IN Campanha_Dados.Pub_alvo%TYPE,
    p_orc_alocado     IN Campanha_Dados.Orc_alocado%TYPE,
    p_data_inicio     IN VARCHAR2,
    p_data_termino    IN VARCHAR2,
    p_espacos_ids     IN VARCHAR2 DEFAULT NULL,
    p_publico_ids     IN VARCHAR2 DEFAULT NULL,
    p_canais          IN VARCHAR2 DEFAULT NULL
)
IS
    v_cod_camp NUMBER;
    v_limite_cred NUMBER;
BEGIN
    BEGIN
        SELECT Lim_cred_aprov INTO v_limite_cred
        FROM Anunciante_Dados
        WHERE Num_id_fiscal = p_num_id_fiscal;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20001, 'Anunciante não encontrado: ' || p_num_id_fiscal);
    END;

    IF p_orc_alocado > v_limite_cred THEN
        RAISE_APPLICATION_ERROR(-20002, 'Orçamento excede limite de crédito. Limite: ' || v_limite_cred);
    END IF;

    SELECT NVL(MAX(Cod_camp), 8000000) + 1 INTO v_cod_camp FROM Campanha_Dados;

    INSERT INTO Campanha_Dados (
        Cod_camp, Num_id_fiscal, Titulo, Objectivo, Pub_alvo,
        Orc_alocado, Data_inicio, Data_termino
    ) VALUES (
        v_cod_camp, p_num_id_fiscal, p_titulo, p_objectivo, p_pub_alvo,
        p_orc_alocado, TO_DATE(p_data_inicio, 'DD/MM/YYYY'), TO_DATE(p_data_termino, 'DD/MM/YYYY')
    );

    IF p_espacos_ids IS NOT NULL THEN
        FOR i IN (SELECT TRIM(REGEXP_SUBSTR(p_espacos_ids, '[^,]+', 1, LEVEL)) AS espaco_id
                  FROM DUAL
                  CONNECT BY REGEXP_SUBSTR(p_espacos_ids, '[^,]+', 1, LEVEL) IS NOT NULL)
        LOOP
            INSERT INTO Campanha_Espaco (Cod_camp, Id_espaco)
            VALUES (v_cod_camp, i.espaco_id);
        END LOOP;
    END IF;

    IF p_publico_ids IS NOT NULL THEN
        FOR i IN (SELECT TRIM(REGEXP_SUBSTR(p_publico_ids, '[^,]+', 1, LEVEL)) AS publico_id
                  FROM DUAL
                  CONNECT BY REGEXP_SUBSTR(p_publico_ids, '[^,]+', 1, LEVEL) IS NOT NULL)
        LOOP
            INSERT INTO Campanha_PublicoAlvo (Cod_camp, Id_publicoAlvo)
            VALUES (v_cod_camp, i.publico_id);
        END LOOP;
    END IF;

    IF p_canais IS NOT NULL THEN
        FOR i IN (SELECT TRIM(REGEXP_SUBSTR(p_canais, '[^,]+', 1, LEVEL)) AS canal
                  FROM DUAL
                  CONNECT BY REGEXP_SUBSTR(p_canais, '[^,]+', 1, LEVEL) IS NOT NULL)
        LOOP
            INSERT INTO Campanha_Canal (Cod_camp, Canais_util)
            VALUES (v_cod_camp, i.canal);
        END LOOP;
    END IF;

    COMMIT;

EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
END sp_inserir_campanha_completa;
/

-- 2. FUNCTION: CALCULAR CUSTO TOTAL COM DESCONTO
CREATE OR REPLACE FUNCTION fn_calcular_custo_total_campanha (
    p_cod_camp IN Campanha_Dados.Cod_camp%TYPE
) RETURN NUMBER
IS
    v_custo_base NUMBER := 0;
    v_desconto NUMBER := 0;
BEGIN
    SELECT NVL(SUM(e.Preco_base), 0)
    INTO v_custo_base
    FROM Campanha_Espaco ce
    JOIN Espaco_Dados e ON ce.Id_espaco = e.Id_espaco
    WHERE ce.Cod_camp = p_cod_camp;

    RETURN v_custo_base;

EXCEPTION
    WHEN OTHERS THEN
        RETURN 0;
END fn_calcular_custo_total_campanha;
/

-- 3. PROCEDURE: RELATÓRIO FINANCEIRO
CREATE OR REPLACE PROCEDURE sp_relatorio_financeiro_anunciante (
    p_nif IN Anunciante_Dados.Num_id_fiscal%TYPE,
    p_cursor OUT SYS_REFCURSOR
)
IS
BEGIN
    OPEN p_cursor FOR
    SELECT
        c.Cod_camp,
        c.Titulo AS Campanha,
        c.Orc_alocado AS Orcamento,
        fn_calcular_custo_total_campanha(c.Cod_camp) AS Custo_Real,
        (c.Orc_alocado - fn_calcular_custo_total_campanha(c.Cod_camp)) AS Resultado
    FROM Campanha_Dados c
    WHERE c.Num_id_fiscal = p_nif
    ORDER BY c.Data_inicio DESC;
END sp_relatorio_financeiro_anunciante;
/

-- 4. PROCEDURE: APROVAÇÃO DE PEÇAS
CREATE OR REPLACE PROCEDURE sp_aprovar_rejeitar_peca (
    p_id_peca IN Pecas_Criativas.Id_unicoPeca%TYPE,
    p_novo_status IN Pecas_Criativas.Status_aprov%TYPE,
    p_justificativa IN VARCHAR2 DEFAULT NULL
)
IS
BEGIN
    UPDATE Pecas_Criativas
    SET Status_aprov = p_novo_status
    WHERE Id_unicoPeca = p_id_peca;

    COMMIT;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20003, 'Peça criativa não encontrada: ' || p_id_peca);
END sp_aprovar_rejeitar_peca;
/

-- 5. PROCEDURE: ESTATÍSTICAS DO SISTEMA
CREATE OR REPLACE PROCEDURE sp_estatisticas_sistema (
    p_cursor OUT SYS_REFCURSOR
)
IS
BEGIN
    OPEN p_cursor FOR
    SELECT
        (SELECT COUNT(*) FROM Anunciante_Dados) as total_anunciantes,
        (SELECT COUNT(*) FROM Campanha_Dados) as total_campanhas,
        (SELECT COUNT(*) FROM Campanha_Dados WHERE Data_termino >= SYSDATE) as campanhas_ativas,
        (SELECT COUNT(*) FROM Espaco_Dados) as total_espacos,
        (SELECT COUNT(*) FROM Espaco_Dados WHERE Disponibilidade = 'Disponível') as espacos_disponiveis,
        (SELECT NVL(SUM(Orc_alocado), 0) FROM Campanha_Dados WHERE Data_termino >= SYSDATE) as orcamento_total_ativas
    FROM DUAL;
END sp_estatisticas_sistema;
/

COMMIT;
