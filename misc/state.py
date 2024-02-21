from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    next_questions = State()
    next_answers = State()
