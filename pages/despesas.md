---
title: Despesas
---

# 💳 Despesas parlamentares

Análise das despesas por período, partido, UF, categoria e deputado.

```sql legislaturas
select distinct cast(id_legislatura as varchar) as id_legislatura
from camara_db.despesas_mensais
order by id_legislatura desc
```

```sql anos
select distinct cast(ano as varchar) as ano
from camara_db.despesas_mensais
order by ano desc
```

```sql partidos
select distinct sigla_partido
from camara_db.despesas_mensais
order by sigla_partido
```

```sql ufs
select distinct sigla_uf
from camara_db.despesas_mensais
order by sigla_uf
```

<Dropdown name=legislatura data={legislaturas} value=id_legislatura title="Legislatura" defaultValue="%">
    <DropdownOption value="%" valueLabel="Todas"/>
</Dropdown>

<Dropdown name=ano data={anos} value=ano title="Ano" defaultValue="%">
    <DropdownOption value="%" valueLabel="Todos"/>
</Dropdown>

<Dropdown name=partido data={partidos} value=sigla_partido title="Partido" defaultValue="%">
    <DropdownOption value="%" valueLabel="Todos"/>
</Dropdown>

<Dropdown name=uf data={ufs} value=sigla_uf title="UF" defaultValue="%">
    <DropdownOption value="%" valueLabel="Todas"/>
</Dropdown>

```sql base
select *
from camara_db.despesas_mensais
where cast(id_legislatura as varchar) like '${inputs.legislatura.value}'
  and cast(ano as varchar) like '${inputs.ano.value}'
  and sigla_partido like '${inputs.partido.value}'
  and sigla_uf like '${inputs.uf.value}'
```

```sql kpis
select
    coalesce(sum(valor_liquido),0) as total_liquido,
    coalesce(sum(valor_glosa),0) as total_glosa,
    coalesce(sum(quantidade_despesas),0) as documentos,
    case when sum(quantidade_despesas) = 0 then 0
         else sum(valor_liquido) / sum(quantidade_despesas) end as ticket_medio,
    count(distinct id_deputado) as deputados
from ${base}
```

<BigValue data={kpis} value=total_liquido title="Valor líquido (R$)" fmt='#,##0.00'/>
<BigValue data={kpis} value=total_glosa title="Glosas (R$)" fmt='#,##0.00'/>
<BigValue data={kpis} value=documentos title="Documentos" fmt='#,##0'/>
<BigValue data={kpis} value=ticket_medio title="Valor médio por documento (R$)" fmt='#,##0.00'/>
<BigValue data={kpis} value=deputados title="Deputados no recorte" fmt='#,##0'/>

```sql insight_deputado
select deputado, sum(valor_liquido) as total_gasto
from ${base}
group by deputado
order by total_gasto desc
limit 1
```

```sql insight_categoria
select categoria_analitica, sum(valor_liquido) as total_gasto
from ${base}
group by categoria_analitica
order by total_gasto desc
limit 1
```

{#if insight_deputado.length > 0}
<p><strong>Destaque do recorte:</strong> <Value data={insight_deputado} column=deputado/> concentra o maior valor líquido, com <strong>R$ <Value data={insight_deputado} column=total_gasto fmt='#,##0.00'/></strong>.</p>
{/if}

{#if insight_categoria.length > 0}
<p>A categoria de maior peso é <strong><Value data={insight_categoria} column=categoria_analitica/></strong>, com <strong>R$ <Value data={insight_categoria} column=total_gasto fmt='#,##0.00'/></strong>.</p>
{/if}

## Evolução mensal

```sql mensal
select
    competencia,
    sum(valor_liquido) as valor_liquido,
    sum(valor_glosa) as valor_glosa
from ${base}
group by competencia
order by competencia
```

<LineChart
    data={mensal}
    x=competencia
    y={['valor_liquido','valor_glosa']}
    yFmt='#,##0'
    title="Despesas e glosas por mês"
    emptySet=warn
/>

## Onde o dinheiro está concentrado?

```sql categorias
select
    categoria_analitica,
    sum(valor_liquido) as valor_liquido
from ${base}
group by categoria_analitica
order by valor_liquido desc
```

```sql classificacao
select
    classificacao_uso,
    sum(valor_liquido) as valor_liquido
from ${base}
group by classificacao_uso
order by valor_liquido desc
```

<BarChart
    data={categorias}
    x=categoria_analitica
    y=valor_liquido
    yFmt='#,##0'
    swapXY=true
    title="Despesas por categoria analítica"
    emptySet=warn
/>

<BarChart
    data={classificacao}
    x=classificacao_uso
    y=valor_liquido
    yFmt='#,##0'
    swapXY=true
    title="Despesas por classificação de uso"
    emptySet=warn
/>

## Ranking de deputados

```sql ranking
select
    deputado,
    sigla_partido,
    sigla_uf,
    sum(quantidade_despesas) as documentos,
    sum(valor_liquido) as total_gasto,
    sum(valor_glosa) as total_glosado,
    case when sum(quantidade_despesas) = 0 then 0
         else sum(valor_liquido) / sum(quantidade_despesas) end as gasto_medio
from ${base}
group by deputado, sigla_partido, sigla_uf
order by total_gasto desc
```

<DataTable data={ranking} search=true rows=15>
    <Column id=deputado title="Deputado"/>
    <Column id=sigla_partido title="Partido"/>
    <Column id=sigla_uf title="UF"/>
    <Column id=documentos title="Documentos" fmt='#,##0'/>
    <Column id=total_gasto title="Total gasto (R$)" fmt='#,##0.00'/>
    <Column id=total_glosado title="Glosado (R$)" fmt='#,##0.00'/>
    <Column id=gasto_medio title="Média (R$)" fmt='#,##0.00'/>
</DataTable>
