SELECT
    (SELECT max(cast(data_documento AS DATE)) FROM dw.fact_despesa_deputado) AS ultima_despesa,
    (SELECT max(cast(data_hora_registro AS DATE)) FROM dw.fact_voto_deputado) AS ultimo_voto,
    (SELECT max(data_referencia_exercicio) FROM dw.dim_deputado) AS referencia_exercicio,
    (SELECT count(*) FROM dw.fact_despesa_deputado) AS linhas_despesas,
    (SELECT count(*) FROM dw.fact_voto_deputado) AS linhas_votos;
