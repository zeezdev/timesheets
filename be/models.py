import sqlalchemy.sql.elements
from sqlalchemy import Text, ForeignKey, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import false


class Base(DeclarativeBase):
    __table_args__ = {'sqlite_autoincrement': True}


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text(), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True, server_default=None)
    tasks: Mapped[list['Task']] = relationship(back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f'Category(id={self.id!r}, name={self.name!r}, description={self.description!r})'


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text(), nullable=False, unique=True)
    is_archived: Mapped[bool] = mapped_column(Boolean(), default=False, server_default=false())
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped['Category'] = relationship(back_populates='tasks')
    work_items: Mapped[list['WorkItem']] = relationship(back_populates='task', cascade='all, delete-orphan')

    def __repr__(self):
        return f'Task(id={self.id!r}, name={self.name!r}, category_id={self.category_id!r})'

    # @property
    # def is_current(self) -> bool:
    #     return self.work_items.fi


class WorkItem(Base):
    __tablename__ = 'work_items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))
    task: Mapped['Task'] = relationship(back_populates='work_items')
    start_timestamp: Mapped[int]
    end_timestamp: Mapped[int | None] = mapped_column(nullable=True, server_default=sqlalchemy.sql.elements.TextClause('NULL'))
