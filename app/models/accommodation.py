import uuid
import enum
from typing import List, Optional
from sqlalchemy import String, Float, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base_class import Base

class TargetAudience(str, enum.Enum):
    BOYS = "Boys"
    GIRLS = "Girls"
    CO_ED = "Co-ed"

class Accommodation(Base):
    __tablename__ = "accommodations"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    area: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    address: Mapped[str] = mapped_column(String(500), nullable=False)
    contact_number: Mapped[str] = mapped_column(String(50), nullable=False)
    target_audience: Mapped[TargetAudience] = mapped_column(Enum(TargetAudience), nullable=False, index=True)
    features: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    distance_from_college_km: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    def __repr__(self) -> str:
        return f"<Accommodation id={self.id} name={self.name} area={self.area} target_audience={self.target_audience}>"
