-- TRIGGERS PARA AUDITORIA E INTEGRIDADE

CREATE SEQUENCE seq_log_auditoria
  START WITH 1
  INCREMENT BY 1
  NOCACHE;

CREATE OR REPLACE TRIGGER trg_audita_orcamento_campanha
AFTER UPDATE OF Orc_alocado ON Campanha_Dados
FOR EACH ROW
WHEN (NEW.Orc_alocado <> OLD.Orc_alocado)
BEGIN
    INSERT INTO Log_Auditoria_Orcamento (
        Id_log,
        Cod_camp,
        Data_alteracao,
        User_alterou,
        Valor_antigo,
        Valor_novo
    )
    VALUES (
        seq_log_auditoria.NEXTVAL,
        :OLD.Cod_camp,
        SYSDATE,
        USER,
        :OLD.Orc_alocado,
        :NEW.Orc_alocado
    );
END;
/

COMMIT;
