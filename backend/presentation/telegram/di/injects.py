from typing import Callable, Coroutine, TypeVar

from dishka.integrations.aiogram import CONTAINER_NAME
from dishka.integrations.base import wrap_injection

T = TypeVar("T")


def inject_getter(
    func: Callable[..., Coroutine[None, None, T]],
) -> T:
    return wrap_injection(  # type: ignore[return-value]
        func=func,
        container_getter=lambda _, p: p[CONTAINER_NAME],
        is_async=True,
    )
