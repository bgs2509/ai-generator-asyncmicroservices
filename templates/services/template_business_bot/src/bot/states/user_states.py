"""User-related FSM states.

Define states for multi-step user interactions.

Usage:
    from src.bot.states.user_states import UserRegistration

    @router.message(UserRegistration.waiting_for_name)
    async def process_name(message: Message, state: FSMContext):
        await state.update_data(name=message.text)
        await state.set_state(UserRegistration.waiting_for_email)
"""
from aiogram.fsm.state import State, StatesGroup


class UserRegistration(StatesGroup):
    """States for user registration flow."""

    waiting_for_name = State()
    waiting_for_email = State()
    waiting_for_phone = State()
    confirming = State()


class UserProfile(StatesGroup):
    """States for profile editing flow."""

    editing_name = State()
    editing_email = State()
    editing_phone = State()
