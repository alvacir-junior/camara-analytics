---
title: Visão Geral
---

# 🏛️ Câmara Analytics

Visão executiva dos dados modelados pelo ETL da Câmara dos Deputados. Use o filtro para navegar entre legislaturas.

```sql legislaturas
select
    cast(id_legislatura as varchar) as id_legislatura,
    'Legislatura ' || cast(id_legislatura as varchar) as legislatura
from camara_db.legislaturas
order by id_legislatura desc
```

<Dropdown name=legislatura data={legislaturas} value=id_legislatura label=legislatura title="Legislatura" defaultValue="%">
    <DropdownOption value="%" valueLabel="Todas"/>
</Dropdown>

```sql kpis
with dep as (
    select *
    from camara_db.deputados
    where cast(id_legislatura as varchar) like '${inputs.legislatura.value}'
),
desp as (
    select *
    from camara_db.despesas_mensais
    where cast(id_legislatura as varchar) like '${inputs.legislatura.value}'
),
votos as (
    select *
    from camara_db.votos
    where cast(id_legislatura as varchar) like '${inputs.legislatura.value}'
)
select
    (select count(distinct id_deputado) from dep) as deputados,
    (select count(distinct id_deputado) from dep where em_exercicio = true) as em_exercicio,
    (select coalesce(sum(valor_liquido),0) from desp) as total_gasto,
    (select coalesce(sum(quantidade_despesas),0) from desp) as documentos,
    (select count(*) from votos) as votos_registrados,
    (select count(distinct id_votacao) from votos) as votacoes
```

<BigValue data={kpis} value=deputados title="Deputados distintos"/>
<BigValue data={kpis} value=em_exercicio title="Em exercício na última fotografia"/>
<BigValue data={kpis} value=total_gasto title="Despesas líquidas (R$)" fmt='#,##0'/>
<BigValue data={kpis} value=votos_registrados title="Votos registrados" fmt='#,##0'/>
<BigValue data={kpis} value=votacoes title="Votações distintas" fmt='#,##0'/>

## 🏆 Deputados mais econômicos — Legislatura atual

Ranking dos deputados atualmente em exercício com menor volume de despesas
acumuladas na legislatura atual.

```sql top_economicos
select
    id_deputado,
    deputado,
    quantidade_despesas,
    total_gasto
from camara_db.deputados
where em_exercicio = true
  and id_legislatura = (
      select max(id_legislatura)
      from camara_db.deputados
  )
  and quantidade_despesas > 0
  and total_gasto > 0
order by total_gasto asc
limit 20;
```

<BarChart
    data={top_economicos}
    x=deputado
    y=total_gasto
    yFmt='#,##0.00'
    swapXY=true
    sort=false
    title="Top 20 deputados com menores despesas"
    emptySet=warn
/>

<DataTable data={top_economicos}>
    <Column id=deputado title="Deputado"/>
    <Column id=quantidade_despesas title="Registros de despesas" fmt='#,##0'/>
    <Column id=total_gasto title="Despesa acumulada (R$)" fmt='#,##0.00'/>
</DataTable>

> **Critério:** considera somente deputados da legislatura mais recente com `em_exercicio = true`. O ranking utiliza o valor total líquido de despesas acumuladas.

## ⭐ Atividade parlamentar e economicidade

Os indicadores comparam os deputados atualmente em exercício na legislatura atual.

- **Atividade:** posição relativa pela quantidade de votos registrados.
- **Economicidade:** posição relativa pelo menor volume de despesas.
- **70 pontos:** corte mínimo para participação no ranking de eficiência.

```sql indice_deputados
with base as (
    select
        id_deputado,
        deputado,
        id_legislatura,
        quantidade_votos,
        coalesce(total_gasto, 0) as total_gasto,

        percent_rank() over (
            order by quantidade_votos
        ) * 100 as atividade_votacoes,

        (
            1 - percent_rank() over (
                order by coalesce(total_gasto, 0)
            )
        ) * 100 as economicidade

    from camara_db.deputados

    where em_exercicio = true
      and id_legislatura = (
          select max(id_legislatura)
          from camara_db.deputados
      )
)

select
    id_deputado,
    deputado,
    quantidade_votos,
    total_gasto,
    round(atividade_votacoes, 1) as atividade_votacoes,
    round(economicidade, 1) as economicidade
from base
order by deputado
```

<DataTable data={indice_deputados}>
    <Column id=deputado title="Deputado"/>
    <Column id=quantidade_votos title="Votos registrados" fmt='#,##0'/>
    <Column id=total_gasto title="Despesas (R$)" fmt='#,##0.00'/>
    <Column id=atividade_votacoes title="Atividade" fmt='#,##0.0'/>
    <Column id=economicidade title="Economicidade" fmt='#,##0.0'/>
</DataTable>


## ⭐ Atividade parlamentar e economicidade

Os indicadores comparam os deputados atualmente em exercício na legislatura atual.

- **Atividade:** posição relativa pela quantidade de votos registrados.
- **Economicidade:** posição relativa pelo menor volume de despesas.
- **70 pontos:** corte mínimo para participação no ranking de eficiência.

```sql indice_deputados
with base as (
    select
        id_deputado,
        deputado,
        id_legislatura,
        quantidade_votos,
        coalesce(total_gasto, 0) as total_gasto,

        percent_rank() over (
            order by quantidade_votos
        ) * 100 as atividade_votacoes,

        (
            1 - percent_rank() over (
                order by coalesce(total_gasto, 0)
            )
        ) * 100 as economicidade

    from camara_db.deputados

    where em_exercicio = true
      and id_legislatura = (
          select max(id_legislatura)
          from camara_db.deputados
      )
)

select
    id_deputado,
    deputado,
    quantidade_votos,
    total_gasto,
    round(atividade_votacoes, 1) as atividade_votacoes,
    round(economicidade, 1) as economicidade
from base
order by deputado
```

<DataTable data={indice_deputados}>
    <Column id=deputado title="Deputado"/>
    <Column id=quantidade_votos title="Votos registrados" fmt='#,##0'/>
    <Column id=total_gasto title="Despesas (R$)" fmt='#,##0.00'/>
    <Column id=atividade_votacoes title="Atividade" fmt='#,##0.0'/>
    <Column id=economicidade title="Economicidade" fmt='#,##0.0'/>
</DataTable>


## 🏆 Ranking — Alta atividade e economicidade

O ranking considera somente deputados com **atividade ≥ 70** e
**economicidade ≥ 70**.

Entre os deputados elegíveis, a pontuação combina:

- **60% Economicidade**
- **40% Atividade em votações**

```sql ranking_eficiencia
with elegiveis as (
    select
        id_deputado,
        deputado,
        quantidade_votos,
        total_gasto,
        atividade_votacoes,
        economicidade,

        round(
            economicidade * 0.60 +
            atividade_votacoes * 0.40,
            1
        ) as score_eficiencia

    from ${indice_deputados}

    where atividade_votacoes >= 70
      and economicidade >= 70
),

ranking as (
    select
        row_number() over (
            order by
                score_eficiencia desc,
                economicidade desc,
                atividade_votacoes desc
        ) as ranking,

        id_deputado,
        deputado,
        quantidade_votos,
        total_gasto,
        atividade_votacoes,
        economicidade,
        score_eficiencia

    from elegiveis
)

select *
from ranking
where ranking <= 20
order by ranking
```

<DataTable
    data={ranking_eficiencia}
    sort="ranking asc"
>
    <Column id=ranking title="Posição"/>
    <Column id=deputado title="Deputado"/>
    <Column id=score_eficiencia title="Score" fmt='#,##0.0'/>
    <Column id=economicidade title="Economicidade" fmt='#,##0.0'/>
    <Column id=atividade_votacoes title="Atividade" fmt='#,##0.0'/>
    <Column id=quantidade_votos title="Votos registrados" fmt='#,##0'/>
    <Column id=total_gasto title="Despesas (R$)" fmt='#,##0.00'/>
</DataTable>

> **Metodologia:** o ranking considera apenas deputados atualmente em exercício
> na legislatura mais recente que atingem pelo menos 70 pontos tanto em
> atividade em votações quanto em economicidade. O score é uma métrica
> definida para este projeto, com peso de 60% para economicidade e 40%
> para atividade.


## Evolução das despesas

```sql despesas_tempo
select
    competencia,
    sum(valor_liquido) as valor_liquido
from camara_db.despesas_mensais
where cast(id_legislatura as varchar) like '${inputs.legislatura.value}'
group by competencia
order by competencia
```

<LineChart
    data={despesas_tempo}
    x=competencia
    y=valor_liquido
    yFmt='#,##0'
    title="Despesa líquida por mês"
    emptySet=warn
/>

## Principais destaques

```sql top_deputados
select
    deputado,
    sum(valor_liquido) as total_gasto
from camara_db.despesas_mensais
where cast(id_legislatura as varchar) like '${inputs.legislatura.value}'
group by deputado
order by total_gasto desc
limit 10
```

```sql top_categoria
select
    categoria_analitica,
    sum(valor_liquido) as total_gasto
from camara_db.despesas_mensais
where cast(id_legislatura as varchar) like '${inputs.legislatura.value}'
group by categoria_analitica
order by total_gasto desc
limit 1
```

```sql composicao_votos
select
    upper(coalesce(tipo_voto,'N/D')) as tipo_voto,
    count(*) as quantidade
from camara_db.votos
where cast(id_legislatura as varchar) like '${inputs.legislatura.value}'
group by tipo_voto
order by quantidade desc
```

{#if top_deputados.length > 0}
<p>O maior volume de despesas no recorte é de <strong><Value data={top_deputados} column=deputado/></strong>, com <strong>R$ <Value data={top_deputados} column=total_gasto fmt='#,##0.00'/></strong>.</p>
{/if}

{#if top_categoria.length > 0}
<p>A categoria com maior valor líquido é <strong><Value data={top_categoria} column=categoria_analitica/></strong>, totalizando <strong>R$ <Value data={top_categoria} column=total_gasto fmt='#,##0.00'/></strong>.</p>
{/if}

<BarChart
    data={top_deputados}
    x=deputado
    y=total_gasto
    yFmt='#,##0'
    swapXY=true
    title="Top 10 deputados por despesas"
    emptySet=warn
/>

<BarChart
    data={composicao_votos}
    x=tipo_voto
    y=quantidade
    title="Composição dos votos registrados"
    emptySet=warn
/>

## Atualização da base

```sql atualizacao
select * from camara_db.atualizacao
```

<DataTable data={atualizacao}>
    <Column id=ultima_despesa title="Última despesa"/>
    <Column id=ultimo_voto title="Último voto"/>
    <Column id=referencia_exercicio title="Referência exercício"/>
    <Column id=linhas_despesas title="Linhas de despesas" fmt='#,##0'/>
    <Column id=linhas_votos title="Linhas de votos" fmt='#,##0'/>
</DataTable>

> **Nota:** `em_exercicio` representa a fotografia mais recente da composição parlamentar. Não deve ser interpretado como a situação histórica do deputado na data de cada despesa.
