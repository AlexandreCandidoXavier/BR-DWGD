# Brazilian Daily  Weather Gridded  Data (BR-DWGD)
Estes códigos pretendem demonstrar algumas possibilidades de utilização da grade
BR-DWGD por meio da linguagem Python. Encontrando erros, por favor entrar em contato (alexandre.xavier@ufes.br).


<p><strong><span style="color: #ff0000;">NOTA: 
</span></strong><span style="color: #ff0000;">Para rodar os códigos abaixo, serão necessários &plusmn;6GB de memória
RAM livre.</span></p>

## Informações sobre atualizações da **BR-DWGB**

[https://sites.google.com/site/alexandrecandidoxavierufes/brazilian-daily-weather-gridded-data?authuser=0](https://sites.google.com/site/alexandrecandidoxavierufes/brazilian-daily-weather-gridded-data?authuser=0)

## Download da grade (BR-DWGD)
[**Aqui**](https://drive.google.com/drive/folders/11-qnvwojirAtaQxSE03N0_SUrbcsz44N)

## Citação dos dados

Caso venha a utilizar os dados, solicitamos que seja devidamente citado como:

Xavier, A. C., Scanlon, B. R., King, C. W., & Alves, A. I. (2022). 
New improved Brazilian daily weather gridded data (1961–2020). **International 
Journal of Climatology**, 42(16), 8390– 8404. https://doi.org/10.1002/joc.7731

## Exportando dados para arquivos csv

Para exportar em *csv*:

1. **todas as variáveis de pontos geográficos específicos, na escala de tempo:**
   1. diária [export2cvs_daily_points.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/export2cvs_daily_points.py)
   2. mensal [export2cvs_monthly_points.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/export2cvs_monthly_points.py)
2. **todas as variáveis, de todas as células, em uma região com limite geográfico conhecido, na escala de tempo:**
   1. diária [export2csv_daily_region.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/export2csv_daily_region.py)
   2. mensal [export2csv_monthly_region.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/export2csv_monthly_region.py)
   
## Para exportar dados, em nível municipal, nos formatos *geojson*, *shp* ou *gpkg*

No exemplo do código [extraindo_dados_nivel_municipal.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/extraindo_dados_nivel_municipal.py),
é extraida a precipitação acumulada mensal de todos os municípios do Brasil 
(jan/1961-dec/2022), e estes dados, exportados para um arquivo no formato 
*geojson*.
Para modificar:

1. a variável que vai ser utilizada, modificar **linha 48**;
2. a escala de tempo, modificar **linha 51**;
3. o nome/formato do arquivo a ser exportado (*shapefile*, *geojson* ou *gpkg*), 
   modificar **linha 55** e;
4. se a variável a ser exportada vai ser a acumulada ou a média 
   do período, modificar **linha 87**.

Resultado gráfico do código, apenas para exemplificar o procedimento: (*i*)
a precipitação acumulada para jan/1961; (*ii*) a precipitação acumulada 
extrapolada para jan/1961 e; (*iii*) precipitação acumulada para jan/1961
em nível municipal.

![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/extracao_municipal.jpeg)

## Resultados gráficos dos scripts

[exemplo1.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/exemplo1.py) Plotando dados e controles

![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo1.jpeg)

[exemplo2.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/exemplo2.py) Para uma posição geográfica, exportando dados diários de Tmax no formato "csv" e plotando sua série histórica assim como média mensal. Período 01/01/1961-31/12/1989.

![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo2.jpeg)

[exemplo3.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/exemplo3.py) Normais RH, período 1990-01-01 a 2019-12-31.

![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo3.jpeg)

[exemplo4.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/exemplo4.py) Mensais ETo, período 1961-01-01 a 1989-12-31.

![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo4.jpeg)

[exemplo5.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/exemplo5.py) Plotando e exportando em "csv" normais mensais de Tmax para 
algumas localidades. Normais 01/01/1990 a 31/12/2019.

![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo5.jpeg)

[exemplo6.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/exemplo6.py) Plotando controles para duas posições

![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo6.jpeg)

[exemplo7.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/exemplo7.py) Cálculo da diferenca sazonal entre a precipitacao e a 
ET0 para o Brasil utilizando os dados gradeados (1980/01/01-2009/12/31)

![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo7.jpeg)

[exemplo8.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/exemplo8.py) Abrindo e plotando a normal da temperatura media do mês janeiro, período 1961/01/01-1989/12/31.

![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo8_1.jpeg)
![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo8_2.jpeg)


[exemplo9.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/exemplo9.py) Comportamento da temperatura média anual para as diferentes regiões, período 1961-2019.

![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo9_1.jpeg)
![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo9_2.jpeg)

**Estatísticas:** 

|Região      |<html>&Delta; (&#8451;/ano)</html>|R           | p_value  |std_err     |
|------------|------------|------------|----------|------------|
|Sul         |0.019       |0.660       | 1.66e-08 |0.003       |
|Sudeste     |0.023       |0.779       | 3.73e-13 |0.002       |
|Nordeste    |0.029       |0.855       | 7.07e-18 |0.002       |
|Centro-Oeste|0.026       |0.843       | 5.26e-17 |0.002       |
|Norte       |0.028       |0.877       | 7.54e-20 |0.002       |

