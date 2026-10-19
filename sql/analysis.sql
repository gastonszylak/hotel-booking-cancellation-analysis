-- =====================================================================
-- Análisis SQL — Cancelaciones de reservas hoteleras (jul-2015 a ago-2017)
-- Motor: SQLite (sintaxis estándar; compatible con MySQL 8 / SQL Server).
-- Tabla: bookings (1 fila por reserva). Ingresos en euros.
-- Cada consulta empieza con "-- name:" para que src/run_sql.py la ejecute.
-- =====================================================================

-- name: 01_kpis_por_hotel
SELECT hotel,
       COUNT(*)                                                         AS reservas,
       ROUND(100.0 * AVG(is_canceled), 1)                               AS tasa_cancelacion_pct,
       ROUND(SUM(CASE WHEN is_canceled = 0 THEN revenue END), 0)        AS ingreso_realizado_eur,
       ROUND(SUM(CASE WHEN is_canceled = 1 THEN revenue END), 0)        AS ingreso_cancelado_eur,
       ROUND(AVG(CASE WHEN is_canceled = 0 THEN adr END), 1)            AS tarifa_promedio_eur
FROM bookings
GROUP BY hotel
UNION ALL
SELECT 'TOTAL', COUNT(*), ROUND(100.0 * AVG(is_canceled), 1),
       ROUND(SUM(CASE WHEN is_canceled = 0 THEN revenue END), 0),
       ROUND(SUM(CASE WHEN is_canceled = 1 THEN revenue END), 0),
       ROUND(AVG(CASE WHEN is_canceled = 0 THEN adr END), 1)
FROM bookings;

-- name: 02_cancelacion_por_anticipacion
SELECT lead_time_band                       AS anticipacion,
       COUNT(*)                             AS reservas,
       ROUND(100.0 * AVG(is_canceled), 1)   AS tasa_cancelacion_pct
FROM bookings
GROUP BY lead_time_band
ORDER BY MIN(lead_time);

-- name: 03_cancelacion_por_segmento
SELECT market_segment                                       AS segmento,
       COUNT(*)                                             AS reservas,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)   AS pct_reservas,
       ROUND(100.0 * AVG(is_canceled), 1)                   AS tasa_cancelacion_pct,
       ROUND(SUM(CASE WHEN is_canceled = 1 THEN revenue END) / 1000.0, 0) AS ingreso_cancelado_miles_eur
FROM bookings
GROUP BY market_segment
HAVING COUNT(*) >= 500
ORDER BY ingreso_cancelado_miles_eur DESC;

-- name: 04_senales_de_compromiso
SELECT 'Pedidos especiales: ' || special_requests_band AS senal,
       COUNT(*) AS reservas, ROUND(100.0 * AVG(is_canceled), 1) AS tasa_cancelacion_pct
FROM bookings GROUP BY special_requests_band
UNION ALL
SELECT CASE WHEN is_repeated_guest = 1 THEN 'Huésped que repite' ELSE 'Huésped nuevo' END,
       COUNT(*), ROUND(100.0 * AVG(is_canceled), 1)
FROM bookings GROUP BY is_repeated_guest
UNION ALL
SELECT CASE WHEN had_previous_cancel = 1 THEN 'Canceló antes' ELSE 'Sin cancelaciones previas' END,
       COUNT(*), ROUND(100.0 * AVG(is_canceled), 1)
FROM bookings GROUP BY had_previous_cancel;

-- name: 05_ingreso_cancelado_por_mes_de_llegada
-- Solo 2016 (único año completo): jul-ago aparecen en 3 años y el resto en 2.
SELECT arrival_month_num                                                     AS mes,
       arrival_month_name                                                    AS nombre,
       ROUND(100.0 * AVG(is_canceled), 1)                                    AS tasa_cancelacion_pct,
       ROUND(SUM(CASE WHEN is_canceled = 1 THEN revenue END) / 1000.0, 0)    AS ingreso_cancelado_miles_eur
FROM bookings
WHERE arrival_date_year = 2016
GROUP BY arrival_month_num, arrival_month_name
ORDER BY arrival_month_num;

-- name: 06_validacion_nivel_de_riesgo_2017
-- El puntaje se diseñó mirando 2015-2016; acá se valida sobre llegadas de 2017.
SELECT risk_level                                   AS nivel_riesgo,
       COUNT(*)                                     AS reservas_2017,
       ROUND(100.0 * AVG(is_canceled), 1)           AS tasa_cancelacion_pct,
       ROUND(100.0 * SUM(is_canceled) / SUM(SUM(is_canceled)) OVER (), 1) AS pct_de_todas_las_cancelaciones
FROM bookings
WHERE arrival_date_year = 2017
GROUP BY risk_level
ORDER BY tasa_cancelacion_pct;

-- name: 07_top_paises_ingreso_cancelado
WITH paises AS (
    SELECT country,
           COUNT(*)                                             AS reservas,
           AVG(is_canceled)                                     AS tasa,
           SUM(CASE WHEN is_canceled = 1 THEN revenue END)      AS cancelado
    FROM bookings
    GROUP BY country
)
SELECT country                              AS pais,
       reservas,
       ROUND(100.0 * tasa, 1)               AS tasa_cancelacion_pct,
       ROUND(cancelado / 1000.0, 0)         AS ingreso_cancelado_miles_eur,
       RANK() OVER (ORDER BY cancelado DESC) AS ranking
FROM paises
ORDER BY ranking
LIMIT 8;
