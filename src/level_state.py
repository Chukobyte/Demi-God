from typing import Optional

from crescent_api import Rect2, ShaderInstance

from src.utils.task import co_suspend


class LevelState:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
            cls.boundary = Rect2(0, 0, 896, 144)
            cls.floor_y = 0.0
            cls.is_paused = False
            cls.screen_shader_instance: Optional[ShaderInstance] = None
        return cls._instance

    @staticmethod
    async def fade_transition(time: float, fade_out=True):
        try:
            level_state = LevelState()
            if fade_out:
                await co_suspend()
                LevelState().screen_shader_instance.set_float_param("brightness", 0.75)
                await co_suspend()
                LevelState().screen_shader_instance.set_float_param("brightness", 0.5)
                await co_suspend()
                LevelState().screen_shader_instance.set_float_param("brightness", 0.25)
                await co_suspend()
                LevelState().screen_shader_instance.set_float_param("brightness", 0.0)
            else:
                await co_suspend()
                LevelState().screen_shader_instance.set_float_param("brightness", 0.25)
                await co_suspend()
                LevelState().screen_shader_instance.set_float_param("brightness", 0.5)
                await co_suspend()
                LevelState().screen_shader_instance.set_float_param("brightness", 0.75)
                await co_suspend()
                LevelState().screen_shader_instance.set_float_param("brightness", 1.0)
        except GeneratorExit:
            pass
