from datetime import date
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"
SAMPLE_CVS = FIXTURES / "cvs"
# The golden snapshot was produced with this date as "today".
REFERENCE_DATE = date(2026, 11, 16)
