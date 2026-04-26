from dotenv import load_dotenv
load_dotenv()

import sys
from pathlib import Path
import datetime
from sqlalchemy import text

# ensure project root is on sys.path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.database import engine, Base

def main() -> None:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"forward_pe_data_backup_{ts}"

    with engine.begin() as conn:
        # drop the table (cascade for Postgres to remove constraints/indexes)
        conn.execute(text("DROP TABLE IF EXISTS forward_pe_data CASCADE"))
        print("Dropped table forward_pe_data (if it existed).")

    # recreate tables from ORM
    Base.metadata.create_all(bind=engine)
    print("Recreated tables from ORM models.")

if __name__ == "__main__":
    main()