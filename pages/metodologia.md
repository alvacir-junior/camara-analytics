---
title: Sobre os dados
---

# ℹ️ Sobre os dados

## Modelo analítico

O projeto de dados está organizado em camadas **RAW → DS → DW → DM**. O Evidence consome principalmente os Data Marts e, quando necessário, fatos e dimensões do DW para evitar duplicidades de grão.

### Data Marts usados

- `dm.resumo_legislaturas`: composição e período das legislaturas;
- `dm.despesas_mensais`: despesas mensais por deputado, partido, UF e tipo;
- `dm.deputado_resumo`: indicadores consolidados por deputado e legislatura;
- `dm.votos_por_tipo_proposicao`: atividade de votação por tipo de proposição.

Para o painel de votações, a consulta de origem parte diretamente de `dw.fact_voto_deputado`, evitando que o relacionamento N:N entre votação e proposição multiplique votos no total geral.

## Cuidados de interpretação

### Deputado em exercício

`em_exercicio` é uma **fotografia da última atualização disponível**. Esse campo responde quem está em exercício agora na composição observada, mas não reconstrói a situação do parlamentar na data histórica de cada despesa ou votação.

### Quantidade de deputados

O total de pessoas que participaram de uma legislatura pode ser maior do que o número de cadeiras simultâneas, devido a suplências, licenças, renúncias e substituições.

### Despesas negativas

Valores líquidos negativos podem existir por ajustes, estornos, restituições ou lançamentos compensatórios. O ETL sinaliza esses casos para revisão, mas não os elimina automaticamente.

## Conexão do DuckDB

O arquivo final do ETL deve ser copiado para:

`/sources/camara_db/camara.duckdb`

Depois execute:

```bash
npm run sources
npm run dev
```

O `connection.yaml` já está preparado para usar esse arquivo local.
