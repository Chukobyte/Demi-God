from crescent_api import Vector2

from src.characters.enemy import Enemy
from src.utils.task import *


class EnemySnake(Enemy):
    def __init__(self, entity_id: int):
        super().__init__(entity_id)
        self._set_base_hp(1)
        self.destroy_on_touch = True
        self.physics_update_task = Task(coroutine=self._physics_update_task())

    # --- TASKS --- #
    async def _physics_update_task(self) -> None:
        try:
            player = self._find_player()
            move_speed = 30
            if player.position.x > self.position.x:
                move_dir = Vector2.RIGHT()
            else:
                self.anim_sprite.flip_h = True
                move_dir = Vector2.LEFT()
            while True:
                delta_time = self.get_full_time_dilation_with_physics_delta()
                self.position += move_dir * Vector2(
                    move_speed * delta_time, move_speed * delta_time
                )
                await co_suspend()
        except GeneratorExit:
            pass
