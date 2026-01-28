"""Slayer task definitions by master with comprehensive OSRS Wiki data."""

from .nieve import get_nieve_tasks
from .duradel import get_duradel_tasks
from .konar import get_konar_tasks
from .misc_masters import (
    get_turael_tasks,
    get_spria_tasks,
    get_mazchna_tasks,
    get_vannaka_tasks,
    get_chaeldar_tasks,
    get_tasks_by_master,
)

__all__ = [
    "get_nieve_tasks",
    "get_duradel_tasks",
    "get_konar_tasks",
    "get_turael_tasks",
    "get_spria_tasks",
    "get_mazchna_tasks",
    "get_vannaka_tasks",
    "get_chaeldar_tasks",
    "get_tasks_by_master",
]
