"""
Carga la tabla limpia en una base SQLite y ejecuta las consultas de sql/analysis.sql.
Los resultados se guardan en reports/resultados_sql.md.

Uso:  python src/run_sql.py
"""
import re
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "hotel.db"


def main() -> None:
    DB.unlink(missing_ok=True)
    con = sqlite3.connect(DB)
    b = pd.read_csv(ROOT / "data" / "processed" / "bookings.csv")
    for c in ["had_previous_cancel", "has_agent"]:
        b[c] = b[c].astype(int)
    b.to_sql("bookings", con, index=False)

    sql = (ROOT / "sql" / "analysis.sql").read_text(encoding="utf-8")
    blocks = re.split(r"^-- name: (\S+)\s*$", sql, flags=re.M)[1:]
    out = ["# Resultados de las consultas SQL\n",
           "Generado por `src/run_sql.py` a partir de `sql/analysis.sql`.\n"]
    for name, query in zip(blocks[::2], blocks[1::2]):
        df = pd.read_sql_query(query, con)
        out.append(f"## {name}\n\n{df.to_markdown(index=False)}\n")
        print(f"\n== {name}\n{df.to_string(index=False)}")
    (ROOT / "reports" / "resultados_sql.md").write_text("\n".join(out), encoding="utf-8")
    con.close()


if __name__ == "__main__":
    main()
