import uuid
from typing import List, Dict
from sqlalchemy import String, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class FastFoodSpot(Base):
    __tablename__ = "fast_food_spots"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    area: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    contact_number: Mapped[str] = mapped_column(String(50), nullable=False)
    specialties: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    average_cost_for_two: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    top_items: Mapped[Dict[str, float]] = mapped_column(JSON, default=dict, nullable=False)

    def __repr__(self) -> str:
        return f"<FastFoodSpot id={self.id} name={self.name} area={self.area} cost_for_two={self.average_cost_for_two}>"
