import sqlalchemy.sql.elements
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    __table_args__ = {'sqlite_autoincrement': True}


class Category(Base):
    """
    execute_statement('''
    CREATE TABLE IF NOT EXISTS main.categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
    )''')
    """

    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text(), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text(), nullable=True, server_default=None)
    tasks: Mapped[list['Task']] = relationship(back_populates='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f'Category(id={self.id!r}, name={self.name!r}, description={self.description!r})'


class Task(Base):
    """
    execute_statement('''
    CREATE TABLE IF NOT EXISTS main.tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    category_id INTEGER,
    FOREIGN KEY (category_id)
        REFERENCES categories(id)
            ON DELETE CASCADE ON UPDATE NO ACTION
    )''')
    """
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text(), nullable=False, unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    category: Mapped['Category'] = relationship(back_populates='tasks')
    work_items: Mapped[list['WorkItem']] = relationship(back_populates='task', cascade='all, delete-orphan')

    def __repr__(self):
        return f'Task(id={self.id!r}, name={self.name!r}, category_id={self.category_id!r})'

    # @property
    # def is_current(self) -> bool:
    #     return self.work_items.fi

class WorkItem(Base):
    """
    execute_statement('''
    CREATE TABLE IF NOT EXISTS main.work_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER,
    -- comment TEXT,
    start_timestamp INTEGER NOT NULL,
    end_timestamp INTEGER DEFAULT NULL,
    FOREIGN KEY (task_id)
        REFERENCES tasks(id)
            ON DELETE CASCADE ON UPDATE NO ACTION
    )''')
    """
    __tablename__ = 'work_items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('tasks.id'))
    task: Mapped['Task'] = relationship(back_populates='work_items')
    start_timestamp: Mapped[int]
    end_timestamp: Mapped[int | None] = mapped_column(nullable=True, server_default=sqlalchemy.sql.elements.TextClause('NULL'))
