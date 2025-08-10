from pydantic import BaseModel, ConfigDict, Field, computed_field
import uuid
from datetime import date as date_type

class WorkTimeData(BaseModel):
    date: date_type = Field(default_factory=date_type.today)
    time_material: float = Field(default=1.5, ge=0.0, description="Time spent on material in minutes")
    qty_material: int = Field(default=20,ge=0, description="Quantity of material used")
    time_plus: int = Field(default=0, description="Additional time in minutes")

class WorkTimeCreate(WorkTimeData):
    pass

class WorkTime(WorkTimeData):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)

    @computed_field(return_type=float)
    def total_time(self):
        return round((self.time_material * self.qty_material + self.time_plus) / 60, 2)

    model_config = ConfigDict(from_attributes=True)
