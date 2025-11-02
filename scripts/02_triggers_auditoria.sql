-- ============================================================================
-- TRIGGERS - AUDITORIA E VALIDAÇÃO AUTOMÁTICA
-- ============================================================================

-- ============================================================================
-- TRIGGER: TRG_VALIDAR_LIMITE_CREDITO
-- Descrição: Valida limite de crédito antes de inserir campanha
-- ============================================================================
CREATE OR REPLACE TRIGGER TRG_VALIDAR_LIMITE_CREDITO
BEFORE INSERT ON Campanha_Dados
FOR EACH ROW
DECLARE
    v_limite NUMBER;
    v_usado NUMBER;
BEGIN
    SELECT Lim_cred_aprov INTO v_limite
    FROM Anunciante_Dados
    WHERE Num_id_fiscal = :NEW.Num_id_fiscal;

    SELECT NVL(SUM(Orc_alocado), 0) INTO v_usado
    FROM Campanha_Dados
    WHERE Num_id_fiscal = :NEW.Num_id_fiscal
    AND Data_termino >= SYSDATE;

    IF (v_usado + :NEW.Orc_alocado) > v_limite THEN
        RAISE_APPLICATION_ERROR(-20001,
            'Orçamento solicitado excede limite de crédito');
    END IF;
END TRG_VALIDAR_LIMITE_CREDITO;
/

-- ============================================================================
-- TRIGGER: TRG_AUDITORIA_PAGAMENTOS
-- Descrição: Registra todas as alterações em pagamentos
-- ============================================================================
CREATE OR REPLACE TRIGGER TRG_AUDITORIA_PAGAMENTOS
AFTER INSERT OR UPDATE OR DELETE ON Pagamento_Dados
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        INSERT INTO Auditoria(
            Tabela, Operacao, Num_registro, Data_operacao, Usuario
        ) VALUES(
            'PAGAMENTO_DADOS', 'INSERT', :NEW.Cod_pag, SYSDATE, USER
        );
    ELSIF UPDATING THEN
        INSERT INTO Auditoria(
            Tabela, Operacao, Num_registro, Data_operacao, Usuario
        ) VALUES(
            'PAGAMENTO_DADOS', 'UPDATE', :NEW.Cod_pag, SYSDATE, USER
        );
    ELSIF DELETING THEN
        INSERT INTO Auditoria(
            Tabela, Operacao, Num_registro, Data_operacao, Usuario
        ) VALUES(
            'PAGAMENTO_DADOS', 'DELETE', :OLD.Cod_pag, SYSDATE, USER
        );
    END IF;
END TRG_AUDITORIA_PAGAMENTOS;
/

-- ============================================================================
-- TRIGGER: TRG_ATUALIZAR_DATA_MODIFICACAO
-- Descrição: Atualiza automaticamente data_atualizacao em todas as tabelas
-- ============================================================================
CREATE OR REPLACE TRIGGER TRG_ATUALIZAR_DATA_ATUALIZACAO_CAMPANHA
BEFORE UPDATE ON Campanha_Dados
FOR EACH ROW
BEGIN
    :NEW.Data_atualizacao := SYSDATE;
END TRG_ATUALIZAR_DATA_ATUALIZACAO_CAMPANHA;
/

CREATE OR REPLACE TRIGGER TRG_ATUALIZAR_DATA_ATUALIZACAO_ANUNCIANTE
BEFORE UPDATE ON Anunciante_Dados
FOR EACH ROW
BEGIN
    :NEW.Data_atualizacao := SYSDATE;
END TRG_ATUALIZAR_DATA_ATUALIZACAO_ANUNCIANTE;
/
