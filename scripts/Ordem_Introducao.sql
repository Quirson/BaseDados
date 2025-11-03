-- ============================================================================
-- Grupo: Eden Magnus, Francisco Guamba, Malik Dauto, Quirson Ngale
-- Data: Outubro 2025
-- SGBD: Oracle Database
-- ============================================================================
-- COMMIT inicial para garantir uma transação limpa
COMMIT;

-- ============================================================================
-- BLOCO 1: INSERÇÃO EM TABELAS INDEPENDENTES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Inserção: ANUNCIANTE_DADOS (5 registros)
-- ----------------------------------------------------------------------------
INSERT INTO Anunciante_Dados VALUES (1000001, 'Vodacom Moçambique', 'Telecomunicações', 'Grande', 'Av. 25 de Setembro, Maputo', '+258 84 300 0000', 'Carlos Manjate', 'Campanhas anteriores: Verão 2024, Natal 2023', 'Email e Telefone', 5000000.00, 'AAA - Excelente');
INSERT INTO Anunciante_Dados VALUES (1000002, 'Cervejas de Moçambique', 'Bebidas e Alimentos', 'Grande', 'Zona Industrial, Machava', '+258 21 450 000', 'João Macamo', 'Campanhas: Laurentina 2024, Festivais Verão', 'Email e Presencial', 3000000.00, 'AA - Muito Bom');
INSERT INTO Anunciante_Dados VALUES (1000003, 'BCI - Banco Comercial', 'Serviços Financeiros', 'Grande', 'Av. 25 de Setembro, Centro', '+258 21 352 000', 'Pedro Nhantumbo', 'Campanhas: Crédito Habitação 2024, Poupança Jovem', 'Email', 4000000.00, 'AAA - Excelente');
INSERT INTO Anunciante_Dados VALUES (1000004, 'Tito Moda Boutique', 'Moda e Vestuário', 'Pequeno', 'Shopping Maputo, Loja 45', '+258 84 555 1234', 'Tito Guambe', 'Campanhas: Coleção Verão 2024', 'Redes Sociais', 150000.00, 'B - Regular');
INSERT INTO Anunciante_Dados VALUES (1000005, 'Mozcar Automóveis', 'Automóveis', 'Médio', 'Av. Acordos de Lusaka, Maputo', '+258 21 416 000', 'Rui Matsolo', 'Campanhas: Novos Modelos 2025', 'Email e Presencial', 2000000.00, 'AA - Muito Bom');

-- ----------------------------------------------------------------------------
-- Inserção: AGENCIA_DADOS (5 registros)
-- ----------------------------------------------------------------------------
INSERT INTO Agencia_Dados VALUES (2000001, 'PubliMoz Creative', 'Portfolio: Vodacom, Mcel, BCI', 'Director: Manuel Sitoe', 'Design Gráfico, Marketing Digital, Vídeo', 'Campanhas premiadas: 5 em 2024', 95);
INSERT INTO Agencia_Dados VALUES (2000002, 'AfricAds Agency', 'Portfolio: Cervejas Moz, Shoprite', 'Directora: Isabel Chongo', 'Branding, Social Media, BTL', 'Experiência: 15 anos no mercado', 88);
INSERT INTO Agencia_Dados VALUES (2000003, 'Digital Solutions Moz', 'Portfolio: BCI, LAM, UEM', 'Director: Carlos Tembe', 'Marketing Digital, SEO, Google Ads', 'Especialização em campanhas digitais', 92);
INSERT INTO Agencia_Dados VALUES (2000004, 'Kreativa Studio', 'Portfolio: Tito Moda, Farmácia Moderna', 'Directora: Amina Said', 'Design, Fotografia, Social Media', 'Foco em pequenos negócios', 85);
INSERT INTO Agencia_Dados VALUES (2000005, 'MediaMax Publicidade', 'Portfolio: Mozcar, Shoprite', 'Director: Fernando Macamo', 'TV, Rádio, Outdoor, Digital', 'Campanhas multimedia integradas', 90);

-- ----------------------------------------------------------------------------
-- Inserção: ESPACO_DADOS (5 registros)
-- ----------------------------------------------------------------------------
INSERT INTO Espaco_Dados VALUES (3000001, 'Av. Julius Nyerere - Outdoor', 'Outdoor Billboard', '6m x 3m', 'N/A', 'Alta - Avenida Principal', '06:00-22:00', 45000.00, 'Disponível', 'ClearChannel Moçambique', 'Ocupação histórica: 85% nos últimos 12 meses');
INSERT INTO Espaco_Dados VALUES (3000002, 'Digital - Facebook Ads', 'Rede Social Digital', 'Variável', '1200x628 pixels', 'Alta - 2M usuários', '24/7', 15000.00, 'Sempre Disponível', 'Meta Platforms', 'Campanhas anteriores: 150+ em 2024');
INSERT INTO Espaco_Dados VALUES (3000003, 'Shopping Maputo - Tela LED', 'Tela Digital Indoor', '3m x 2m', '1920x1080 Full HD', 'Muito Alta', '10:00-22:00', 60000.00, 'Disponível', 'Shopping Maputo', 'Taxa ocupação: 95% - espaço premium');
INSERT INTO Espaco_Dados VALUES (3000004, 'Rádio Moçambique - Spot 30s', 'Rádio FM', '30 segundos', 'Audio: 192kbps', 'Nacional', 'Prime Time: 07:00-09:00', 8000.00, 'Disponível', 'Rádio Moçambique', 'Audiência estimada: 500k ouvintes');
INSERT INTO Espaco_Dados VALUES (3000005, 'TVM - Spot Televisivo 30s', 'Televisão', '30 segundos', '1920x1080 HD', 'Nacional', 'Prime Time: 20:00-22:00', 120000.00, 'Disponível', 'TVM', 'Audiência: 1.5M telespectadores');

-- ----------------------------------------------------------------------------
-- Inserção: PUBLICO_ALVO (5 registros)
-- ----------------------------------------------------------------------------
INSERT INTO Publico_Alvo VALUES (4000001, 'Idade: 18-35 anos, Género: Todos, Renda: Média-Alta, Localização: Urbana', 'Usuários de smartphone, early adopters tecnologia, alta conectividade', 'Estilo de vida moderno, valorizam inovação, socialmente ativos', 'Horário nobre redes sociais, eventos urbanos, shopping centers');
INSERT INTO Publico_Alvo VALUES (4000002, 'Idade: 25-45 anos, Género: Masculino predominante, Renda: Média', 'Consumidores de cerveja, frequentam bares e restaurantes', 'Sociáveis, gostam de esportes, vida social ativa', 'Fins de semana, eventos esportivos, horário pós-trabalho');
INSERT INTO Publico_Alvo VALUES (4000003, 'Idade: 30-55 anos, Género: Todos, Renda: Média-Alta, Empregados', 'Planejadores financeiros, buscam estabilidade econômica', 'Conservadores, focados em segurança financeira, família', 'Horário comercial, internet banking, agências físicas');
INSERT INTO Publico_Alvo VALUES (4000004, 'Idade: 18-30 anos, Género: Feminino predominante, Renda: Variável', 'Seguidores de moda, compras online e físicas, influenciados por tendências', 'Fashion-forward, atentos a estilo, presença em redes sociais', 'Shopping centers, Instagram, eventos de moda');
INSERT INTO Publico_Alvo VALUES (4000005, 'Idade: 35-60 anos, Género: Todos, Renda: Alta, Profissionais', 'Compradores de automóveis, valorizam qualidade e status', 'Bem-sucedidos profissionalmente, valorizam marca e conforto', 'Showrooms, feiras automóveis, revistas especializadas');

-- ----------------------------------------------------------------------------
-- Inserção: PROCESSO_DADOS (5 registros originais + 5 novos)
-- ----------------------------------------------------------------------------
INSERT INTO Processo_Dados VALUES (6000001, 'Upload através portal web - Materiais recebidos 01/Set/2024', 'Verificação técnica aprovada: Resolução, formato, duração conformes', 'Análise ética e legal concluída. Sem violações identificadas. Aprovado CNCS.', 'Certificado de conformidade emitido em 05/Set/2024. Válido até 05/Set/2025');
INSERT INTO Processo_Dados VALUES (6000002, 'Submissão via email - Materiais recebidos 10/Set/2024', 'Verificação técnica: Ajustes necessários em qualidade áudio. Reenviado.', 'Conteúdo aprovado. Sem restrições etárias. Adequado para todos públicos.', 'Certificação emitida 15/Set/2024 após correções técnicas');
INSERT INTO Processo_Dados VALUES (6000003, 'FTP upload - Recebido 20/Set/2024, Múltiplos formatos', 'Aprovado: Formatos compatíveis com todos canais de distribuição', 'Revisão legal completa. Disclaimers adicionados conforme regulamento.', 'Certificado emitido 22/Set/2024. Aprovação total');
INSERT INTO Processo_Dados VALUES (6000004, 'Entrega física mídia - Recebido 25/Set/2024', 'Digitalização e verificação em andamento. Prazo: 3 dias úteis', 'Aguardando aprovação legal. Documentação adicional solicitada.', 'Processo em andamento. Certificação pendente');
INSERT INTO Processo_Dados VALUES (6000005, 'Portal web - Submissão 28/Set/2024', 'Verificação técnica concluída: Todos padrões atendidos', 'Aprovação ética instantânea. Conteúdo educacional sem restrições.', 'Certificado emitido automaticamente 28/Set/2024');
-- NOVO: Registros para suportar as Pecas_Interativas
INSERT INTO Processo_Dados VALUES (6000006, 'API Submission - Recebido 01/Out/2025', 'Verificação técnica: OK', 'Análise legal: OK', 'Certificado emitido 01/Out/2025');
INSERT INTO Processo_Dados VALUES (6000007, 'API Submission - Recebido 02/Out/2025', 'Verificação técnica: OK', 'Análise legal: OK', 'Certificado emitido 02/Out/2025');
INSERT INTO Processo_Dados VALUES (6000008, 'API Submission - Recebido 03/Out/2025', 'Verificação técnica: OK', 'Análise legal: OK', 'Certificado emitido 03/Out/2025');
INSERT INTO Processo_Dados VALUES (6000009, 'API Submission - Recebido 04/Out/2025', 'Verificação técnica: OK', 'Análise legal: OK', 'Certificado emitido 04/Out/2025');
INSERT INTO Processo_Dados VALUES (6000010, 'API Submission - Recebido 05/Out/2025', 'Verificação técnica: OK', 'Análise legal: OK', 'Certificado emitido 05/Out/2025');


-- ----------------------------------------------------------------------------
-- Inserção: MODALIDADE_COBRANCA (5 registros)
-- ----------------------------------------------------------------------------
INSERT INTO Modalidade_Cobranca VALUES (9000001, 'Mensal', 'Faturamento todo dia 1 do mês');
INSERT INTO Modalidade_Cobranca VALUES (9000002, 'CPC', 'Faturamento semanal baseado em clicks');
INSERT INTO Modalidade_Cobranca VALUES (9000003, 'Campanha', 'Faturamento único início campanha');
INSERT INTO Modalidade_Cobranca VALUES (9000004, 'Spot', 'Faturamento por transmissão');
INSERT INTO Modalidade_Cobranca VALUES (9000005, 'CPM', 'Faturamento quinzenal por mil impressões');

-- ----------------------------------------------------------------------------
-- Inserção: PROMOCOES (5 registros)
-- ----------------------------------------------------------------------------
INSERT INTO Promocoes VALUES (9100001, 'Premium Anual', 15.00);
INSERT INTO Promocoes VALUES (9100002, 'Pacote Trimestral', 10.00);
INSERT INTO Promocoes VALUES (9100003, 'Volume 10+', 8.50);
INSERT INTO Promocoes VALUES (9100004, 'Pacote Starter', 5.00);
INSERT INTO Promocoes VALUES (9100005, 'Nenhum', 0.00);

-- ----------------------------------------------------------------------------
-- Inserção: PAGAMENTOS (5 registros)
-- ----------------------------------------------------------------------------
INSERT INTO Pagamentos VALUES (5000001, 9000001, 45000.00, 9100001, 'Transferência Bancária', 'Relatório veiculação mensal', 'Conciliado em 30/Set/2024');
INSERT INTO Pagamentos VALUES (5000002, 9000002, 2.50, 9100005, 'Cartão de Crédito', 'Dashboard online tempo real', 'Conciliação automática diária');
INSERT INTO Pagamentos VALUES (5000003, 9000003, 180000.00, 9100002, 'Transferência Bancária', 'Relatório semanal veiculação', 'Conciliado em 05/Out/2024');
INSERT INTO Pagamentos VALUES (5000004, 9000004, 8000.00, 9100003, 'Cheque', 'Certificado transmissão', 'Pendente conciliação');
INSERT INTO Pagamentos VALUES (5000005, 9000005, 15.00, 9100004, 'M-Pesa', 'Relatório impressões online', 'Conciliado em 01/Out/2024');

-- ============================================================================
-- BLOCO 2: TABELAS COM CHAVES ESTRANGEIRAS SIMPLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Inserção: PECAS_CRIATIVAS (5 registros originais + 5 novos)
-- ----------------------------------------------------------------------------
INSERT INTO Pecas_Criativas VALUES (7000001, 'Vodacom 5G Chegou', 'Peça visual anunciando chegada do 5G em Moçambique', 1000001, NULL, 'Agência PubliMoz', TO_DATE('2024-08-15', 'YYYY-MM-DD'), 'Aprovado', 'Direitos exclusivos Vodacom. Uso até Dez/2025', 1, 6000001);
INSERT INTO Pecas_Criativas VALUES (7000002, 'Laurentina Refrescante', 'Campanha verão com foco em momentos sociais', 1000002, NULL, 'Agência AfricAds', TO_DATE('2024-09-01', 'YYYY-MM-DD'), 'Aprovado', 'Cervejas de Moçambique. Renovável anualmente', 2, 6000002);
INSERT INTO Pecas_Criativas VALUES (7000003, 'BCI Crédito Habitação', 'Spot televisivo sobre crédito habitação facilitado', 1000003, NULL, 'Digital Solutions', TO_DATE('2024-09-10', 'YYYY-MM-DD'), 'Aprovado', 'BCI. Direitos perpétuos para uso institucional', 1, 6000003);
INSERT INTO Pecas_Criativas VALUES (7000004, 'Tito Moda Primavera', 'Lookbook digital coleção primavera/verão', 1000004, NULL, 'Kreativa Studio', TO_DATE('2024-09-20', 'YYYY-MM-DD'), 'Em Revisão', 'Tito Moda. Uso exclusivo redes sociais 2024/2025', 1, 6000004);
INSERT INTO Pecas_Criativas VALUES (7000005, 'Mozcar Novos Modelos', 'Vídeo showcasing novos modelos 2025', 1000005, NULL, 'MediaMax', TO_DATE('2024-09-25', 'YYYY-MM-DD'), 'Aprovado', 'Mozcar Automóveis. Licença 12 meses', 1, 6000005);
-- NOVO: Registros para suportar as Pecas_Interativas
INSERT INTO Pecas_Criativas VALUES (7000006, 'Quiz Interativo BCI', 'Quiz sobre literacia financeira', 1000003, NULL, 'Digital Solutions', TO_DATE('2025-10-01', 'YYYY-MM-DD'), 'Aprovado', 'Direitos do BCI', 0, 6000006);
INSERT INTO Pecas_Criativas VALUES (7000007, 'Filtro Instagram CDM', 'Filtro para stories do Instagram', 1000002, NULL, 'AfricAds Agency', TO_DATE('2025-10-02', 'YYYY-MM-DD'), 'Aprovado', 'Direitos da CDM', 0, 6000007);
INSERT INTO Pecas_Criativas VALUES (7000008, 'Configurador de Carro Mozcar', 'Ferramenta web para configurar carros', 1000005, NULL, 'MediaMax', TO_DATE('2025-10-03', 'YYYY-MM-DD'), 'Aprovado', 'Direitos da Mozcar', 0, 6000008);
INSERT INTO Pecas_Criativas VALUES (7000009, 'Jogo "Velocidade 5G"', 'Mini-jogo mobile para promover 5G', 1000001, NULL, 'PubliMoz Creative', TO_DATE('2025-10-04', 'YYYY-MM-DD'), 'Em Revisão', 'Direitos da Vodacom', 0, 6000009);
INSERT INTO Pecas_Criativas VALUES (7000010, 'Votação de Look Tito Moda', 'Enquete interativa nas redes sociais', 1000004, NULL, 'Kreativa Studio', TO_DATE('2025-10-05', 'YYYY-MM-DD'), 'Aprovado', 'Direitos da Tito Moda', 0, 6000010);

-- ----------------------------------------------------------------------------
-- Inserção: CAMPANHA_DADOS (5 registros)
-- ----------------------------------------------------------------------------
INSERT INTO Campanha_Dados VALUES (8000001, 1000001, 'Campanha 5G Revolution', 'Posicionar Vodacom como líder em tecnologia 5G em Moçambique', 'Jovens urbanos, early adopters, 18-35 anos', 500000.00, TO_DATE('2024-10-01', 'YYYY-MM-DD'), TO_DATE('2024-12-31', 'YYYY-MM-DD'), 'Vídeos, banners digitais, outdoor, spots rádio', 'Impressões, Reach, Engajamento, Conversões', 'Resultados parciais: 2M impressões, 150k engajamentos, 5k novos contratos', 6000001, 7000001, 5000001);
INSERT INTO Campanha_Dados VALUES (8000002, 1000002, 'Verão Laurentina 2024', 'Aumentar vendas período verão e fortalecer associação marca com momentos sociais', 'Homens 25-45 anos, consumidores cerveja', 300000.00, TO_DATE('2024-11-01', 'YYYY-MM-DD'), TO_DATE('2025-02-28', 'YYYY-MM-DD'), 'TV, rádio, ativações BTL, redes sociais', 'Vendas, Brand Awareness, Participação eventos', 'Início previsto Nov/2024. Metas: +20% vendas vs ano anterior', 6000002, 7000002, 5000003);
INSERT INTO Campanha_Dados VALUES (8000003, 1000003, 'Casa Própria BCI', 'Promover crédito habitação com taxas especiais e processo simplificado', 'Profissionais 30-55 anos, classe média-alta', 400000.00, TO_DATE('2024-10-15', 'YYYY-MM-DD'), TO_DATE('2025-03-31', 'YYYY-MM-DD'), 'TV, rádio, digital, agências BCI', 'Solicitações crédito, Aprovações, Brand perception', 'Meta: 500 aprovações crédito. Campanha em andamento', 6000003, 7000003, 5000003);
INSERT INTO Campanha_Dados VALUES (8000004, 1000004, 'Primavera Tito Fashion', 'Lançar coleção primavera e aumentar seguidores Instagram', 'Mulheres 18-30 anos, fashion lovers', 50000.00, TO_DATE('2024-10-20', 'YYYY-MM-DD'), TO_DATE('2024-12-20', 'YYYY-MM-DD'), 'Instagram, Facebook, TikTok, influencers', 'Seguidores, Vendas online, Tráfego loja física', 'Planejamento em fase final. Lançamento Out/2024', 6000004, 7000004, 5000004);
INSERT INTO Campanha_Dados VALUES (8000005, 1000005, 'Mozcar Drive 2025', 'Apresentar novos modelos e gerar test drives', 'Profissionais 35-60 anos, compradores potenciais', 250000.00, TO_DATE('2024-11-01', 'YYYY-MM-DD'), TO_DATE('2025-01-31', 'YYYY-MM-DD'), 'TV, outdoor, digital, eventos showroom', 'Test drives agendados, Leads qualificados, Vendas', 'Pré-lançamento. Meta: 200 test drives, 50 vendas', 6000005, 7000005, 5000005);

-- ----------------------------------------------------------------------------
-- NOVO BLOCO: ATUALIZAÇÃO DE CHAVES ESTRANGEIRAS
-- Descrição: Atualiza a coluna Cod_camp na tabela Pecas_Criativas agora que
-- as campanhas já foram inseridas, completando a integridade dos dados.
-- ----------------------------------------------------------------------------
UPDATE Pecas_Criativas SET Cod_camp = 8000001 WHERE Id_unicoPeca = 7000001;
UPDATE Pecas_Criativas SET Cod_camp = 8000002 WHERE Id_unicoPeca = 7000002;
UPDATE Pecas_Criativas SET Cod_camp = 8000003 WHERE Id_unicoPeca = 7000003;
UPDATE Pecas_Criativas SET Cod_camp = 8000004 WHERE Id_unicoPeca = 7000004;
UPDATE Pecas_Criativas SET Cod_camp = 8000005 WHERE Id_unicoPeca = 7000005;

-- ----------------------------------------------------------------------------
-- Inserção: AGENCIA_ESPECIALIDADE (5 registros)
-- ----------------------------------------------------------------------------
INSERT INTO Agencia_Especialidade VALUES (2000001, 'Design Gráfico');
INSERT INTO Agencia_Especialidade VALUES (2000001, 'Marketing Digital');
INSERT INTO Agencia_Especialidade VALUES (2000002, 'Branding Estratégico');
INSERT INTO Agencia_Especialidade VALUES (2000003, 'SEO e SEM');
INSERT INTO Agencia_Especialidade VALUES (2000004, 'Social Media Management');

-- ----------------------------------------------------------------------------
-- Inserção: AGENCIA_CERTIFICACOES (5 registros)
-- ----------------------------------------------------------------------------
INSERT INTO Agencia_Certificacoes VALUES (2000001, 'Google Partner Certified');
INSERT INTO Agencia_Certificacoes VALUES (2000002, 'ISO 9001:2015');
INSERT INTO Agencia_Certificacoes VALUES (2000003, 'Facebook Blueprint Certified');
INSERT INTO Agencia_Certificacoes VALUES (2000004, 'Adobe Certified Professional');
INSERT INTO Agencia_Certificacoes VALUES (2000005, 'HubSpot Certified Agency');

-- ----------------------------------------------------------------------------
-- Inserção: APROVACAO_NIVEL (5 registros)
-- ----------------------------------------------------------------------------
INSERT INTO Aprovacao_Nivel VALUES (6000001, 'Nível 3: Aprovação Diretoria - Aprovado em 05/Set/2024');
INSERT INTO Aprovacao_Nivel VALUES (6000002, 'Nível 2: Aprovação Gerência - Aprovado com ressalvas');
INSERT INTO Aprovacao_Nivel VALUES (6000003, 'Nível 3: Aprovação Diretoria e Jurídico - Aprovado');
INSERT INTO Aprovacao_Nivel VALUES (6000004, 'Nível 1: Aprovação Coordenação - Em análise');
INSERT INTO Aprovacao_Nivel VALUES (6000005, 'Nível 2: Aprovação Automática - Sistema aprovado');

-- ----------------------------------------------------------------------------
-- Inserção: PROCESSO_REVISAO (5 registros)
-- ----------------------------------------------------------------------------
INSERT INTO Processo_Revisao VALUES (6000001, 'Ciclo único - Sem revisões', 'Nenhuma alteração necessária');
INSERT INTO Processo_Revisao VALUES (6000002, 'Ciclo 2 revisões', 'Rev1: Ajuste áudio. Rev2: Aprovado');
INSERT INTO Processo_Revisao VALUES (6000003, 'Ciclo único', 'Adicionados disclaimers legais');
INSERT INTO Processo_Revisao VALUES (6000004, 'Em andamento', 'Aguardando documentação adicional');
INSERT INTO Processo_Revisao VALUES (6000005, 'Aprovação automática', 'Sem necessidade revisão manual');

-- ============================================================================
-- BLOCO 3: TABELAS DE ESPECIALIZAÇÃO (PEÇAS CRIATIVAS)
-- Nota: A soma dos registros nas tabelas de especialização deve ser igual ao
-- número de peças que pertencem a esses tipos. Não é obrigatório que cada
-- tabela de especialização tenha 5 registros, mas sim que todas tenham dados.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Inserção: PECAS_VISUAIS (3 registros)
-- ----------------------------------------------------------------------------
INSERT INTO Pecas_Visuais VALUES (7000001, '1920x1080', '1920x1080', 'PNG', 'Vermelho Vodacom, Branco, Preto', 'Logo 5G, ícones velocidade, gradientes modernos', 'Desktop, Mobile, Tablets, Outdoor Digital');
INSERT INTO Pecas_Visuais VALUES (7000003, '1920x1080', '1920x1080', 'JPG', 'Azul BCI, Branco, Dourado', 'Imagens família, casa, logo BCI', 'TV Full HD, Digital Screens, Web');
INSERT INTO Pecas_Visuais VALUES (7000004, '1080x1350', '1080x1350', 'PNG', 'Pastéis, Rosa, Azul claro, Branco', 'Fotos lookbook, textos fashion, logo Tito Moda', 'Instagram Feed, Stories, Reels');

-- ----------------------------------------------------------------------------
-- Inserção: PECAS_AUDIOVISUAIS (2 registros)
-- ----------------------------------------------------------------------------
INSERT INTO Pecas_Audiovisuais VALUES (7000002, '30s', 'Full HD', '1920x1080', 'Português', 'Formato MP4 H.264, compatível TV digital, YouTube, Facebook');
INSERT INTO Pecas_Audiovisuais VALUES (7000005, '45s', '4K', '3840x2160', 'Português, Legendas inglês disponíveis', 'Formato MP4 H.265, TV 4K, YouTube 4K, Cinema digital');

-- ----------------------------------------------------------------------------
-- NOVO: Inserção: PECAS_INTERATIVAS (5 registros)
-- Descrição: Adicionados 5 registros para cumprir o requisito de que todas
-- as tabelas devem conter dados.
-- ----------------------------------------------------------------------------
INSERT INTO Pecas_Interativas VALUES (7000006, 'HTML5, JavaScript', 'Alto', 'Navegador Web Moderno', 85.50, 'Coleta de leads (nome, email)');
INSERT INTO Pecas_Interativas VALUES (7000007, 'Spark AR', 'Médio', 'Instagram App', 92.00, 'Contagem de usos do filtro');
INSERT INTO Pecas_Interativas VALUES (7000008, 'WebGL, Three.js', 'Muito Alto', 'Navegador com aceleração gráfica', 95.20, 'Modelos de carro mais configurados');
INSERT INTO Pecas_Interativas VALUES (7000009, 'Unity Engine', 'Alto', 'Android, iOS', 88.75, 'Pontuação, tempo de jogo');
INSERT INTO Pecas_Interativas VALUES (7000010, 'Instagram/Facebook API', 'Baixo', 'App de Rede Social', 78.90, 'Contagem de votos por opção');


-- ============================================================================
-- BLOCO 4: TABELAS DE RELACIONAMENTO N:M
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Inserção: ANUNCIANTE_AGENCIA (5 relacionamentos)
-- ----------------------------------------------------------------------------
INSERT INTO Anunciante_Agencia VALUES (1000001, 2000001);
INSERT INTO Anunciante_Agencia VALUES (1000002, 2000002);
INSERT INTO Anunciante_Agencia VALUES (1000003, 2000003);
INSERT INTO Anunciante_Agencia VALUES (1000004, 2000004);
INSERT INTO Anunciante_Agencia VALUES (1000005, 2000005);

-- ----------------------------------------------------------------------------
-- Inserção: CAMPANHA_ESPACO (10 relacionamentos)
-- ----------------------------------------------------------------------------
INSERT INTO Campanha_Espaco VALUES (8000001, 3000001);
INSERT INTO Campanha_Espaco VALUES (8000001, 3000002);
INSERT INTO Campanha_Espaco VALUES (8000002, 3000004);
INSERT INTO Campanha_Espaco VALUES (8000002, 3000005);
INSERT INTO Campanha_Espaco VALUES (8000003, 3000005);
INSERT INTO Campanha_Espaco VALUES (8000003, 3000004);
INSERT INTO Campanha_Espaco VALUES (8000004, 3000002);
INSERT INTO Campanha_Espaco VALUES (8000005, 3000001);
INSERT INTO Campanha_Espaco VALUES (8000005, 3000005);
INSERT INTO Campanha_Espaco VALUES (8000005, 3000003);

-- ----------------------------------------------------------------------------
-- Inserção: CAMPANHA_PUBLICOALVO (5 relacionamentos)
-- ----------------------------------------------------------------------------
INSERT INTO Campanha_PublicoAlvo VALUES (8000001, 4000001);
INSERT INTO Campanha_PublicoAlvo VALUES (8000002, 4000002);
INSERT INTO Campanha_PublicoAlvo VALUES (8000003, 4000003);
INSERT INTO Campanha_PublicoAlvo VALUES (8000004, 4000004);
INSERT INTO Campanha_PublicoAlvo VALUES (8000005, 4000005);

-- ----------------------------------------------------------------------------
-- Inserção: CAMPANHA_CANAL (8 registros)
-- ----------------------------------------------------------------------------
INSERT INTO Campanha_Canal VALUES (8000001, 'Facebook Ads');
INSERT INTO Campanha_Canal VALUES (8000001, 'Outdoor Digital');
INSERT INTO Campanha_Canal VALUES (8000002, 'Televisão');
INSERT INTO Campanha_Canal VALUES (8000002, 'Rádio');
INSERT INTO Campanha_Canal VALUES (8000003, 'Televisão');
INSERT INTO Campanha_Canal VALUES (8000004, 'Instagram');
INSERT INTO Campanha_Canal VALUES (8000005, 'Outdoor');
INSERT INTO Campanha_Canal VALUES (8000005, 'Televisão');

-- ----------------------------------------------------------------------------
-- Inserção: ESPACO_PECA (8 relacionamentos)
-- ----------------------------------------------------------------------------
INSERT INTO Espaco_Peca VALUES (3000001, 7000001);
INSERT INTO Espaco_Peca VALUES (3000002, 7000001);
INSERT INTO Espaco_Peca VALUES (3000004, 7000002);
INSERT INTO Espaco_Peca VALUES (3000005, 7000002);
INSERT INTO Espaco_Peca VALUES (3000005, 7000003);
INSERT INTO Espaco_Peca VALUES (3000002, 7000004);
INSERT INTO Espaco_Peca VALUES (3000001, 7000005);
INSERT INTO Espaco_Peca VALUES (3000005, 7000005);

-- ============================================================================
-- COMMIT E VERIFICAÇÕES
-- ============================================================================

COMMIT;

-- CORREÇÃO: Query de verificação atualizada para incluir a tabela Pecas_Interativas.
SELECT 'Anunciante_Dados' AS Tabela, COUNT(*) AS Total FROM Anunciante_Dados
UNION ALL
SELECT 'Agencia_Dados', COUNT(*) FROM Agencia_Dados
UNION ALL
SELECT 'Agencia_Certificacoes', COUNT(*) FROM Agencia_Certificacoes
UNION ALL
SELECT 'Agencia_Especialidade', COUNT(*) FROM Agencia_Especialidade
UNION ALL
SELECT 'Anunciante_Agencia', COUNT(*) FROM Anunciante_Agencia
UNION ALL
SELECT 'Aprovacao_Nivel', COUNT(*) FROM Aprovacao_Nivel
UNION ALL
SELECT 'Campanha_Canal', COUNT(*) FROM Campanha_Canal
UNION ALL
SELECT 'Campanha_Dados', COUNT(*) FROM Campanha_Dados
UNION ALL
SELECT 'Campanha_Espaco', COUNT(*) FROM Campanha_Espaco
UNION ALL
SELECT 'Campanha_PublicoAlvo', COUNT(*) FROM Campanha_PublicoAlvo
UNION ALL
SELECT 'Espaco_Dados', COUNT(*) FROM Espaco_Dados
UNION ALL
SELECT 'Espaco_Peca', COUNT(*) FROM Espaco_Peca
UNION ALL
SELECT 'Modalidade_Cobranca', COUNT(*) FROM Modalidade_Cobranca
UNION ALL
SELECT 'Pagamentos', COUNT(*) FROM Pagamentos
UNION ALL
SELECT 'Pecas_Audiovisuais', COUNT(*) FROM Pecas_Audiovisuais
UNION ALL
SELECT 'Pecas_Criativas', COUNT(*) FROM Pecas_Criativas
UNION ALL
SELECT 'Pecas_Interativas', COUNT(*) FROM Pecas_Interativas -- ADICIONADO
UNION ALL
SELECT 'Pecas_Visuais', COUNT(*) FROM Pecas_Visuais
UNION ALL
SELECT 'Processo_Dados', COUNT(*) FROM Processo_Dados
UNION ALL
SELECT 'Processo_Revisao', COUNT(*) FROM Processo_Revisao
UNION ALL
SELECT 'Promocoes', COUNT(*) FROM Promocoes
UNION ALL
SELECT 'Publico_Alvo', COUNT(*) FROM Publico_Alvo
ORDER BY 1;

SELECT 'Script de inserção executado com sucesso' AS Status FROM DUAL;