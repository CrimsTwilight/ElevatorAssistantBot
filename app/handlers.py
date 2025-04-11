import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


import app.keyboards as kb
from app.database.requests import add_user, show_number_of_users, get_all_users
from app.utils import calculate_productivity


router = Router()


class MyStates(StatesGroup):
    number_of_orders = State()
    number_of_points = State()
    number_of_hours = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer('Привет, для расчёта производительности нажми /stat')


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer('Когда-нибудь тут будет памятка!')


@router.message(Command('stat'))
async def cmd_stat(message: Message):
    await message.answer("Выберите действие:", reply_markup=kb.menu)


@router.message(Command('admin'))
async def cmd_admin(message: Message):
    if message.from_user.id == int(os.getenv('ADMIN')):
        await message.answer("Выберите действие:", reply_markup=kb.menu_admin)


@router.callback_query(F.data == 'action_1')
async def action_1(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Введите количество приказов:')
    await state.set_state(MyStates.number_of_orders)


@router.message(MyStates.number_of_orders)
async def number_of_orders(message: Message, state: FSMContext):
    if message.text.isdigit():
        number = int(message.text)
        await state.update_data(number_of_orders=number)
        await message.answer('Введите количество часов:')
        await state.set_state(MyStates.number_of_hours)
    else:
        await message.answer('Пожалуйста, введите корректное число.')


@router.callback_query(F.data == 'action_2')
async def action_2(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Введите количество баллов:')
    await state.set_state(MyStates.number_of_points)


@router.message(MyStates.number_of_points)
async def number_of_points(message: Message, state: FSMContext):
    if message.text.isdigit():
        number = int(message.text)
        await state.update_data(number_of_points=number)
        await message.answer('Введите количество часов:')
        await state.set_state(MyStates.number_of_hours)
    else:
        await message.answer('Пожалуйста, введите корректное число.')


@router.message(MyStates.number_of_hours)
async def number_of_hours(message: Message, state: FSMContext):
    if message.text.isdigit():
        number = int(message.text)
        await state.update_data(number_of_hours=number)
        data = await state.get_data()
        await message.answer(calculate_productivity(data))
        await state.clear()
    else:
        await message.answer('Пожалуйста, введите корректное число.')


@router.callback_query(F.data == 'number_of_users')
async def number_of_users(callback: CallbackQuery):
    await callback.answer()
    user_count = await show_number_of_users()
    await callback.message.answer(str(user_count))


@router.callback_query(F.data == 'list_of_users')
async def list_of_users(callback: CallbackQuery):
    await callback.answer()
    users = await get_all_users()
    text = "Список пользователей:\n"
    for user in users:
        text += (f"ID: {user.tg_id}, Имя: {user.full_name}, "
                 f"Username: @{user.username}\n")
    await callback.message.answer(text)
