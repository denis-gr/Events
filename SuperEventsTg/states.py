from aiogram.fsm.state import StatesGroup, State

class AnswerGamePointStatesGroup(StatesGroup):
    game_id = State()
    gp_id = State()
    answer = State()
