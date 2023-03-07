from __future__ import annotations

import pandas as pd

from dataclasses import dataclass
from typing import Optional

# from ....loan.computation.categoties import amortization as amortization_methods

@dataclass
class DataSource:
    _data: pd.DataFrame

    def filter():
        pass
    @property
    def amortization_methods(self) -> list[str]:
        return [*amortization_methods.keys()]