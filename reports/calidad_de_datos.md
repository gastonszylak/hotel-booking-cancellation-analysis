# Reporte de calidad de datos

## Fuente

- `hotel_bookings.csv`: 119,390 reservas, 32 columnas (llegadas jul-2015 a ago-2017, un hotel urbano y un resort en Portugal)

## Valores faltantes

- `children`: 4 nulos -> 0
- `country`: 488 nulos -> 'Desconocido'
- `agent`: 16,340 nulos -> reserva sin agencia (se crea `has_agent`)
- `company`: 112,593 nulos (94%) -> se descarta la columna

## Registros inválidos (eliminados)

- sin huéspedes (0 adultos, niños y bebés): 180
- 0 noches de estadía: 715
- tarifa diaria (ADR) negativa: 1
- ADR > 1.000 € (outlier extremo: 5.400 €): 1
- **Total eliminado: 827 (0.7%)**

## Duplicados

- Filas idénticas: 31,933. Se **conservan**: el dataset no tiene ID de reserva y las reservas grupales generan filas iguales legítimas.

## Advertencias de análisis

- **Anomalía:** las reservas con depósito *no reembolsable* figuran canceladas en un 99%. Va contra la lógica del negocio y probablemente sea un error de registro; se reporta pero no se usa para sacar conclusiones.
- `reservation_status`, `reservation_status_date` y `assigned_room_type` se conocen **después** del resultado de la reserva; no se usan para segmentar el riesgo (evita fuga de información).

## Salida

- `bookings.csv`: 118,563 reservas, 34 columnas
