SELECT
    d.id_legislatura,
    d.id_deputado,
    d.nome AS deputado,
    d.em_exercicio,
    d.data_referencia_exercicio,
    coalesce(p.sigla_partido, 'N/D') AS sigla_partido,
    coalesce(u.sigla_uf, 'N/D') AS sigla_uf,
    v.id_votacao,
    cast(v.data AS DATE) AS data_votacao,
    date_trunc('month', cast(v.data AS DATE)) AS competencia,
    year(cast(v.data AS DATE)) AS ano,
    f.tipo_voto,
    v.aprovacao,
    v.sigla_orgao,
    v.descricao
FROM dw.fact_voto_deputado AS f
LEFT JOIN dw.dim_deputado AS d
    ON d.sk_deputado = f.sk_deputado
LEFT JOIN dw.dim_partido AS p
    ON p.sk_partido = f.sk_partido
LEFT JOIN dw.dim_uf AS u
    ON u.sk_uf = f.sk_uf
LEFT JOIN dw.dim_votacao AS v
    ON v.sk_votacao = f.sk_votacao
WHERE d.id_deputado IS NOT NULL
  AND v.id_votacao IS NOT NULL;
