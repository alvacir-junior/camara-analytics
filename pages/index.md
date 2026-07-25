# 🏛️ Painel Geral de Eficiência Parlamentar

```sql deputados
select 
    nome_deputado,
    partido,
    uf,
    nota_eficiencia_geral,
    total_gasto_ceap
from gold.obt_eficiencia_deputados
order by nota_eficiencia_geral desc