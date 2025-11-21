import sys
from panda3d.core import loadPrcFile
loadPrcFile('conf.prc')

from direct.showbase.ShowBase import ShowBase
from loguru import logger
from math import sin, cos, radians
import os 

class MyGame(ShowBase):
    def __init__(self):
        super().__init__(self)

        self.disable_mouse()
        self.accept("escape", sys.exit)

        # カメラ視点
        self.cam.setPos(0, -5, 0)

        self.scale = 1.0

        self.earth_pos = 0

        # earth 3Dモデルをロード
        self.model_earth = self.loader.loadModel(
            "earth.glb")

        self.model_earth.setPos(0, 0, 0)
        self.model_earth.setHpr(84, 99, -76)
        self.model_earth.setScale(self.scale, self.scale, self.scale)
        # シーンに追加
        self.model_earth.reparentTo(self.render)
        
        self.model_moon = self.loader.loadModel("moon.glb")
        self.moon_scale = self.scale / 6
        self.model_moon.setPos(-2, 2, 0)
        self.model_moon.setScale(self.moon_scale, 
                                 self.moon_scale,
                                 self.moon_scale)
        self.model_moon.reparentTo(self.render)

        self.x = 0
        self.direction = 1

        self.speed = 15
        self.moon_sp = 1.5
        self.angle = 2
        self.y = 5

        self.ct = 0

        logger.info(f'finish load model.')

        self.accept('j', self.k_j)
        self.accept('k', self.k_k)

        self.task_mgr.add(self.update, 'update_task')

    def k_k(self):
        self.earth_pos = 1

        hpr = self.model_earth.getHpr()

        logger.info(f'hpr: {hpr}')
        logger.info(f'hpr: {hpr[0]}')

        self.model_earth.setHpr(hpr[0] + self.earth_pos, 
                                hpr[1] , 
                                hpr[2] + self.earth_pos)

    def k_j(self):
        self.earth_pos = 1

        hpr = self.model_earth.getHpr()

        logger.info(f'hpr: {hpr}')
        logger.info(f'hpr: {hpr[0]}')

        self.model_earth.setHpr(hpr[0] + self.earth_pos, 
                                hpr[1] , 
                                hpr[2] - self.earth_pos)
    

    def update(self, task):
        dt = __builtins__.globalClock.getDt()

        # モデルの重心で回転        
        # self.model.setHpr(self.angle, 0, 0)
        # self.model_earth.setH(self.angle)

        # モデルが区間座標の移動
        self.model_moon.setPos(cos(self.x)*2, sin(self.x)*2, 0)

        hpr = self.model_earth.getHpr()
        # new_pitch_x = hpr[0] + cos(self.angle) * dt * 10
        # new_pitch_y = hpr[1] + sin(self.angle) * dt * 10

        new_pitch_x = hpr[0] + dt * 10

        self.model_earth.setHpr(new_pitch_x, hpr[1], hpr[2])

        # logger.info(f'rotate: {hpr} ')
        
        # self.model_earth.lookAt(self.model_moon, 99.0, 0)
        hpr_m = self.model_moon.getHpr()
        self.model_moon.setHpr(hpr_m[0] + dt* 100, hpr_m[1], hpr_m[2])
        

        # 角度変動
        self.angle += 1

        if self.angle >= 3600:
            self.angle = 0

        # if self.angle % 30 == 0:
        #     logger.info(f' angle: { self.angle}')

        self.x += self.moon_sp * dt

       
        return task.cont

if __name__ == '__main__':
    game = MyGame()

    # print(__builtins__.base.camera)
    game.run()
