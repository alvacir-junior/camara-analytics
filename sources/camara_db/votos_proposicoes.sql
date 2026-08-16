SELECT
    id_legislatura,
    id_deputado,
    deputado,
    coalesce(sigla_partido, 'N/D') AS sigla_partido,
    coalesce(sigla_uf, 'N/D') AS sigla_uf,
    coalesce(tipo_proposicao, 'N/D') AS tipo_proposicao,
    coalesce(tipo_voto, 'N/D') AS tipo_voto,
    quantidade_votacoes,
    quantidade_registros
FROM dm.votos_por_tipo_proposicao;
