import uuid
import enum
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class FoodServiceType(str, enum.Enum):
    TIFFIN = "Tiffin"
    DHABA = "Dhaba"
    BHOJNALAYA = "Bhojnalaya"

class BudgetType(str, enum.Enum):
    BUDGET = "Budget"
    MID_RANGE = "Mid-range"

class FoodService(Base):
    __tablename__ = "food_services"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    type: Mapped[FoodServiceType] = mapped_column(Enum(FoodServiceType), nullable=False, index=True)
    area: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    contact_number: Mapped[str] = mapped_column(String(50), nullable=False)
    timings: Mapped[str] = mapped_column(String(255), nullable=False)
    budget_type: Mapped[BudgetType] = mapped_column(Enum(BudgetType), nullable=False, index=True)
    usp: Mapped[str] = mapped_column(String(255), nullable=False)

    def __repr__(self) -> str:
        return f"<FoodService id={self.id} name={self.name} type={self.type} area={self.area}>"
