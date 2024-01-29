import datetime

import factory
from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory

from database import db_session_context
from dt import get_now_timestamp
from models import Category, Task, WorkItem

init_start_timestamp = datetime.datetime(2024, 1, 1).timestamp()


def session_factory():
    return db_session_context['session']


class CategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Category
        # sqlalchemy_session = Session
        sqlalchemy_session_factory = session_factory
        sqlalchemy_session = None
        sqlalchemy_session_persistence = 'flush'
        # sqlalchemy_session_persistence = None

    name = Sequence(lambda n: f'Category#{n}')
    description = factory.Faker('sentence')

    # @factory.post_generation
    # def tasks(self, create, extracted, **kwargs):
    #     if not create:
    #         return
    #
    #     if extracted is None:
    #         extracted = [TaskFactory(category=self)]
    # #
    # #     if extracted:
    # #         self.tasks.add(*extracted)


class TaskFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Task
        sqlalchemy_session_factory = session_factory
        sqlalchemy_session = None
        sqlalchemy_session_persistence = 'flush'

    name = Sequence(lambda n: f'Task#{n}')
    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def work_items(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted is None:
            extracted = [WorkItemFactory(task=self)]
        #
        # if extracted:
        #     self.work_items.add(*extracted)


def start_timestamp(n):
    result = get_now_timestamp() + (n * 300)
    # result = init_start_timestamp + (n * 300)  # 5min.
    return result


class WorkItemFactory(SQLAlchemyModelFactory):
    class Meta:
        model = WorkItem
        sqlalchemy_session_factory = session_factory
        sqlalchemy_session = None
        sqlalchemy_session_persistence = 'flush'

    task = factory.SubFactory(TaskFactory)
    start_timestamp = factory.Sequence(start_timestamp)
    end_timestamp = factory.LazyAttribute(lambda self: self.start_timestamp + 300)
