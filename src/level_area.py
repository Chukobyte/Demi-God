import copy
from typing import Optional, List, Type

from crescent_api import GameProperties

from src.characters.enemy_definitions import EnemyDefinition
from src.items import (
    HealthRestoreItem,
    SignItem,
    EnergyDrainDecreaseItem,
    DamageDecreaseItem,
)


class LevelAreaType:
    INTRO = "intro"
    NORMAL = "normal"
    POWER_UP = "power_up"
    BOSS = "boss"
    END = "end"


class LevelSection:
    def __init__(self, enemy_defs: List[EnemyDefinition]):
        self.enemy_defs = enemy_defs
        self.index: Optional[int] = None


class LevelArea:
    """
    Area in a level separated by gates.  Can contain sections.
    """

    def __init__(
        self,
        area_type: str,
        width: int,
        sections: List[LevelSection] = None,
        item_types: List[Type] = None,
    ):
        self.area_type = area_type
        self.width = width
        if not sections:
            sections = []
        self.sections = sections
        for i, section in enumerate(sections):
            section.index = i
        if not item_types:
            item_types = []
        self.item_types = item_types
        self.is_completed = False

    def set_completed(self, is_completed: bool) -> None:
        self.is_completed = is_completed

    def is_section_last(self, section: LevelSection) -> bool:
        if self.sections:
            last_index = len(self.sections) - 1
            return self.sections[last_index] == section
        return False

    def copy(self) -> "LevelArea":
        return copy.deepcopy(self)


class LevelAreaDefinitions:
    DEF_MAP = {
        1: LevelArea(area_type=LevelAreaType.INTRO, width=260, item_types=[SignItem]),
        2: LevelArea(
            area_type=LevelAreaType.NORMAL,
            width=896,
            sections=[
                LevelSection(enemy_defs=[EnemyDefinition.RABBIT()]),
                LevelSection(
                    enemy_defs=[EnemyDefinition.RABBIT(), EnemyDefinition.JESTER()]
                ),
                LevelSection(
                    enemy_defs=[EnemyDefinition.RABBIT(), EnemyDefinition.JESTER()]
                ),
                LevelSection(
                    enemy_defs=[
                        EnemyDefinition.RABBIT(),
                        EnemyDefinition.JESTER(),
                    ]
                ),
                LevelSection(
                    enemy_defs=[
                        EnemyDefinition.RABBIT(),
                        EnemyDefinition.JESTER(),
                    ]
                ),
            ],
        ),
        3: LevelArea(
            area_type=LevelAreaType.POWER_UP,
            width=GameProperties().game_resolution.w,
            item_types=[EnergyDrainDecreaseItem, HealthRestoreItem, DamageDecreaseItem],
        ),
        4: LevelArea(
            area_type=LevelAreaType.NORMAL,
            width=896,
            sections=[
                LevelSection(enemy_defs=[EnemyDefinition.SNAKE()]),
                LevelSection(
                    enemy_defs=[
                        EnemyDefinition.RABBIT(),
                        EnemyDefinition.JESTER(),
                        EnemyDefinition.SNAKE(),
                    ]
                ),
                LevelSection(
                    enemy_defs=[
                        EnemyDefinition.RABBIT(),
                        EnemyDefinition.JESTER(),
                        EnemyDefinition.SNAKE(),
                    ]
                ),
                LevelSection(
                    enemy_defs=[
                        EnemyDefinition.RABBIT(),
                        EnemyDefinition.JESTER(),
                        EnemyDefinition.SNAKE(),
                        EnemyDefinition.CROW(),
                    ]
                ),
                LevelSection(
                    enemy_defs=[
                        EnemyDefinition.RABBIT(),
                        EnemyDefinition.JESTER(),
                        EnemyDefinition.SNAKE(),
                        EnemyDefinition.CROW(),
                    ]
                ),
            ],
        ),
        5: LevelArea(
            area_type=LevelAreaType.BOSS,
            width=GameProperties().game_resolution.w,
        ),
        6: LevelArea(
            area_type=LevelAreaType.END, width=GameProperties().game_resolution.w
        ),
    }

    @staticmethod
    def get_def(area_num: int) -> Optional[LevelArea]:
        return LevelAreaDefinitions.DEF_MAP.get(area_num, None).copy()

    @staticmethod
    def is_valid_area_index(index: int) -> bool:
        return index in LevelAreaDefinitions.DEF_MAP.keys()
