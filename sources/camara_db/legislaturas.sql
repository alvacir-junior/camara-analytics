SELECT
    id_legislatura,
    data_inicio,
    data_fim,
    quantidade_deputados,
    quantidade_cadastro_oficial,
    quantidade_membros_inferidos,
    quantidade_em_exercicio,
    quantidade_deputados_distintos
FROM dm.resumo_legislaturas
ORDER BY id_legislatura DESC;
