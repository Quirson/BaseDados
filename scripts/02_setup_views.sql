-- VIEWS PROFISSIONAIS PARA ANÁLISE

CREATE OR REPLACE VIEW v_campanhas_ativas AS
SELECT
    c.Cod_camp,
    c.Titulo AS Campanha_Titulo,
    c.Objectivo,
    c.Orc_alocado,
    c.Data_inicio,
    c.Data_termino,
    a.Nome_razao_soc AS Anunciante,
    (SELECT LISTAGG(e.Local_fis_dig, '; ') WITHIN GROUP (ORDER BY e.Local_fis_dig)
     FROM Campanha_Espaco ce
     JOIN Espaco_Dados e ON ce.Id_espaco = e.Id_espaco
     WHERE ce.Cod_camp = c.Cod_camp) AS Espacos_Utilizados
FROM
    Campanha_Dados c
JOIN
    Anunciante_Dados a ON c.Num_id_fiscal = a.Num_id_fiscal
WHERE
    c.Data_termino >= SYSDATE;

CREATE OR REPLACE VIEW v_performance_anunciantes AS
SELECT
    a.Num_id_fiscal,
    a.Nome_razao_soc,
    COUNT(DISTINCT c.Cod_camp) as Total_Campanhas,
    ROUND(AVG(c.Orc_alocado), 2) as Orcamento_Medio,
    SUM(c.Orc_alocado) as Orcamento_Total
FROM
    Anunciante_Dados a
LEFT JOIN
    Campanha_Dados c ON a.Num_id_fiscal = c.Num_id_fiscal
GROUP BY
    a.Num_id_fiscal,
    a.Nome_razao_soc
ORDER BY
    Orcamento_Total DESC;

COMMIT;
