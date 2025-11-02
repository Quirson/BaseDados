-- ÍNDICES PARA PERFORMANCE

CREATE INDEX idx_campanha_nif ON Campanha_Dados(Num_id_fiscal);
CREATE INDEX idx_campanha_peca ON Campanha_Dados(Id_unicoPeca);
CREATE INDEX idx_peca_nif ON Pecas_Criativas(Num_id_fiscal);
CREATE INDEX idx_camp_esp_camp ON Campanha_Espaco(Cod_camp);
CREATE INDEX idx_camp_esp_esp ON Campanha_Espaco(Id_espaco);
CREATE INDEX idx_anunciante_nome ON Anunciante_Dados(Nome_razao_soc);

COMMIT;
