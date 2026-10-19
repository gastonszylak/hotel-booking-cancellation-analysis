"""
Exporta la tabla que consume el tablero de Power BI (data/powerbi/pbi_bookings.csv),
con columnas de orden para que los tramos se muestren en secuencia lógica.

Uso:  python src/export_powerbi.py   (después de src/clean.py)
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "powerbi"
OUT.mkdir(parents=True, exist_ok=True)

LEAD = ["0-7 días", "8-30 días", "31-90 días", "91-180 días", "181-365 días", "+365 días"]


def main() -> None:
    h = pd.read_csv(ROOT / "data" / "processed" / "bookings.csv")
    h["lead_time_band_order"] = h.lead_time_band.map({b: i for i, b in enumerate(LEAD)})
    h["risk_level_order"] = h.risk_level.map({"Bajo": 0, "Medio": 1, "Alto": 2})
    h["special_requests_order"] = h.special_requests_band.map({"Sin pedidos": 0, "1 pedido": 1, "2 o más": 2})
    for c in ["had_previous_cancel", "has_agent"]:
        h[c] = h[c].astype(int)
    cols = ["hotel", "is_canceled", "arrival_date", "arrival_date_year", "arrival_month", "lead_time",
            "lead_time_band", "lead_time_band_order", "nights", "guests", "country", "market_segment",
            "distribution_channel", "customer_type", "deposit_type", "is_repeated_guest", "had_previous_cancel",
            "total_of_special_requests", "special_requests_band", "special_requests_order", "adr", "revenue",
            "risk_score", "risk_level", "risk_level_order"]
    h[cols].to_csv(OUT / "pbi_bookings.csv", index=False)
    print(f"pbi_bookings.csv: {len(h):,} filas")


if __name__ == "__main__":
    main()
