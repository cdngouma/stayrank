from typing import Optional
import pandas as pd
from stayrank.config import BOROUGH_CONTEXT_PATH
from stayrank.models.schemas import BoroughContext


BOROUGH_CONTEXT = pd.read_parquet(BOROUGH_CONTEXT_PATH)


def get_borough_context(borough: str) -> Optional[BoroughContext]:
    if not borough or not isinstance(borough, str):
        return None
    
    context = BOROUGH_CONTEXT.copy()

    match = (
        context[context["borough"].str.strip().str.lower() == borough.strip().lower()]
    )

    if match.empty:
        return None
    
    row = match.iloc[0]

    return BoroughContext(
        borough=row["borough"],
        dining=row["dining"],
        shopping=row["shopping"],
        parks=row["parks"],
        nightlife=row["nightlife"]
    )