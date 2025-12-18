"""Inline keyboard builders.

Provides factory functions for creating inline keyboards.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_confirm_keyboard(
    confirm_text: str = "Confirm",
    cancel_text: str = "Cancel",
    confirm_callback: str = "confirm",
    cancel_callback: str = "cancel",
) -> InlineKeyboardMarkup:
    """Create a confirmation keyboard with Confirm/Cancel buttons.

    Args:
        confirm_text: Text for confirm button
        cancel_text: Text for cancel button
        confirm_callback: Callback data for confirm action
        cancel_callback: Callback data for cancel action

    Returns:
        InlineKeyboardMarkup with two buttons
    """
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=confirm_text, callback_data=confirm_callback),
        InlineKeyboardButton(text=cancel_text, callback_data=cancel_callback),
    )
    return builder.as_markup()


def get_pagination_keyboard(
    current_page: int,
    total_pages: int,
    callback_prefix: str = "page",
) -> InlineKeyboardMarkup:
    """Create a pagination keyboard.

    Args:
        current_page: Current page number (1-indexed)
        total_pages: Total number of pages
        callback_prefix: Prefix for callback data

    Returns:
        InlineKeyboardMarkup with navigation buttons
    """
    builder = InlineKeyboardBuilder()
    buttons = []

    if current_page > 1:
        buttons.append(
            InlineKeyboardButton(
                text="<< First",
                callback_data=f"{callback_prefix}:1",
            )
        )
        buttons.append(
            InlineKeyboardButton(
                text="< Prev",
                callback_data=f"{callback_prefix}:{current_page - 1}",
            )
        )

    buttons.append(
        InlineKeyboardButton(
            text=f"{current_page}/{total_pages}",
            callback_data="noop",
        )
    )

    if current_page < total_pages:
        buttons.append(
            InlineKeyboardButton(
                text="Next >",
                callback_data=f"{callback_prefix}:{current_page + 1}",
            )
        )
        buttons.append(
            InlineKeyboardButton(
                text="Last >>",
                callback_data=f"{callback_prefix}:{total_pages}",
            )
        )

    builder.row(*buttons)
    return builder.as_markup()
