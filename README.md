# Câmara Analytics — Evidence

Camada de visualização para o projeto ETL Câmara dos Deputados.

## O que já está preparado

- Visão Geral com KPIs, evolução mensal e destaques automáticos;
- página de Despesas com filtros por legislatura, ano, partido e UF;
- página de Votações com participação, composição dos votos e tipos de proposição;
- página de Deputados com ranking de gastos, atividade e busca;
- página Sobre os dados com regras de interpretação;
- conexão DuckDB em `sources/camara_db/connection.yaml`.

## 1. Adicionar o banco gerado pelo ETL

Copie o DuckDB produzido pelo ETL para:

```text
sources/camara_db/camara.duckdb
```

O arquivo esperado é o mesmo configurado no ETL por `CAMARA_DB_PATH` (por padrão `data/output/camara.duckdb`).

## 2. Instalar dependências

```bash
npm install
```

## 3. Atualizar as fontes do Evidence

```bash
npm run sources
```

## 4. Executar localmente

```bash
npm run dev
```

## Estrutura das consultas de origem

```text
sources/camara_db/
├── connection.yaml
├── atualizacao.sql
├── deputados.sql
├── despesas_mensais.sql
├── legislaturas.sql
├── votos.sql
└── votos_proposicoes.sql
```

A consulta `votos.sql` parte de `dw.fact_voto_deputado` para manter uma linha por voto parlamentar e não sofrer multiplicação pelo relacionamento votação × proposição.

## Próximo refinamento recomendado

Após inserir o DuckDB real, rode `npm run sources` e revise os resultados visuais. A partir dos volumes reais, vale ajustar limites, formatos, categorias e criar páginas detalhadas por deputado usando páginas parametrizadas.
