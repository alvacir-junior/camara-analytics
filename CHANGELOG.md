# Changelog — Câmara Analytics

## Primeira versão analítica

- substituída a consulta de exemplo antiga por fontes compatíveis com o ETL Câmara v0.6.6;
- adicionadas páginas de Visão Geral, Despesas, Votações e Deputados;
- adicionada página de metodologia e cuidados de interpretação;
- adicionados filtros por legislatura, ano, partido e UF onde o grão permite;
- adicionados KPIs, séries temporais, rankings, tabelas pesquisáveis e destaques dinâmicos;
- consultas de votos passaram a usar `dw.fact_voto_deputado` no total geral para evitar multiplicação pelo relacionamento N:N com proposições;
- mantido `sources/camara_db/camara.duckdb` como placeholder vazio, a ser substituído pelo banco produzido pelo ETL;
- removidos ambiente virtual, scripts locais e caches gerados que não são necessários para distribuir o projeto Evidence.
