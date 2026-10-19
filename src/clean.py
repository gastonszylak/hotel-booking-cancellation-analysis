"""
Limpieza y preparación de datos — Reservas hoteleras (Hotel Booking Demand).

Lee data/raw/hotel_bookings.csv, valida calidad, crea variables de negocio y
guarda data/processed/bookings.csv (insumo para SQL, notebook y Power BI).

Uso:  python src/clean.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "hotel_bookings.csv"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

MONTHS = {m: i for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"], start=1)}
MONTHS_ES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

quality_log: list[str] = []


def log(msg: str) -> None:
    print(msg)
    quality_log.append(msg)


def main() -> None:
    h = pd.read_csv(RAW, na_values=["NULL"])
    log("## Fuente\n")
    log(f"- `hotel_bookings.csv`: {len(h):,} reservas, {h.shape[1]} columnas "
        f"(llegadas jul-2015 a ago-2017, un hotel urbano y un resort en Portugal)")

    log("\n## Valores faltantes\n")
    h["children"] = h["children"].fillna(0).astype(int)
    log("- `children`: 4 nulos -> 0")
    log(f"- `country`: {h.country.isna().sum()} nulos -> 'Desconocido'")
    h["country"] = h["country"].fillna("Desconocido")
    log(f"- `agent`: {h.agent.isna().sum():,} nulos -> reserva sin agencia (se crea `has_agent`)")
    log(f"- `company`: {h.company.isna().sum():,} nulos (94%) -> se descarta la columna")
    h["has_agent"] = h.agent.notna()
    h = h.drop(columns=["company"])

    log("\n## Registros inválidos (eliminados)\n")
    n0 = len(h)
    guests = h.adults + h.children + h.babies
    nights = h.stays_in_weekend_nights + h.stays_in_week_nights
    rules = {
        "sin huéspedes (0 adultos, niños y bebés)": guests == 0,
        "0 noches de estadía": nights == 0,
        "tarifa diaria (ADR) negativa": h.adr < 0,
        "ADR > 1.000 € (outlier extremo: 5.400 €)": h.adr > 1000,
    }
    mask = pd.Series(False, index=h.index)
    for desc, m in rules.items():
        log(f"- {desc}: {int(m.sum())}")
        mask |= m
    h = h[~mask].copy()
    log(f"- **Total eliminado: {n0 - len(h):,} ({(n0 - len(h)) / n0:.1%})**")

    log("\n## Duplicados\n")
    dups = h.duplicated().sum()
    log(f"- Filas idénticas: {dups:,}. Se **conservan**: el dataset no tiene ID de reserva y las "
        "reservas grupales generan filas iguales legítimas.")

    # Variables de negocio
    h["arrival_date"] = pd.to_datetime(dict(
        year=h.arrival_date_year, month=h.arrival_date_month.map(MONTHS), day=h.arrival_date_day_of_month))
    h["arrival_month_num"] = h.arrival_date.dt.month
    h["arrival_month"] = h.arrival_date.dt.to_period("M").astype(str)
    h["arrival_month_name"] = h.arrival_month_num.map(lambda m: MONTHS_ES[m - 1])
    h["booking_date"] = h.arrival_date - pd.to_timedelta(h.lead_time, unit="D")
    h["nights"] = h.stays_in_weekend_nights + h.stays_in_week_nights
    h["guests"] = h.adults + h.children + h.babies
    h["revenue"] = (h.adr * h.nights).round(2)  # ingreso de la estadía (realizado o perdido)
    h["lead_time_band"] = pd.cut(
        h.lead_time, [-1, 7, 30, 90, 180, 365, 10_000],
        labels=["0-7 días", "8-30 días", "31-90 días", "91-180 días", "181-365 días", "+365 días"]).astype(str)
    h["special_requests_band"] = np.where(h.total_of_special_requests == 0, "Sin pedidos",
                                          np.where(h.total_of_special_requests == 1, "1 pedido", "2 o más"))
    h["had_previous_cancel"] = h.previous_cancellations > 0
    h["hotel"] = h.hotel.map({"City Hotel": "Hotel urbano", "Resort Hotel": "Resort"})

    # Puntaje de riesgo de cancelación (solo con datos conocidos al momento de reservar)
    h["risk_score"] = (
        np.select([h.lead_time > 90, h.lead_time > 30], [2, 1], 0)
        + h.market_segment.isin(["Online TA", "Offline TA/TO", "Groups"]).astype(int)
        + (h.total_of_special_requests == 0).astype(int)
        + 2 * h.had_previous_cancel.astype(int)
        + (h.is_repeated_guest == 0).astype(int)
    )
    h["risk_level"] = pd.cut(h.risk_score, [-1, 2, 4, 99], labels=["Bajo", "Medio", "Alto"]).astype(str)

    log("\n## Advertencias de análisis\n")
    nr = h[h.deposit_type == "Non Refund"].is_canceled.mean()
    log(f"- **Anomalía:** las reservas con depósito *no reembolsable* figuran canceladas en un {nr:.0%}. "
        "Va contra la lógica del negocio y probablemente sea un error de registro; "
        "se reporta pero no se usa para sacar conclusiones.")
    log("- `reservation_status`, `reservation_status_date` y `assigned_room_type` se conocen **después** "
        "del resultado de la reserva; no se usan para segmentar el riesgo (evita fuga de información).")

    cols = [
        "hotel", "is_canceled", "arrival_date", "arrival_date_year", "arrival_month", "arrival_month_num",
        "arrival_month_name", "booking_date", "lead_time", "lead_time_band", "nights", "guests", "adults",
        "children", "meal", "country", "market_segment", "distribution_channel", "customer_type",
        "deposit_type", "is_repeated_guest", "had_previous_cancel", "previous_cancellations",
        "booking_changes", "days_in_waiting_list", "has_agent", "adr", "revenue",
        "required_car_parking_spaces", "total_of_special_requests", "special_requests_band",
        "reservation_status", "risk_score", "risk_level",
    ]
    h[cols].to_csv(OUT / "bookings.csv", index=False)
    log(f"\n## Salida\n\n- `bookings.csv`: {len(h):,} reservas, {len(cols)} columnas")

    (ROOT / "reports").mkdir(exist_ok=True)
    (ROOT / "reports" / "calidad_de_datos.md").write_text(
        "# Reporte de calidad de datos\n\n" + "\n".join(quality_log) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
