-- Grupo: Eden Magnus, Francisco Guamba, Malik Dauto, Quirson Ngale
-- Data: Outubro 2025
-- SGBD: Oracle Database
-- ============================================================================

-- ============================================================================
-- BLOCO 1: TABELAS INDEPENDENTES (SEM CHAVES ESTRANGEIRAS)
-- ============================================================================
ALTER SESSION SET NLS_LANGUAGE='PORTUGUESE'; -- Para Portugues na Hora da Compilacao nao dar Errado
ALTER SESSION SET NLS_TERRITORY='PORTUGAL'; -- Portugal Por Causa do Portugues
-- ----------------------------------------------------------------------------
-- Tabela: ANUNCIANTE_DADOS
-- Descrição: Armazena informações dos anunciantes (clientes)
-- ----------------------------------------------------------------------------
CREATE TABLE Anunciante_Dados (
    Num_id_fiscal    NUMBER(7) PRIMARY KEY,
    Nome_razao_soc   VARCHAR2(255) NOT NULL,
    Cat_negocio      VARCHAR2(255) NOT NULL,
    Porte            VARCHAR2(50) NOT NULL
        CHECK (Porte IN ('Pequeno', 'Médio', 'Grande')),
    Endereco         VARCHAR2(255) NOT NULL,
    Contactos        VARCHAR2(255) NOT NULL,
    Rep_legal        VARCHAR2(255) NOT NULL,
    Historico_camp   CLOB,
    Pref_com         VARCHAR2(255) NOT NULL,
    Lim_cred_aprov   NUMBER(10,2) NOT NULL
        CHECK (Lim_cred_aprov >= 0),
    Classif_conf     VARCHAR2(50) NOT NULL
        CHECK (Classif_conf IN ('AAA - Excelente', 'AA - Muito Bom', 'A - Bom', 'B - Regular', 'C - Baixo'))
);

-- ----------------------------------------------------------------------------
-- Tabela: AGENCIA_DADOS
-- Descrição: Armazena informações das agências de publicidade
-- ----------------------------------------------------------------------------
CREATE TABLE Agencia_Dados (
    Reg_comercial    NUMBER(7) PRIMARY KEY,
    Nome_age         VARCHAR2(100) NOT NULL,
    Portif_clientes  CLOB,
    Equip_principal  VARCHAR2(100) NOT NULL,
    Cap_tecnicas     VARCHAR2(255) NOT NULL,
    Historico_camp   VARCHAR2(255),
    Aval_desemp      NUMBER(3) NOT NULL
        CHECK (Aval_desemp BETWEEN 0 AND 100)
);

-- ----------------------------------------------------------------------------
-- Tabela: ESPACO_DADOS
-- Descrição: Armazena informações dos espaços publicitários
-- ----------------------------------------------------------------------------
CREATE TABLE Espaco_Dados (
    Id_espaco        NUMBER(7) PRIMARY KEY,
    Local_fis_dig    VARCHAR2(255) NOT NULL,
    Tipo             VARCHAR2(100) NOT NULL,
    Dimensoes        VARCHAR2(100) NOT NULL,
    Resolucao        VARCHAR2(50),
    Visibilidade     VARCHAR2(100) NOT NULL,
    Horario_maior    VARCHAR2(100),
    Preco_base       NUMBER(10,2) NOT NULL
        CHECK (Preco_base > 0),
    Disponibilidade  VARCHAR2(50) NOT NULL
        CHECK (Disponibilidade IN ('Disponível', 'Ocupado', 'Manutenção', 'Sempre Disponível')),
    Proprietario     VARCHAR2(255) NOT NULL,
    Historico_ocup   CLOB
);

-- ----------------------------------------------------------------------------
-- Tabela: PUBLICO_ALVO
-- Descrição: Armazena informações sobre segmentação de público-alvo
-- ----------------------------------------------------------------------------
CREATE TABLE Publico_Alvo (
    Id_publicoAlvo   NUMBER(7) PRIMARY KEY,
    Seg_demograf     CLOB NOT NULL,
    Seg_comport      CLOB NOT NULL,
    Seg_psicograf    CLOB NOT NULL,
    Seg_context      CLOB NOT NULL
);

-- ----------------------------------------------------------------------------
-- Tabela: PROCESSO_DADOS
-- Descrição: Armazena informações dos processos de aprovação
-- ----------------------------------------------------------------------------
CREATE TABLE Processo_Dados (
    Cod_processo     NUMBER(7) PRIMARY KEY,
    Sub_materiais    VARCHAR2(255) NOT NULL,
    Verf_conf_tec    VARCHAR2(255) NOT NULL,
    Anal_norm_legais CLOB NOT NULL,
    Certif_confor    CLOB NOT NULL
);

-- ----------------------------------------------------------------------------
-- Tabela: MODALIDADE_COBRANCA (MOVIDA PARA INDEPENDENTES)
-- Descrição: Tipos de modalidades de cobrança
-- ----------------------------------------------------------------------------
CREATE TABLE Modalidade_Cobranca (
    Cod_modalidade   NUMBER(7) PRIMARY KEY,
    Modal_cobranca   VARCHAR2(50) NOT NULL UNIQUE,
    Ciclo_fat        VARCHAR2(255) NOT NULL
);

-- ----------------------------------------------------------------------------
-- Tabela: PROMOCOES (MOVIDA PARA INDEPENDENTES)
-- Descrição: Tipos de pacotes promocionais
-- ----------------------------------------------------------------------------
CREATE TABLE Promocoes (
    Cod_promocao     NUMBER(7) PRIMARY KEY,
    Pacotes_promo    VARCHAR2(100) NOT NULL UNIQUE,
    Desc_volume      NUMBER(5,2) NOT NULL
        CHECK (Desc_volume BETWEEN 0 AND 100)
);

-- ----------------------------------------------------------------------------
-- Tabela: PAGAMENTOS (REESTRUTURADA)
-- Descrição: Armazena informações de pagamentos
-- ----------------------------------------------------------------------------
CREATE TABLE Pagamentos (
    Cod_pagamento    NUMBER(7) PRIMARY KEY,
    Cod_modalidade   NUMBER(7) NOT NULL,
    Precos_dinam     NUMBER(10,2) NOT NULL
        CHECK (Precos_dinam >= 0),
    Cod_promocao     NUMBER(7),
    Metod_pagamento  VARCHAR2(50) NOT NULL,
    Comprov_veic     VARCHAR2(255),
    Reconc_financ    VARCHAR2(255),
    CONSTRAINT fk_pag_modalidade FOREIGN KEY (Cod_modalidade)
        REFERENCES Modalidade_Cobranca(Cod_modalidade),
    CONSTRAINT fk_pag_promocao FOREIGN KEY (Cod_promocao)
        REFERENCES Promocoes(Cod_promocao)
);

-- ============================================================================
-- BLOCO 2: TABELAS COM CHAVES ESTRANGEIRAS SIMPLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Tabela: PECAS_CRIATIVAS
-- Descrição: Armazena informações das peças criativas (publicitárias)
-- ----------------------------------------------------------------------------
CREATE TABLE Pecas_Criativas (
    Id_unicoPeca     NUMBER(7) PRIMARY KEY,
    Titulo           VARCHAR2(100) NOT NULL,
    Descricao        CLOB NOT NULL,
    Num_id_fiscal    NUMBER(7) NOT NULL,
    Cod_camp         NUMBER(7),
    Criador          VARCHAR2(100) NOT NULL,
    Data_criacao     DATE NOT NULL,
    Status_aprov     VARCHAR2(20) NOT NULL
        CHECK (Status_aprov IN ('Aprovado', 'Em Revisão', 'Rejeitado', 'Pendente')),
    Direitos_autorais CLOB NOT NULL,
    Classif_conteudo NUMBER(2) NOT NULL
        CHECK (Classif_conteudo BETWEEN 0 AND 18),
    Cod_processo     NUMBER(7),
    CONSTRAINT fk_peca_anunciante FOREIGN KEY (Num_id_fiscal)
        REFERENCES Anunciante_Dados(Num_id_fiscal),
    CONSTRAINT fk_peca_processo FOREIGN KEY (Cod_processo)
        REFERENCES Processo_Dados(Cod_processo)
);

-- ----------------------------------------------------------------------------
-- Tabela: CAMPANHA_DADOS
-- Descrição: Armazena informações das campanhas publicitárias
-- ----------------------------------------------------------------------------
CREATE TABLE Campanha_Dados (
    Cod_camp         NUMBER(7) PRIMARY KEY,
    Num_id_fiscal    NUMBER(7) NOT NULL,
    Titulo           VARCHAR2(100) NOT NULL,
    Objectivo        CLOB NOT NULL,
    Pub_alvo         VARCHAR2(255) NOT NULL,
    Orc_alocado      NUMBER(10,2) NOT NULL
        CHECK (Orc_alocado > 0),
    Data_inicio      DATE NOT NULL,
    Data_termino     DATE NOT NULL,
    Elem_criativos   VARCHAR2(255),
    Metri_desemp     VARCHAR2(255),
    Result_obtidos   CLOB,
    Cod_processo     NUMBER(7),
    Id_unicoPeca     NUMBER(7),
    Cod_pagamento    NUMBER(7),
    CONSTRAINT fk_camp_anunciante FOREIGN KEY (Num_id_fiscal)
        REFERENCES Anunciante_Dados(Num_id_fiscal),
    CONSTRAINT fk_camp_processo FOREIGN KEY (Cod_processo)
        REFERENCES Processo_Dados(Cod_processo),
    CONSTRAINT fk_camp_peca FOREIGN KEY (Id_unicoPeca)
        REFERENCES Pecas_Criativas(Id_unicoPeca),
    CONSTRAINT fk_camp_pagamento FOREIGN KEY (Cod_pagamento)
        REFERENCES Pagamentos(Cod_pagamento),
    CONSTRAINT ck_camp_datas CHECK (Data_termino > Data_inicio)
);

-- Atualizar FK em Pecas_Criativas que depende de Campanha
ALTER TABLE Pecas_Criativas
    ADD CONSTRAINT fk_peca_campanha FOREIGN KEY (Cod_camp)
    REFERENCES Campanha_Dados(Cod_camp);

-- ----------------------------------------------------------------------------
-- Tabela: AGENCIA_ESPECIALIDADE
-- Descrição: Especialidades das agências (multivalorado)
-- ----------------------------------------------------------------------------
CREATE TABLE Agencia_Especialidade (
    Reg_comercial    NUMBER(7),
    Especialidade    VARCHAR2(255) NOT NULL,
    PRIMARY KEY (Reg_comercial, Especialidade),
    CONSTRAINT fk_esp_agencia FOREIGN KEY (Reg_comercial)
        REFERENCES Agencia_Dados(Reg_comercial)
);

-- ----------------------------------------------------------------------------
-- Tabela: AGENCIA_CERTIFICACOES
-- Descrição: Certificações das agências (multivalorado)
-- ----------------------------------------------------------------------------
CREATE TABLE Agencia_Certificacoes (
    Reg_comercial    NUMBER(7),
    Certificacoes    VARCHAR2(255) NOT NULL,
    PRIMARY KEY (Reg_comercial, Certificacoes),
    CONSTRAINT fk_cert_agencia FOREIGN KEY (Reg_comercial)
        REFERENCES Agencia_Dados(Reg_comercial)
);

-- ----------------------------------------------------------------------------
-- Tabela: APROVACAO_NIVEL
-- Descrição: Níveis de aprovação hierárquica do processo
-- ----------------------------------------------------------------------------
CREATE TABLE Aprovacao_Nivel (
    Cod_processo     NUMBER(7) PRIMARY KEY,
    Aprov_hierar     VARCHAR2(255) NOT NULL,
    CONSTRAINT fk_aprov_processo FOREIGN KEY (Cod_processo)
        REFERENCES Processo_Dados(Cod_processo)
);

-- ----------------------------------------------------------------------------
-- Tabela: PROCESSO_REVISAO
-- Descrição: Informações sobre revisões do processo
-- ----------------------------------------------------------------------------
CREATE TABLE Processo_Revisao (
    Cod_processo     NUMBER(7) PRIMARY KEY,
    Ciclo_rev        VARCHAR2(255) NOT NULL,
    Historico_alt    VARCHAR2(255) NOT NULL,
    CONSTRAINT fk_revisao_processo FOREIGN KEY (Cod_processo)
        REFERENCES Processo_Dados(Cod_processo)
);

-- ============================================================================
-- BLOCO 3: TABELAS DE ESPECIALIZAÇÃO (PEÇAS CRIATIVAS)
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Tabela: PECAS_VISUAIS
-- Descrição: Especialização de peças criativas (visuais)
-- ----------------------------------------------------------------------------
CREATE TABLE Pecas_Visuais (
    Id_unicoPeca     NUMBER(7) PRIMARY KEY,
    Dim_pvisuais     VARCHAR2(50) NOT NULL,
    Resol_pvisuais   VARCHAR2(50) NOT NULL,
    Form_arquivo     VARCHAR2(20) NOT NULL,
    Pal_cores        VARCHAR2(255),
    El_graficos      VARCHAR2(255),
    Compat_disp_exib VARCHAR2(255),
    CONSTRAINT fk_visual_peca FOREIGN KEY (Id_unicoPeca)
        REFERENCES Pecas_Criativas(Id_unicoPeca)
);

-- ----------------------------------------------------------------------------
-- Tabela: PECAS_AUDIOVISUAIS
-- Descrição: Especialização de peças criativas (audiovisuais)
-- ----------------------------------------------------------------------------
CREATE TABLE Pecas_Audiovisuais (
    Id_unicoPeca     NUMBER(7) PRIMARY KEY,
    Duracao          VARCHAR2(20) NOT NULL,
    Qualidad_video   VARCHAR2(20) NOT NULL,
    Resol_video      VARCHAR2(20) NOT NULL,
    Legendas_disp    VARCHAR2(255),
    Req_tecnicos     VARCHAR2(255),
    CONSTRAINT fk_audio_peca FOREIGN KEY (Id_unicoPeca)
        REFERENCES Pecas_Criativas(Id_unicoPeca)
);

-- ----------------------------------------------------------------------------
-- Tabela: PECAS_INTERATIVAS
-- Descrição: Especialização de peças criativas (interativas)
-- ----------------------------------------------------------------------------
CREATE TABLE Pecas_Interativas (
    Id_unicoPeca     NUMBER(7) PRIMARY KEY,
    Tec_util         VARCHAR2(255) NOT NULL,
    Niv_interacao    VARCHAR2(20) NOT NULL
        CHECK (Niv_interacao IN ('Baixo', 'Médio', 'Alto', 'Muito Alto')),
    Req_dispositivo  VARCHAR2(255),
    Metri_engaj      NUMBER(5,2) NOT NULL
        CHECK (Metri_engaj >= 0),
    Dados_colect     CLOB,
    CONSTRAINT fk_inter_peca FOREIGN KEY (Id_unicoPeca)
        REFERENCES Pecas_Criativas(Id_unicoPeca)
);

-- ============================================================================
-- BLOCO 4: TABELAS DE RELACIONAMENTO N:M
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Tabela: ANUNCIANTE_AGENCIA
-- Descrição: Relacionamento entre Anunciantes e Agências
-- ----------------------------------------------------------------------------
CREATE TABLE Anunciante_Agencia (
    Num_id_fiscal    NUMBER(7),
    Reg_comercial    NUMBER(7),
    PRIMARY KEY (Num_id_fiscal, Reg_comercial),
    CONSTRAINT fk_anunc_agencia_anunc FOREIGN KEY (Num_id_fiscal)
        REFERENCES Anunciante_Dados(Num_id_fiscal),
    CONSTRAINT fk_anunc_agencia_ag FOREIGN KEY (Reg_comercial)
        REFERENCES Agencia_Dados(Reg_comercial)
);

-- ----------------------------------------------------------------------------
-- Tabela: CAMPANHA_ESPACO
-- Descrição: Relacionamento entre Campanhas e Espaços Publicitários
-- ----------------------------------------------------------------------------
CREATE TABLE Campanha_Espaco (
    Cod_camp         NUMBER(7),
    Id_espaco        NUMBER(7),
    PRIMARY KEY (Cod_camp, Id_espaco),
    CONSTRAINT fk_camp_esp_campanha FOREIGN KEY (Cod_camp)
        REFERENCES Campanha_Dados(Cod_camp),
    CONSTRAINT fk_camp_esp_espaco FOREIGN KEY (Id_espaco)
        REFERENCES Espaco_Dados(Id_espaco)
);

-- ----------------------------------------------------------------------------
-- Tabela: CAMPANHA_PUBLICOALVO
-- Descrição: Relacionamento entre Campanhas e Público-Alvo
-- ----------------------------------------------------------------------------
CREATE TABLE Campanha_PublicoAlvo (
    Cod_camp         NUMBER(7),
    Id_publicoAlvo   NUMBER(7),
    PRIMARY KEY (Cod_camp, Id_publicoAlvo),
    CONSTRAINT fk_camp_pub_campanha FOREIGN KEY (Cod_camp)
        REFERENCES Campanha_Dados(Cod_camp),
    CONSTRAINT fk_camp_pub_publico FOREIGN KEY (Id_publicoAlvo)
        REFERENCES Publico_Alvo(Id_publicoAlvo)
);

-- ----------------------------------------------------------------------------
-- Tabela: CAMPANHA_CANAL
-- Descrição: Canais utilizados nas campanhas (multivalorado)
-- ----------------------------------------------------------------------------
CREATE TABLE Campanha_Canal (
    Cod_camp         NUMBER(7),
    Canais_util      VARCHAR2(255) NOT NULL,
    PRIMARY KEY (Cod_camp, Canais_util),
    CONSTRAINT fk_canal_campanha FOREIGN KEY (Cod_camp)
        REFERENCES Campanha_Dados(Cod_camp)
);

-- ----------------------------------------------------------------------------
-- Tabela: ESPACO_PECA
-- Descrição: Relacionamento entre Espaços e Peças Criativas
-- ----------------------------------------------------------------------------
CREATE TABLE Espaco_Peca (
    Id_espaco        NUMBER(7),
    Id_unicoPeca     NUMBER(7),
    PRIMARY KEY (Id_espaco, Id_unicoPeca),
    CONSTRAINT fk_esp_peca_espaco FOREIGN KEY (Id_espaco)
        REFERENCES Espaco_Dados(Id_espaco),
    CONSTRAINT fk_esp_peca_peca FOREIGN KEY (Id_unicoPeca)
        REFERENCES Pecas_Criativas(Id_unicoPeca)
);

-- ============================================================================
-- FIM DO SCRIPT DE CRIAÇÃO
-- ============================================================================

SELECT 'Base de dados criada com sucesso!' AS Status FROM DUAL;