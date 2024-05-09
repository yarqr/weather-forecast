from aiogram.fsm.state import State, StatesGroup


class CreateUserSG(StatesGroup):
    choose_language = State()
    main = State()
    settings = State()


class UpdateUserCitySG(StatesGroup):
    input_city = State()
    result = State()
