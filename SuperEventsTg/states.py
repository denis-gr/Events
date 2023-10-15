from aiogram.fsm.state import StatesGroup, State

class AnswerGamePointStatesGroup(StatesGroup):
    current_event_id = State()
    game_id = State()
    gp_id = State()
    answer = State()
