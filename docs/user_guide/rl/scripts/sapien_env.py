import sapien.core as sapien

import gymnasium as gym
from gymnasium.utils import seeding


class SapienEnv(gym.Env):
    """Superclass for Sapien environments."""

    def __init__(self, control_freq, timestep):
        self.control_freq = control_freq  # alias: frame_skip in mujoco_py
        self.timestep = timestep

        self._scene = sapien.Scene()
        self._scene.set_timestep(timestep)

        self._build_world()
        self.viewer = None
        self.seed()

    def _build_world(self):
        raise NotImplementedError()

    def _setup_viewer(self):
        raise NotImplementedError()

    # ---------------------------------------------------------------------------- #
    # Override gym functions
    # ---------------------------------------------------------------------------- #
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def close(self):
        if self.viewer is not None:
            pass  # release viewer

    def render(self, mode='human'):
        if mode == 'human':
            if self.viewer is None:
                self._setup_viewer()
            self._scene.update_render()
            if not self.viewer.closed:
                self.viewer.render()
        else:
            raise NotImplementedError('Unsupported render mode {}.'.format(mode))

    # ---------------------------------------------------------------------------- #
    # Utilities
    # ---------------------------------------------------------------------------- #
    def get_actor(self, name):
        all_actors = self._scene.get_all_actors()
        actor = [x for x in all_actors if x.name == name]
        if len(actor) > 1:
            raise RuntimeError(f'Not a unique name for actor: {name}')
        elif len(actor) == 0:
            raise RuntimeError(f'Actor not found: {name}')
        return actor[0]

    def get_articulation(self, name):
        all_articulations = self._scene.get_all_articulations()
        articulation = [x for x in all_articulations if x.name == name]
        if len(articulation) > 1:
            raise RuntimeError(f'Not a unique name for articulation: {name}')
        elif len(articulation) == 0:
            raise RuntimeError(f'Articulation not found: {name}')
        return articulation[0]

    @property
    def dt(self):
        return self.timestep * self.control_freq
