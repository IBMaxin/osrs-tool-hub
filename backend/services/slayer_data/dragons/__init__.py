"""Dragon slayer task data."""

from .metal_dragons import METAL_DRAGONS_TASK_DATA
from .colored_dragons import COLORED_DRAGONS_TASK_DATA
from .wyverns import WYVERNS_TASK_DATA

# Combine all dragon task data
DRAGON_TASK_DATA = {
    **METAL_DRAGONS_TASK_DATA,
    **COLORED_DRAGONS_TASK_DATA,
    **WYVERNS_TASK_DATA,
}

__all__ = ["DRAGON_TASK_DATA"]
