"""Slayer task data module - combines all task data sources."""

from .common import COMMON_TASK_DATA
from .demons import DEMON_TASK_DATA
from .dragons import DRAGON_TASK_DATA
from .special import SPECIAL_TASK_DATA

# Combine all task data into single dictionary
SLAYER_TASK_DATA = {
    **COMMON_TASK_DATA,
    **DEMON_TASK_DATA,
    **DRAGON_TASK_DATA,
    **SPECIAL_TASK_DATA,
}
