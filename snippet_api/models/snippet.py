import uuid
from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base


class Snippet(Base):
    __tablename__ = "snippets"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(36), unique=True, index=True,
                                      default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(200))
    code: Mapped[str] = mapped_column(Text)
    language: Mapped[str] = mapped_column(String(50), default="text")
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner = relationship("User", back_populates="snippets")
