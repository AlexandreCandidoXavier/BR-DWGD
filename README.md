# BR-DWGD
Brazilian Daily  Weather  Gridded  Data new version. Homepage dos dados [aqui](https://sites.google.com/site/alexandrecandidoxavierufes/brazilian-daily-weather-gridded-data?authuser=0)

# Exportando dados arquivos csv

O script [export2cvs.csv](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/export2cvs.py) apresenta 
como exportar os dados diários de posições geográficas para arquivos no formato *csv*.

# Os resultados gráficos dos scripts

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

[exemplo7.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/exemplo7.py) Calculo da diferenca sazonal entre a precipitacao e a 
ET0 para o Brasil utilizando os dados gradeados (1980/01/01-2009/12/31)

![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo7.jpeg)

[exemplo8.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/exemplo8.py) Abrindo e plotando a normal da temperatura media do mês janeiro, período 1961/01/01-1989/12/31.

![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo8_1.jpeg)
![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo8_2.jpeg)


[exemplo9.py](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/exemplo9.py) Comportamento da temperatura média anual para as diferentes regiões, período 1961-2019.

![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo9_1.jpeg)
![](https://github.com/AlexandreCandidoXavier/BR-DWGD/blob/main/exemplos/imagens/resultado_exemplo9_2.jpeg)

**Estatísticas:**

|Região      |<html>&Delta; (&#8451;/ano)</html>|R           |p_value     |std_err     |
|------------|------------|------------|------------|------------|
|Sul         |0.019       |0.656       |1.69e-08    |0.002       |
|Sudeste     |0.023       |0.778       |3.87e-13    |0.002       |
|Nordeste    |0.028       |0.854       |6.98e-18    |0.002       |
|Centro-Oeste|0.025       |0.842       |5.90e-17    |0.002       |
|Norte       |0.028       |0.877       |7.28e-20    |0.002       |

