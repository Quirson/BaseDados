-- ============================================================================
-- VIEWS PROFISSIONAIS - ANALYTICS E RELATÓRIOS
-- ============================================================================

-- ============================================================================
-- VIEW: VW_CAMPANHAS_ATIVAS
-- Descrição: Todas as campanhas em andamento com dados do anunciante
-- ============================================================================
CREATE OR REPLACE VIEW VW_CAMPANHAS_ATIVAS AS
SELECT
    c.Cod_camp,
    c.Titulo,
    a.Nome_razao_soc,
    a.Cat_negocio,
    c.Orc_alocado,
    c.Data_inicio,
    c.Data_termino,
    c.Objectivo,
    TRUNC((c.Data_termino - SYSDATE)) as Dias_restantes,
    CASE
        WHEN TRUNC((c.Data_termino - SYSDATE)) <= 7 THEN 'Urgente'
        WHEN TRUNC((c.Data_termino - SYSDATE)) <= 30 THEN 'Atenção'
        ELSE 'Normal'
    END as Prioridade
FROM Campanha_Dados c
JOIN Anunciante_Dados a ON c.Num_id_fiscal = a.Num_id_fiscal
WHERE c.Data_termino >= SYSDATE
ORDER BY c.Data_termino ASC;

-- ============================================================================
-- VIEW: VW_DESEMPENHO_ANUNCIANTES
-- Descrição: Performance e uso de crédito por anunciante
-- ============================================================================
CREATE OR REPLACE VIEW VW_DESEMPENHO_ANUNCIANTES AS
SELECT
    a.Num_id_fiscal,
    a.Nome_razao_soc,
    a.Lim_cred_aprov,
    ROUND(NVL(SUM(c.Orc_alocado), 0), 2) as Orcamento_usado,
    ROUND(a.Lim_cred_aprov - NVL(SUM(c.Orc_alocado), 0), 2) as Credito_disponivel,
    ROUND((NVL(SUM(c.Orc_alocado), 0) / a.Lim_cred_aprov) * 100, 2) as Percentual_uso,
    COUNT(c.Cod_camp) as Campanhas_ativas
FROM Anunciante_Dados a
LEFT JOIN Campanha_Dados c ON a.Num_id_fiscal = c.Num_id_fiscal
    AND c.Data_termino >= SYSDATE
GROUP BY a.Num_id_fiscal, a.Nome_razao_soc, a.Lim_cred_aprov
ORDER BY Percentual_uso DESC;

-- ============================================================================
-- VIEW: VW_RECEITA_MENSAL
-- Descrição: Receita gerada por mês
-- ============================================================================
CREATE OR REPLACE VIEW VW_RECEITA_MENSAL AS
SELECT
    TO_CHAR(c.Data_inicio, 'YYYY-MM') as Mes,
    ROUND(SUM(c.Orc_alocado), 2) as Receita_total,
    COUNT(DISTINCT c.Cod_camp) as Total_campanhas,
    COUNT(DISTINCT c.Num_id_fiscal) as Total_anunciantes,
    ROUND(AVG(c.Orc_alocado), 2) as Media_orcamento
FROM Campanha_Dados c
GROUP BY TO_CHAR(c.Data_inicio, 'YYYY-MM')
ORDER BY Mes DESC;

-- ============================================================================
-- VIEW: VW_ANALISE_PAGAMENTOS
-- Descrição: Status e análise de pagamentos
-- ============================================================================
CREATE OR REPLACE VIEW VW_ANALISE_PAGAMENTOS AS
SELECT
    a.Nome_razao_soc,
    COUNT(p.Cod_pag) as Total_pagamentos,
    ROUND(SUM(p.Valor_pag), 2) as Valor_total_pago,
    ROUND(SUM(CASE WHEN p.Status_pag = 'Pendente' THEN p.Valor_pag ELSE 0 END), 2) as Valor_pendente,
    ROUND(SUM(CASE WHEN p.Status_pag = 'Pago' THEN p.Valor_pag ELSE 0 END), 2) as Valor_recebido,
    COUNT(CASE WHEN p.Status_pag = 'Pendente' THEN 1 END) as Pagamentos_pendentes
FROM Anunciante_Dados a
LEFT JOIN Pagamento_Dados p ON a.Num_id_fiscal = p.Num_id_fiscal
GROUP BY a.Nome_razao_soc
ORDER BY Valor_pendente DESC;
