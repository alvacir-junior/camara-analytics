---
title: Deputados
---

# 👥 Deputados

Painel de comparação de atividade parlamentar e despesas no contexto de cada legislatura.

```sql legislaturas
select distinct cast(id_legislatura as varchar) as id_legislatura
from camara_db.deputados
order by id_legislatura desc
```

<Dropdown name=legislatura data={legislaturas} value=id_legislatura title="Legislatura" defaultValue="%">
    <DropdownOption value="%" valueLabel="Todas"/>
</Dropdown>

<Dropdown name=situacao title="Situação atual" defaultValue="TODOS">
    <DropdownOption value="TODOS" valueLabel="Todos"/>
    <DropdownOption value="ATIVOS" valueLabel="Em exercício"/>
    <DropdownOption value="INATIVOS" valueLabel="Fora de exercício"/>
</Dropdown>

```sql base
select
    *,
    case when quantidade_votos = 0 then 0
         else abstencoes::double / quantidade_votos end as taxa_abstencao
from camara_db.deputados
where cast(id_legislatura as varchar) like '${inputs.legislatura.value}'
  and (
      '${inputs.situacao.value}' = 'TODOS'
      or ('${inputs.situacao.value}' = 'ATIVOS' and em_exercicio = true)
      or ('${inputs.situacao.value}' = 'INATIVOS' and coalesce(em_exercicio,false) = false)
  )
```

```sql kpis
select
    count(distinct id_deputado) as deputados,
    count(*) filter (where em_exercicio = true) as em_exercicio,
    coalesce(sum(total_gasto),0) as total_gasto,
    coalesce(sum(quantidade_votos),0) as votos,
    coalesce(sum(quantidade_despesas),0) as despesas
from ${base}
```

<BigValue data={kpis} value=deputados title="Deputados" fmt='#,##0'/>
<BigValue data={kpis} value=em_exercicio title="Em exercício" fmt='#,##0'/>
<BigValue data={kpis} value=total_gasto title="Total gasto (R$)" fmt='#,##0.00'/>
<BigValue data={kpis} value=votos title="Votos registrados" fmt='#,##0'/>
<BigValue data={kpis} value=despesas title="Documentos de despesa" fmt='#,##0'/>

```sql insight_gasto
select deputado, total_gasto
from ${base}
order by total_gasto desc
limit 1
```

```sql insight_votos
select deputado, quantidade_votos
from ${base}
order by quantidade_votos desc
limit 1
```

{#if insight_gasto.length > 0}
<p><strong>Maior despesa acumulada no recorte:</strong> <Value data={insight_gasto} column=deputado/>, com <strong>R$ <Value data={insight_gasto} column=total_gasto fmt='#,##0.00'/></strong>.</p>
{/if}

{#if insight_votos.length > 0}
<p><strong>Maior volume de votos registrados:</strong> <Value data={insight_votos} column=deputado/>, com <Value data={insight_votos} column=quantidade_votos fmt='#,##0'/> votos.</p>
{/if}

## Comparativos

```sql top_gastos
select deputado, total_gasto
from ${base}
order by total_gasto desc
limit 15
```

```sql top_votos
select deputado, quantidade_votos
from ${base}
order by quantidade_votos desc
limit 15
```

<BarChart
    data={top_gastos}
    x=deputado
    y=total_gasto
    yFmt='#,##0'
    swapXY=true
    title="Maiores despesas acumuladas"
    emptySet=warn
/>

<BarChart
    data={top_votos}
    x=deputado
    y=quantidade_votos
    swapXY=true
    title="Maior volume de votos registrados"
    emptySet=warn
/>

## Lista de deputados

<DataTable data={base} search=true rows=20>
    <Column id=deputado title="Deputado"/>
    <Column id=id_legislatura title="Legislatura"/>
    <Column id=em_exercicio title="Em exercício"/>
    <Column id=registro_orfao title="Registro inferido"/>
    <Column id=quantidade_votos title="Votos" fmt='#,##0'/>
    <Column id=abstencoes title="Abstenções" fmt='#,##0'/>
    <Column id=taxa_abstencao title="Taxa de abstenção" fmt=pct1/>
    <Column id=quantidade_despesas title="Despesas" fmt='#,##0'/>
    <Column id=total_gasto title="Total gasto (R$)" fmt='#,##0.00'/>
</DataTable>

> O campo **Registro inferido** identifica combinações deputado × legislatura encontradas em fatos, mas que não estavam presentes em uma fonte oficial no momento da carga.
