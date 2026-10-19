# Resultados de las consultas SQL

Generado por `src/run_sql.py` a partir de `sql/analysis.sql`.

## 01_kpis_por_hotel

| hotel        |   reservas |   tasa_cancelacion_pct |   ingreso_realizado_eur |   ingreso_cancelado_eur |   tarifa_promedio_eur |
|:-------------|-----------:|-----------------------:|------------------------:|------------------------:|----------------------:|
| Hotel urbano |      78898 |                   41.9 |             1.43853e+07 |             1.08797e+07 |                 106.6 |
| Resort       |      39665 |                   28   |             1.16016e+07 |             5.84218e+06 |                  92   |
| TOTAL        |     118563 |                   37.3 |             2.5987e+07  |             1.67218e+07 |                 101   |

## 02_cancelacion_por_anticipacion

| anticipacion   |   reservas |   tasa_cancelacion_pct |
|:---------------|-----------:|-----------------------:|
| 0-7 días       |      19246 |                    9.7 |
| 8-30 días      |      18848 |                   28   |
| 31-90 días     |      29436 |                   37.8 |
| 91-180 días    |      26384 |                   44.8 |
| 181-365 días   |      21505 |                   55.5 |
| +365 días      |       3144 |                   67.7 |

## 03_cancelacion_por_segmento

| segmento      |   reservas |   pct_reservas |   tasa_cancelacion_pct |   ingreso_cancelado_miles_eur |
|:--------------|-----------:|---------------:|-----------------------:|------------------------------:|
| Online TA     |      56129 |           47.4 |                   36.9 |                         10228 |
| Groups        |      19758 |           16.7 |                   61.2 |                          2801 |
| Offline TA/TO |      24048 |           20.3 |                   34.5 |                          2487 |
| Direct        |      12449 |           10.5 |                   15.5 |                           993 |
| Corporate     |       5231 |            4.4 |                   18.9 |                           196 |
| Complementary |        715 |            0.6 |                   12.2 |                             0 |

## 04_senales_de_compromiso

| senal                           |   reservas |   tasa_cancelacion_pct |
|:--------------------------------|-----------:|-----------------------:|
| Pedidos especiales: 1 pedido    |      33005 |                   22.1 |
| Pedidos especiales: 2 o más     |      15760 |                   21.2 |
| Pedidos especiales: Sin pedidos |      69798 |                   48   |
| Huésped nuevo                   |     115065 |                   37.9 |
| Huésped que repite              |       3498 |                   15.7 |
| Sin cancelaciones previas       |     112088 |                   34.1 |
| Canceló antes                   |       6475 |                   91.7 |

## 05_ingreso_cancelado_por_mes_de_llegada

|   mes | nombre   |   tasa_cancelacion_pct |   ingreso_cancelado_miles_eur |
|------:|:---------|-----------------------:|------------------------------:|
|     1 | Ene      |                   24.9 |                           139 |
|     2 | Feb      |                   34.5 |                           304 |
|     3 | Mar      |                   30.8 |                           454 |
|     4 | Abr      |                   38.1 |                           626 |
|     5 | May      |                   35.4 |                           582 |
|     6 | Jun      |                   39.8 |                           754 |
|     7 | Jul      |                   32.9 |                           783 |
|     8 | Ago      |                   36.3 |                          1088 |
|     9 | Sep      |                   37.6 |                           776 |
|    10 | Oct      |                   40.9 |                           767 |
|    11 | Nov      |                   37.1 |                           448 |
|    12 | Dic      |                   36.6 |                           469 |

## 06_validacion_nivel_de_riesgo_2017

| nivel_riesgo   |   reservas_2017 |   tasa_cancelacion_pct |   pct_de_todas_las_cancelaciones |
|:---------------|----------------:|-----------------------:|---------------------------------:|
| Bajo           |            8978 |                   15.4 |                              8.8 |
| Medio          |           21863 |                   37.1 |                             51.6 |
| Alto           |            9668 |                   64.5 |                             39.7 |

## 07_top_paises_ingreso_cancelado

| pais   |   reservas |   tasa_cancelacion_pct |   ingreso_cancelado_miles_eur |   ranking |
|:-------|-----------:|-----------------------:|------------------------------:|----------:|
| PRT    |      47942 |                   57.3 |                          8581 |         1 |
| GBR    |      12094 |                   20.3 |                          1172 |         2 |
| ESP    |       8544 |                   25.5 |                          1057 |         3 |
| FRA    |      10389 |                   18.6 |                           928 |         4 |
| DEU    |       7285 |                   16.7 |                           556 |         5 |
| ITA    |       3756 |                   35.5 |                           550 |         6 |
| IRL    |       3373 |                   24.7 |                           412 |         7 |
| BRA    |       2217 |                   37.4 |                           386 |         8 |
