import uuid

from datetime import datetime
from pydantic import BaseModel, Field

from typing import Literal, Optional
from typing_extensions import Annotated


PositiveFloat = Annotated[float, Field(gt=0)]


class TransactionInfo(BaseModel):
    transaction_date: datetime
    liters_purchased: PositiveFloat
    price: PositiveFloat
    gas_type: Literal["DT", "92", "98", "100"]


class UpdateTransactionInfo(BaseModel):
    transaction_date: Optional[datetime] = None
    liters_purchased: Optional[PositiveFloat] = None
    price: Optional[PositiveFloat] = None
    gas_type: Optional[Literal["DT", "92", "98", "100"]] = None


class GasStationTransaction(BaseModel):
    transaction_id: uuid.UUID = Field(default_factory=uuid.uuid4)
    transaction_info: TransactionInfo
