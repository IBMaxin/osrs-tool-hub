"""Common slayer task data - frequently assigned tasks."""

from .demons import DEMONS_TASK_DATA
from .undead import UNDEAD_TASK_DATA
from .beasts import BEASTS_TASK_DATA
from .dragons_wyverns import DRAGONS_WYVERNS_TASK_DATA
from .slayer_tower import SLAYER_TOWER_TASK_DATA
from .catacombs import CATACOMBS_TASK_DATA
from .misc import MISC_TASK_DATA

# Combine all common task data
COMMON_TASK_DATA = {
    **DEMONS_TASK_DATA,
    **UNDEAD_TASK_DATA,
    **BEASTS_TASK_DATA,
    **DRAGONS_WYVERNS_TASK_DATA,
    **SLAYER_TOWER_TASK_DATA,
    **CATACOMBS_TASK_DATA,
    **MISC_TASK_DATA,
}

__all__ = ["COMMON_TASK_DATA"]
