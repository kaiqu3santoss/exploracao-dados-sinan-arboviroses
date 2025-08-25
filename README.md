# exploracao-dados-sinan-arboviroses
Exploração estatística de dados públicos do SINAN sobre arboviroses (dengue, zika, chikungunya) no Brasil

---

## Dataset
- **Fonte**: [Portal de Dados Abertos do Governo Federal](https://dados.gov.br/dados/conjuntos-dados/arboviroses-dengue)  
- **Órgão responsável**: Ministério da Saúde — Sistema de Informação de Agravos de Notificação (SINAN)  
- **Período analisado**: 2024  
- **Registros**: ~1,4 milhão  
- **Colunas**: 121 variáveis disponíveis no recorte público (dados anonimizados)  

### Variáveis importantes
- DT_NOTIFIC: Data da notificação  
- DT_SIN_PRI: Data de início dos sintomas  
- SG_UF_NOT: Unidade federativa da notificação  
- NU_IDADE_N: Idade do paciente  
- CS_SEXO: Sexo (M, F, I = ignorado)  
- FEBRE, CEFALEIA, MIALGIA, EXANTEMA: Sintomas clínicos  
- CLASSI_FIN: Classificação final do caso  
- EVOLUCAO: Evolução (cura, óbito, etc.)  

---

## Principais Análises
- Estatísticas descritivas: média, mediana, moda, mínimo, máximo, desvio padrão, variância.  
- Quartis e IQR para identificar outliers (ex.: idades > 100 anos).  
- Valores ausentes: tabela com as 20 variáveis mais afetadas (missing_top20.csv).  
- Distribuição de sexo:  

  F: 765.238 (54,2%)  
  M: 643.940 (45,6%)  
  I: 1.740   (0,12%)  
  vazio: 3 (~0%)  

- Casos por UF e ano: tabela casos_ano_uf.csv mostra a evolução temporal.  
- Idade média por UF: idade_media_por_uf.csv.  
- Visualizações: histogramas, boxplots, série semanal, gráfico de barras de sintomas, heatmap de correlação.  

---

## Como Executar
1. Clone o repositório:
   git clone https://github.com/seu-usuario/exploracao-dados-sinan-arboviroses.git

2. Instale as dependências:
   pip install -r requirements.txt

3. Execute os notebooks da pasta notebooks/.

---

## Autor
- Kaique Santos  
- Universidade do Estado do Amazonas / Engenharia de Computação  
