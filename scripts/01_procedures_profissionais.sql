-- ============================================================================
-- PROCEDURES PROFISSIONAIS - GESTÃO DE PUBLICIDADE INC MOÇAMBIQUE
-- ============================================================================

-- ============================================================================
-- PROCEDURE: CRIAR_CAMPANHA_SEGURA
-- Descrição: Cria campanha com validação completa e auditoria
-- ============================================================================
CREATE OR REPLACE PROCEDURE CRIAR_CAMPANHA_SEGURA(
    p_cod_camp IN NUMBER,
    p_num_id_fiscal IN NUMBER,
    p_titulo IN VARCHAR2,
    p_desc_camp IN CLOB,
    p_data_inicio IN DATE,
    p_data_termino IN DATE,
    p_orc_alocado IN NUMBER,
    p_objectivo IN VARCHAR2,
    p_status OUT VARCHAR2,
    p_mensagem OUT VARCHAR2
) AS
    v_anunciante_existe NUMBER;
    v_limite_credito NUMBER;
    v_orcamento_usado NUMBER;
BEGIN
    -- Validação 1: Anunciante existe?
    SELECT COUNT(*) INTO v_anunciante_existe
    FROM Anunciante_Dados
    WHERE Num_id_fiscal = p_num_id_fiscal;

    IF v_anunciante_existe = 0 THEN
        p_status := 'ERRO';
        p_mensagem := 'Anunciante não encontrado';
        RETURN;
    END IF;

    -- Validação 2: Datas válidas?
    IF p_data_inicio >= p_data_termino THEN
        p_status := 'ERRO';
        p_mensagem := 'Data de início deve ser antes da data de término';
        RETURN;
    END IF;

    -- Validação 3: Orçamento > 0?
    IF p_orc_alocado <= 0 THEN
        p_status := 'ERRO';
        p_mensagem := 'Orçamento deve ser maior que zero';
        RETURN;
    END IF;

    -- Validação 4: Limite de crédito?
    SELECT Lim_cred_aprov INTO v_limite_credito
    FROM Anunciante_Dados
    WHERE Num_id_fiscal = p_num_id_fiscal;

    SELECT NVL(SUM(Orc_alocado), 0) INTO v_orcamento_usado
    FROM Campanha_Dados
    WHERE Num_id_fiscal = p_num_id_fiscal
    AND Data_termino >= SYSDATE;

    IF (v_orcamento_usado + p_orc_alocado) > v_limite_credito THEN
        p_status := 'ERRO';
        p_mensagem := 'Orçamento excede limite de crédito aprovado';
        RETURN;
    END IF;

    -- Inserir campanha
    INSERT INTO Campanha_Dados(
        Cod_camp, Num_id_fiscal, Titulo, Desc_camp,
        Data_inicio, Data_termino, Orc_alocado, Objectivo, Status_camp
    ) VALUES(
        p_cod_camp, p_num_id_fiscal, p_titulo, p_desc_camp,
        p_data_inicio, p_data_termino, p_orc_alocado, p_objectivo, 'Ativa'
    );

    COMMIT;
    p_status := 'SUCESSO';
    p_mensagem := 'Campanha criada com sucesso';

EXCEPTION WHEN OTHERS THEN
    ROLLBACK;
    p_status := 'ERRO';
    p_mensagem := SQLERRM;
END CRIAR_CAMPANHA_SEGURA;
/

-- ============================================================================
-- PROCEDURE: ATUALIZAR_STATUS_ESPACOS
-- Descrição: Atualiza status de espaços após campanha terminar
-- ============================================================================
CREATE OR REPLACE PROCEDURE ATUALIZAR_STATUS_ESPACOS(
    p_cod_camp IN NUMBER,
    p_status OUT VARCHAR2
) AS
BEGIN
    UPDATE Espaco_Dados
    SET Status_disp = 'Disponível',
        Data_atualizacao = SYSDATE
    WHERE Cod_camp = p_cod_camp;

    COMMIT;
    p_status := 'Espaços atualizado com sucesso';
EXCEPTION WHEN OTHERS THEN
    ROLLBACK;
    p_status := SQLERRM;
END ATUALIZAR_STATUS_ESPACOS;
/

-- ============================================================================
-- FUNCTION: CALCULAR_RECEITA_TOTAL
-- Descrição: Calcula receita total de um anunciante
-- ============================================================================
CREATE OR REPLACE FUNCTION CALCULAR_RECEITA_TOTAL(
    p_num_id_fiscal IN NUMBER
) RETURN NUMBER AS
    v_receita NUMBER := 0;
BEGIN
    SELECT NVL(SUM(Orc_alocado), 0) INTO v_receita
    FROM Campanha_Dados
    WHERE Num_id_fiscal = p_num_id_fiscal
    AND Data_termino >= TRUNC(SYSDATE, 'YYYY');

    RETURN v_receita;
END CALCULAR_RECEITA_TOTAL;
/

-- ============================================================================
-- FUNCTION: VERIFICAR_DISPONIBILIDADE_ESPACO
-- Descrição: Verifica se espaço está disponível para período
-- ============================================================================
CREATE OR REPLACE FUNCTION VERIFICAR_DISPONIBILIDADE_ESPACO(
    p_cod_espaco IN NUMBER,
    p_data_inicio IN DATE,
    p_data_termino IN DATE
) RETURN BOOLEAN AS
    v_conflitos NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_conflitos
    FROM Espaco_Dados e
    JOIN Campanha_Dados c ON e.Cod_camp = c.Cod_camp
    WHERE e.Cod_espaco = p_cod_espaco
    AND c.Data_inicio < p_data_termino
    AND c.Data_termino > p_data_inicio;

    RETURN v_conflitos = 0;
END VERIFICAR_DISPONIBILIDADE_ESPACO;
/
