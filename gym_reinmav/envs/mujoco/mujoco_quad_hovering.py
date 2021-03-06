import numpy as np
import os

from gym_reinmav.envs.mujoco import MujocoQuadEnv


class MujocoQuadHoveringEnv(MujocoQuadEnv):
    def __init__(self):
        super(MujocoQuadHoveringEnv, self).__init__(xml_name="quadrotor_hovering.xml")

    def step(self, a):
        self.do_simulation(self.clip_action(a), self.frame_skip)
        ob = self._get_obs()

        alive_bonus = 100
        reward = - np.sum(np.square(ob[0:3] - np.array([0.0, 0, 1.0]))) * 10 \
                 - np.sum(np.square(ob[7:] - np.zeros(6))) * 0.1 \
                 - np.sum(np.square(a)) \
                 + np.sum(a) * 0.1 \
                 + alive_bonus

        notdone = np.isfinite(ob).all() \
                  and ob[2] > 0.3 \
                  and abs(ob[0]) < 2.0 \
                  and abs(ob[1]) < 2.0

        done = not notdone
        return ob, reward, done, {}
