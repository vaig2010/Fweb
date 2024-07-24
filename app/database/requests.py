from app.database.models import async_session
from app.database.models import (User, Plan, Exercise, Muscle,
                                    Workout_plan, Nutrition_plan)
from sqlalchemy import select, update, delete, insert
import random
async def set_user(user: User) -> None:
    async with async_session() as session:
        db_user = await session.scalar(select(User).where(User.tg_id == user.tg_id))
        
        if not db_user:
            session.add(user)
            await session.commit()
async def get_user(user_id) -> None:
    async with async_session() as session:
        db_user = await session.scalar(select(User).where(User.tg_id == user_id))
        return db_user
async def set_plan(plan) -> None:
    async with async_session() as session:
        db_user = await session.scalar(select(User).where(User.id == plan.user_id))
        if not db_user:
            return
        session.add(plan)
        await session.commit()
        await session.refresh(plan)

async def get_plan(user_id, T):
    async with async_session() as session:
        db_plan = await session.scalar(select(T).where(T.user_id == user_id))
        if not db_plan:
            return
        else:
            return db_plan
async def del_plan(plan) -> None:
    async with async_session() as session:
        await session.delete(plan)
        await session.commit()
async def del_user(user):
    async with async_session() as session:
        await session.delete(user)
        await session.commit()
async def get_all_muscles() -> list[Muscle]:
    async with async_session() as session:
        muscles = await session.scalars(select(Muscle.name))
        return muscles.all()

async def get_my_exes() -> list[Exercise]:
    async with async_session() as session:
        # test
        muscles_id = [14, 21, 7, 1, 8]
        exs = []
        for m in muscles_id:
            t = await session.scalars(select(Exercise).where(Exercise.muscle == m))
            exercises = t.all()
            if exercises:
                chosen_exercise = random.choice(exercises)
                exs.append(chosen_exercise)
        return exs