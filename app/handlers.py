from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import as_list, as_marked_section, Bold

import sqlite3


import app.database.requests as rq
from app.database.models import async_session, User, Plan, Workout_plan, Nutrition_plan
from app.keyboards import get_keyboard, kb_main, kb_registration
router = Router()

class Form(StatesGroup):
    name = State()
    age = State()
    sex = State()
    goal = State()

TRAINING_GOALS = ("Увеличение силы и мышечной массы", "Снижение веса", "Рельефное тело без набора массы", "Поддержание формы")

@router.message(StateFilter(None), F.text.lower() == "регистрация")
@router.message(StateFilter(None), Command('start', 'register'))
async def cmd_start(message: Message, state: FSMContext):
    tg_id = await rq.get_user(message.from_user.id)
    if tg_id:
        await message.answer("Вы уже зарегистрированы")
    else:
        await state.set_state(Form.name)
        await message.answer("Привет! Давайте начнем регистрацию. Как вас зовут?", reply_markup=kb_registration)
@router.message(StateFilter('*'),F.text.lower() == "отмена")
@router.message(StateFilter('*'),Command('cancel'))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer('Регистрация отменена.')
@router.message(Form.name, F.text)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("Сколько вам лет?", reply_markup=kb_registration)
@router.message(Form.name)
async def process_name(message: Message, state: FSMContext):
    await message.answer("Вы не ввели имя. Попробуйте ещё раз.")
@router.message(Form.age, F.text)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer(
        "Ваш пол (М/Ж)?", 
        reply_markup=get_keyboard(
            "М",
            "Ж",
            "Отмена",
            placeholder="Введите пол",
            sizes=(2,1)
        )
    )
    await state.set_state(Form.sex)
@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    await message.answer("Вы не ввели возраст. Попробуйте ещё раз.")
@router.message(Form.sex, F.text)
async def process_sex(message: Message, state: FSMContext):
    data = await state.update_data(sex=message.text)
    
    if data['sex'].upper() not in ('М', 'Ж'):
        await message.answer("Вы ввели некорректное значение. Попробуйте ещё раз")
        await message.answer(data['sex'].upper())
        return
    numerated_goal_list = enumerate(TRAINING_GOALS, 1)
    # Дописать выбор цели по кнопкам 
    await message.answer(
        "Какие у вас цели по тренировкам?\n" + "\n".join(f"{i}. {goal}" for i, goal in numerated_goal_list),
        reply_markup=get_keyboard(
            "1",
            "2",
            "3",
            "4",
            "Отмена",
            placeholder="Введите цель",
            sizes=(2,2)
        )
    )
    await state.set_state(Form.goal)
@router.message(Form.sex)
async def process_sex(message: Message, state: FSMContext):
    await message.answer("Вы не ввели пол. Попробуйте ещё раз")
@router.message(Form.goal, F.text)
async def process_goal(message: Message, state: FSMContext):
    data = await state.update_data(goal=message.text)
    if data["goal"] not in tuple(map(str,range(1,5))):
        await message.answer("Вы ввели некорректное значение. Попробуйте ещё раз")
        return
    data['goal'] = TRAINING_GOALS[int(data['goal']) - 1]
    # Сохранение данных пользователя в базе данных
    user = User(
        tg_id=message.from_user.id,
        name=data['name'],
        age=data['age'],
        sex=data['sex'],
        fitness_goal=data['goal']
    )
    await rq.set_user(user)

    await state.clear()
    text = as_list("Регистрация завершена✅ .",
                   as_marked_section(
                   Bold("Ваша анкета:"),
                   f"Имя: {data['name']}",
                   f"Возраст: {data['age']}",
                   f"Пол: {data['sex']}",
                   f"Цель: {data['goal']}",
                   marker='— ')
                   )
    await message.answer(text.as_html(), reply_markup=kb_main)
@router.message(Form.goal)
async def process_goal(message: Message, state: FSMContext):
    await message.answer("Вы не ввели цель. Попробуйте ещё раз")

@router.message(F.text.lower() == "создать план")
@router.message(Command('set_plan'))
async def set_plan(message: Message):
    # Генерация персонализированных планов
    user = await rq.get_user(message.from_user.id)
    if user is not None:
        check_plan = await rq.get_plan(user.id, T=Plan)
        if check_plan is not None:
            await message.answer("Вы уже установили план. Нажмите показать план")
            return
        workout_plan = Workout_plan(name="Тренировка для цели: \n" + user.fitness_goal, user_id=user.id)
        await rq.set_plan(workout_plan)
        nutrition_plan = Nutrition_plan(name="Питание для цели: \n" + user.fitness_goal, user_id=user.id)
        nutrition_plan.breakfast = "Завтрак: Овсянка с ягодами, медом и орехами. Яичница из 3-4 яиц. Авокадо"
        nutrition_plan.lunch = "Обед: Куриная грудка или рыба (лосось, тунец). Овощи на пару (брокколи, шпинат, морковь)"
        nutrition_plan.dinner = "Ужин: Говядина или индейка. Картофельное пюре. Овощи (спаржа, зеленые бобы)"
        nutrition_plan.snacks = "Перекусы: Греческий йогурт с медом и орехами. Фрукты (банан, яблоко, ягоды). Творог"
        await rq.set_plan(nutrition_plan)
        # Сохранение плана в базе данных
        plan = Plan(user_id=user.id, workout_plan_id=workout_plan.id, nutrition_plan_id=nutrition_plan.id)
        await rq.set_plan(plan)
        await message.answer("План установлен. Нажмите показать план")
    else:
        await message.answer("Вы еще не зарегистрированы. Введите /register.")

@router.message(F.text.lower() == "показать план")
@router.message(Command('get_plan'))
async def get_plan(message: Message):
    user = await rq.get_user(message.from_user.id)
    plan = await rq.get_plan(user.id, Plan)
    if plan is not None:
        await message.answer("Временно не работает. Нажмите план тренировок или план питания")
    else:
        await message.answer("Вы еще не установили план.")
        

@router.message(F.text.lower() == "план тренировок")
@router.message(Command('get_workout_plan'))
async def get_plan(message: Message):
    user = await rq.get_user(message.from_user.id)
    plan = await rq.get_plan(user.id, Workout_plan)
    if plan is not None:
        # Отправка планов пользователю
        my_exs = await rq.get_my_exes()
        text = as_list(plan.name+"\n", as_marked_section(
                   Bold("Список упражнений: "),
                   *[exercise.name for exercise in my_exs],
                   marker='— ')
                   )
        # Отправка планов пользователю
        await message.answer(text.as_html())
    else:
        await message.answer("Вы еще не установили план.")
        
@router.message(F.text.lower() == "план питания")
@router.message(Command('get_nutrition_plan'))
async def get_plan(message: Message):
    user = await rq.get_user(message.from_user.id)
    plan = await rq.get_plan(user.id, Nutrition_plan)
    if plan is not None:
        my_nuts = (plan.breakfast, plan.lunch, plan.dinner, plan.snacks)
        text = as_list(plan.name+"\n", as_marked_section(
                   Bold("График питания: "),
                   *my_nuts,
                   marker='— ')
                   )
        # Отправка планов пользователю
        await message.answer(text.as_html())
    else:
        await message.answer("Вы еще не установили план.")
@router.message(F.text.lower() == "удалить план")
@router.message(Command('delete_plan'))
async def delete_plan(message: Message):
    user = await rq.get_user(message.from_user.id)
    if user is None:
        await message.answer("Вы еще не зарегистрированы.")
        return
    try:
        plan = await rq.get_plan(user.id, Plan)
        await rq.del_plan(plan)
        await message.answer("Вы удалили план.")
    except Exception as e:
        print(e)
        await message.answer("Вы еще не установили план.")
@router.message(F.text.lower() == "удалить инфу о себе")
@router.message(Command('delete_user'))
async def delete_plan(message: Message):
    user = await rq.get_user(message.from_user.id)
    if user is None:
        await message.answer("Вы еще не зарегистрированы.")
        return
    await rq.del_user(user)
    await message.answer("Вы удалили себя из системы.")
    
@router.message(Command('all_muscles'))
async def all_muscles(message: Message):
    all_muscles = await rq.get_all_muscles()
    await message.answer(str(all_muscles))
