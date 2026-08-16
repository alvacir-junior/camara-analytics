---
title: Votações
---

# 🗳️ Votações parlamentares

Participação parlamentar, composição dos votos e comportamento por partido e UF.

```sql legislaturas
select distinct cast(id_legislatura as varchar) as id_legislatura
from camara_db.votos
order by id_legislatura desc
```

```sql anos
select distinct cast(ano as varchar) as ano
from camara_db.votos
where ano is not null
order by ano desc
```

```sql partidos
select distinct sigla_partido
from camara_db.votos
order by sigla_partido
```

```sql ufs
select distinct sigla_uf
from camara_db.votos
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
from camara_db.votos
where cast(id_legislatura as varchar) like '${inputs.legislatura.value}'
  and cast(ano as varchar) like '${inputs.ano.value}'
  and sigla_partido like '${inputs.partido.value}'
  and sigla_uf like '${inputs.uf.value}'
```

```sql kpis
select
    count(*) as votos_registrados,
    count(distinct id_votacao) as votacoes,
    count(distinct id_deputado) as deputados,
    count(*) filter (where upper(tipo_voto) = 'SIM') as votos_sim,
    count(*) filter (where upper(tipo_voto) in ('NÃO','NAO')) as votos_nao,
    count(*) filter (where upper(tipo_voto) in ('ABSTENÇÃO','ABSTENCAO')) as abstencoes
from ${base}
```

<BigValue data={kpis} value=votos_registrados title="Votos registrados" fmt='#,##0'/>
<BigValue data={kpis} value=votacoes title="Votações distintas" fmt='#,##0'/>
<BigValue data={kpis} value=deputados title="Deputados participantes" fmt='#,##0'/>
<BigValue data={kpis} value=votos_sim title="Votos Sim" fmt='#,##0'/>
<BigValue data={kpis} value=votos_nao title="Votos Não" fmt='#,##0'/>
<BigValue data={kpis} value=abstencoes title="Abstenções" fmt='#,##0'/>

```sql insight_tipo_voto
select upper(coalesce(tipo_voto,'N/D')) as tipo_voto, count(*) as quantidade
from ${base}
group by tipo_voto
order by quantidade desc
limit 1
```

```sql insight_participacao
select deputado, count(*) as votos_registrados
from ${base}
group by deputado
order by votos_registrados desc
limit 1
```

{#if insight_tipo_voto.length > 0}
<p><strong>Destaque do recorte:</strong> o tipo de voto mais frequente é <strong><Value data={insight_tipo_voto} column=tipo_voto/></strong>, com <Value data={insight_tipo_voto} column=quantidade fmt='#,##0'/> registros.</p>
{/if}

{#if insight_participacao.length > 0}
<p>O maior volume de votos registrados pertence a <strong><Value data={insight_participacao} column=deputado/></strong>, com <Value data={insight_participacao} column=votos_registrados fmt='#,##0'/> registros.</p>
{/if}

## Evolução e composição

```sql mensal
select
    competencia,
    count(*) as votos_registrados,
    count(distinct id_votacao) as votacoes
from ${base}
group by competencia
order by competencia
```

```sql tipos_voto
select
    upper(coalesce(tipo_voto,'N/D')) as tipo_voto,
    count(*) as quantidade
from ${base}
group by tipo_voto
order by quantidade desc
```

<LineChart
    data={mensal}
    x=competencia
    y={['votos_registrados','votacoes']}
    title="Atividade de votação por mês"
    emptySet=warn
/>

<BarChart
    data={tipos_voto}
    x=tipo_voto
    y=quantidade
    title="Distribuição dos tipos de voto"
    emptySet=warn
/>

## Participação por deputado

```sql participacao
select
    deputado,
    sigla_partido,
    sigla_uf,
    count(*) as votos_registrados,
    count(distinct id_votacao) as votacoes_participadas,
    count(*) filter (where upper(tipo_voto) in ('ABSTENÇÃO','ABSTENCAO')) as abstencoes
from ${base}
group by deputado, sigla_partido, sigla_uf
order by votos_registrados desc
```

```sql top_participacao
select * from ${participacao}
limit 15
```

<BarChart
    data={top_participacao}
    x=deputado
    y=votos_registrados
    swapXY=true
    title="Deputados com mais votos registrados"
    emptySet=warn
/>

<DataTable data={participacao} search=true rows=15>
    <Column id=deputado title="Deputado"/>
    <Column id=sigla_partido title="Partido"/>
    <Column id=sigla_uf title="UF"/>
    <Column id=votos_registrados title="Votos" fmt='#,##0'/>
    <Column id=votacoes_participadas title="Votações" fmt='#,##0'/>
    <Column id=abstencoes title="Abstenções" fmt='#,##0'/>
</DataTable>

## Tipos de proposição

```sql proposicoes
select
    tipo_proposicao,
    sum(quantidade_registros) as votos_registrados,
    sum(quantidade_votacoes) as participacoes_em_votacoes
from camara_db.votos_proposicoes
where cast(id_legislatura as varchar) like '${inputs.legislatura.value}'
  and sigla_partido like '${inputs.partido.value}'
  and sigla_uf like '${inputs.uf.value}'
group by tipo_proposicao
order by votos_registrados desc
limit 20
```

<BarChart
    data={proposicoes}
    x=tipo_proposicao
    y=votos_registrados
    swapXY=true
    title="Votos por tipo de proposição"
    emptySet=warn
/>
