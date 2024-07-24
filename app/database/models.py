from sqlalchemy import BigInteger, ForeignKey, String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine =create_async_engine('sqlite+aiosqlite:///api_db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name = mapped_column(String(100))
    age = mapped_column(BigInteger)
    sex = mapped_column(String(10))
    fitness_goal = mapped_column(String(255))
    plans = relationship("Plan", back_populates="user")
    
class Plan(Base):
    __tablename__ = 'plans'
    id: Mapped[int] = mapped_column(primary_key=True)
    # не удаляется при удалении записи в User
    user_id = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    workout_plan_id = mapped_column(ForeignKey('workout_plans.id', ondelete='CASCADE'), nullable=False)
    nutrition_plan_id = mapped_column(ForeignKey('nutrition_plans.id', ondelete='CASCADE'), nullable=False)
    user = relationship("User", back_populates="plans")
    workout_plan = relationship("Workout_plan", back_populates="plans", cascade="all, delete-orphan", single_parent=True)
    nutrition_plan = relationship("Nutrition_plan", back_populates="plans", cascade="all, delete-orphan", single_parent=True)


class Workout_plan(Base):
    __tablename__ = 'workout_plans'
    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(String(255))
    user_id = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    plans = relationship("Plan", back_populates="workout_plan")
    
class Nutrition_plan(Base):
    __tablename__ = 'nutrition_plans'
    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(String(255))
    user_id = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    breakfast = mapped_column(String(255))
    lunch = mapped_column(String(255))
    dinner = mapped_column(String(255))
    snacks = mapped_column(String(255))
    plans = relationship("Plan", back_populates="nutrition_plan")
class Exercise(Base):
    __tablename__ = 'exercises'
    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(String(100))
    description = mapped_column(String(255))
    link = mapped_column(String(100))
    muscle = mapped_column(Integer, ForeignKey('muscles.id', ondelete='CASCADE'), nullable=False)
    sub_muscle = mapped_column(Integer, ForeignKey('muscles.id', ondelete='CASCADE'), nullable=True)
    restriction = mapped_column(String(100))
    for_begginers = mapped_column(String(100))

class WorkoutExercise(Base):
    __tablename__ = 'workout_exercises'
    id: Mapped[int] = mapped_column(primary_key=True)
    workout_plan_id = mapped_column(Integer, ForeignKey('workout_plans.id', ondelete='CASCADE'), nullable=False)
    exercise_id = mapped_column(Integer, ForeignKey('exercises.id', ondelete='CASCADE'), nullable=False)

class Muscle(Base):
    __tablename__ = 'muscles'
    id: Mapped[int] = mapped_column(primary_key=True)
    name = mapped_column(String(100))
    
    def __str__(self):
        return self.name

async def async_main():
    async with engine.begin() as conn:
        #await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        