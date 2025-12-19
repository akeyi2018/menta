import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import cv2  # OpenCVを使用して動画を読み込む
import random
import socket
from common_proc import setup_socket, set_config
from loguru import logger
import os
import time
import numpy as np

# グローバル変数
quadric = None

def InitializeSphere(config_data):
    global sphere_model_list, quadric
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)

    # ディスプレイリストを作成
    sphere_model_list = glGenLists(1)
    glNewList(sphere_model_list, GL_COMPILE)
    gluSphere(quadric, 
              config_data["BALL_RADIUS"], 
              config_data["BALL_SLICES"], 
              config_data["BALL_STACKS"])
    glEndList()

# 球を描画する関数
def DrawSphere_k(position, radius, config_data):
    glPushMatrix()  # モデルビュー行列を保存
    glPushAttrib(GL_LIGHTING_BIT | GL_CURRENT_BIT)  # ライティングやカラーステートを保存
    glTranslated(position[0], position[1], position[2])  # 平行移動

    # ライティングの設定
    glEnable(GL_DEPTH_TEST)  # デプスバッファを使用
    glEnable(GL_LIGHTING)  # ライティングを有効化
    glEnable(GL_LIGHT0)  # 光源0を有効化
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(ball_color[0], ball_color[1], ball_color[2], 0.1)
    # glColor3f(ball_r, 0.0, 0.0)

    if not (limit_x_min <= position[0] <= limit_x_max and limit_y_min <= position[1] <= limit_y_max):
        # ディスプレイリストを呼び出し
        # glCallList(sphere_model_list)
        gluSphere(quadric, radius, config_data["BALL_SLICES"], config_data["BALL_STACKS"])
    
    glPopAttrib()  # 保存した状態を復元
    glPopMatrix()  # モデルビュー行列を復元


def SetMaterial():
     # 材質の設定
    material_diffuse = [ball_color[0], ball_color[1], ball_color[2], ball_color[3]]   # 拡散反射の色

    material_specular = [1.0, 1.0, 1.0, 0.1]  # 鏡面反射の色
    material_shininess = [30.0]  # 鏡面反射の強さ

      # 光源の位置を設定
    light_position = [0.0, 0, 0.0, 1.0]  # 光源の位置
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)  # 光源の位置を設定

    glMaterialfv(GL_FRONT, GL_DIFFUSE, material_diffuse)  # 拡散反射の色を設定
    glMaterialfv(GL_FRONT, GL_SPECULAR, material_specular)  # 鏡面反射の色を設定
    glMaterialfv(GL_FRONT, GL_SHININESS, material_shininess)  # 鏡面反射の強さを設定
    # glMaterialfv(GL_FRONT, GL_ALPHA, 0.3)

def rotate_positions(positions, angle_deg, axis="z", center=None):
    """
    positions: Nx3リストまたは配列
    angle_deg: 回転角度（度）
    axis: "x", "y", "z" のいずれか
    center: 回転中心 [x, y, z]（省略時は原点）
    """
    angle_rad = np.deg2rad(angle_deg)
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    if axis == "x":
        R = np.array([
            [1, 0,  0],
            [0, c, -s],
            [0, s,  c]
        ])
    elif axis == "y":
        R = np.array([
            [ c, 0, s],
            [ 0, 1, 0],
            [-s, 0, c]
        ])
    elif axis == "z":
        R = np.array([
            [c, -s, 0],
            [s,  c, 0],
            [0,  0, 1]
        ])
    else:
        raise ValueError("axis must be 'x', 'y', or 'z'")
    
    pos_np = np.array(positions)
    if center is not None:
        pos_np = pos_np - center
    pos_rot = pos_np @ R.T
    if center is not None:
        pos_rot = pos_rot + center
    return pos_rot.tolist()

def UpdateVisbleSpheres(postion, movement, x, y, z, config_data):
   
    # 座標計算
    trans_x = abs((config_data["BALL_AREA"]["X_MAX"] - config_data["BALL_AREA"]["X_MIN"]) / config_data["INTERVAL"]["X"])
    trans_z = abs((config_data["BALL_AREA"]["Z_MAX"] - config_data["BALL_AREA"]["Z_MIN"]) / config_data["INTERVAL"]["Z"])

    for i, p in enumerate(postion):
        p[0] += movement[0]
        if p[0] <= config_data["BALL_AREA"]["X_MIN"]:
            postion[i][0] = postion[i][0] + trans_x 
        elif p[0] >= config_data["BALL_AREA"]["X_MAX"]:
            postion[i][0] = postion[i][0] - trans_x 
        p[2] += movement[2]
        if p[2] <= config_data["BALL_AREA"]["Z_MIN"]:
            postion[i][2] = postion[i][2] + trans_z
        elif p[2] >= config_data["BALL_AREA"]["Z_MAX"]:
            postion[i][2] = postion[i][2] - trans_z
    
        # エリア中心で回転したい場合
    center = [
        (config_data["BALL_AREA"]["X_MAX"] + config_data["BALL_AREA"]["X_MIN"]) / 2,
        (config_data["BALL_AREA"]["Y_MAX"] + config_data["BALL_AREA"]["Y_MIN"]) / 2,
        (config_data["BALL_AREA"]["Z_MAX"] + config_data["BALL_AREA"]["Z_MIN"]) / 2
    ]

    postion = rotate_positions(postion, x, axis="x", center=center)
    postion = rotate_positions(postion, y, axis="y", center=center)
    postion = rotate_positions(postion, z, axis="z", center=center)

    return postion

# def UpdateVisbleSpheres(postion, movement, config_data):

#     # 座標計算
#     trans_x = abs((config_data["BALL_AREA"]["X_MAX"] - config_data["BALL_AREA"]["X_MIN"]) / config_data["INTERVAL"]["X"])
#     # trans_y = abs((BALL_AREA_Y_MAX - BALL_AREA_Y_MIN) / config_data["INTERVAL"]["Y"])
#     trans_z = abs((config_data["BALL_AREA"]["Z_MAX"] - config_data["BALL_AREA"]["Z_MIN"]) / config_data["INTERVAL"]["Z"])

#     for i, p in enumerate(postion):
#         p[0] += movement[0]
#         if p[0] <= config_data["BALL_AREA"]["X_MIN"]:
#             postion[i][0] = postion[i][0] + trans_x
#         elif p[0] >= config_data["BALL_AREA"]["X_MAX"]:
#             postion[i][0] = postion[i][0] - trans_x
#         p[2] += movement[2]
#         if p[2] <= config_data["BALL_AREA"]["Z_MIN"]:
#             postion[i][2] = postion[i][2] + trans_z
#         elif p[2] >= config_data["BALL_AREA"]["Z_MAX"]:
#             postion[i][2] = postion[i][2] - trans_z

#     return postion

def initial_env(config_data):
    pygame.display.set_mode((config_data["WINDOW_SIZE"]["WIDTH"], 
                             config_data["WINDOW_SIZE"]["HEIGHT"]), 
                             DOUBLEBUF | OPENGL)
    # pygame.display.set_mode((0, 0), DOUBLEBUF | OPENGL | pygame.FULLSCREEN)
    pygame.display.set_caption("球体色可変")

    # OpenGLの初期化
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    # glEnable(GL_BLEND)  # ブレンディングを有効化
    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # ブレンディングの設定
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 
                   (config_data["WINDOW_SIZE"]["WIDTH"] / config_data["WINDOW_SIZE"]["HEIGHT"]), 
                   0.1, 
                   50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def movie_window_normalize(value, input_min, input_max, output_min, output_max):
    """
    入力値を指定された範囲に正規化する関数
    """
    # 線形変換を使用して値を正規化
    normalized_value = ((value - input_min) / (input_max - input_min)) * (output_max - output_min) + output_min
    return normalized_value

def load_socket(config_data):
    udp_ip = config_data["HOST"]["IP"]
    udp_port_01 = config_data["HOST"]["PORT_01"]
    udp_port_02 = config_data["HOST"]["PORT_02"]
    udp_port_03 = config_data["HOST"]["PORT_03"]

    # socket
    sock = setup_socket(udp_ip,udp_port_01)
    sock.settimeout(0.1) # タイムアウトを設定（例: 0.1秒）

    sock2 = setup_socket(udp_ip,udp_port_02)

    sock3 = setup_socket(udp_ip,udp_port_03)

    return sock, sock2, sock3

def get_limit_area(config_data):

    global limit_x_min, limit_x_max, limit_y_min, limit_y_max

    # BALL_AREAの範囲を取得
    x_min = config_data["BALL_AREA"]["X_MIN"]
    x_max = config_data["BALL_AREA"]["X_MAX"]
    y_min = config_data["BALL_AREA"]["Y_MIN"]
    y_max = config_data["BALL_AREA"]["Y_MAX"]

    # 空き率
    limit_x = config_data["BALL_AREA"]["LIMIT_X"]
    limit_y = config_data["BALL_AREA"]["LIMIT_Y"]

    # LIMIT_AREAの範囲を取得
    limit_x_min = movie_window_normalize((1 - limit_x) / 2, 0, 1, x_min, x_max)
    limit_x_max = movie_window_normalize(1 - (1 - limit_x) / 2, 0, 1, x_min, x_max)

    limit_y_min = movie_window_normalize((1 - limit_y) / 2, 0, 1, y_min, y_max)
    limit_y_max = movie_window_normalize(1 - (1 - limit_y) / 2, 0, 1, y_min, y_max)

def change_dot_num(config_data):
    
    sphere_positions.clear()

    for _ in range(ball_count):
        px = random.uniform(config_data["BALL_AREA"]["X_MIN"], config_data["BALL_AREA"]["X_MAX"])
        py = random.uniform(config_data["BALL_AREA"]["Y_MIN"], config_data["BALL_AREA"]["Y_MAX"])
        pz = random.uniform(config_data["BALL_AREA"]["Z_MIN"], config_data["BALL_AREA"]["Z_MAX"])
        sphere_positions.append([px,py,pz])

def main():
    pygame.init()

    global sphere_positions
    global view_center, view_position, ball_r, ball_g, ball_b, ball_color, light_pos_y, ball_count, ball_radius
    
    # 設定情報
    config_data = set_config()
    
    ball_view_flg = config_data["BALL_VIEW"]
    light_pos_y = config_data["LIGHT_POSITION_Y"]

    win_w, win_h = config_data["WINDOW_SIZE"]["WIDTH"], config_data["WINDOW_SIZE"]["HEIGHT"]
    radius_min, radius_max = config_data["RADIUS_MIN"], config_data["RADIUS_MAX"]

    ball_count = config_data["BALL_COUNT"]
    view_center = config_data["view_center"]
    view_position = config_data["view_position"]

    move_speed = config_data["MOVE_SPEED"]
    roll_speed = config_data["ROLL_SPEED"]

    ct = 0

    get_limit_area(config_data)

    # socket
    sock, sock2, sock3 = load_socket(config_data)

    initial_env(config_data)

    InitializeSphere(config_data)

    # 球の位置を初期化
    sphere_positions = []

    for _ in range(ball_count):
        px = random.uniform(config_data["BALL_AREA"]["X_MIN"], config_data["BALL_AREA"]["X_MAX"])
        py = random.uniform(config_data["BALL_AREA"]["Y_MIN"], config_data["BALL_AREA"]["Y_MAX"])
        pz = random.uniform(config_data["BALL_AREA"]["Z_MIN"], config_data["BALL_AREA"]["Z_MAX"])
        sphere_positions.append([px,py,pz])

    pre_ball_count = ball_count

    prev_x = prev_y = None  # 前回の座標を保持
    movement_fr = 0.0
    movement_x = 0.0
    pre_roll_x = pre_roll_y = pre_roll_z = None
    roll_x = roll_y = roll_z = 0.0

    logger.info("初期化完了")

    start_time = time.time()  # 再生開始時刻

    while True:

        # 現在の再生時間（秒）
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        # UDPデータ受信部分
        try:
            data, _ = sock.recvfrom(256)
            x, y, roll_x, roll_y, roll_z = map(float, data.decode().replace('\x00','').split())

            if x != prev_x or y != prev_y:
                movement_x = x / (100 * 5)
                movement_fr = y / (100 * 5)
                prev_x, prev_y = x, y

            if roll_x != pre_roll_x or roll_y != pre_roll_y or roll_z != pre_roll_z:
                pre_roll_x, pre_roll_y, pre_roll_z = roll_x, roll_y, roll_z


            movement = [movement_x * roll_speed, 0.0, movement_fr * move_speed]

            data2, _ = sock2.recvfrom(256)
            ball_r, ball_g, ball_b, ball_a = map(float, data2.decode().split())

            ball_color = [ball_r, ball_g, ball_b, ball_a]
            # logger.info(f'sock2 data: {ball_color}')

            # ball_color = [1.0, 1.0, 1.0, 0.1]

            data3, _ = sock3.recvfrom(256)
            radius, ball_count = map(int, data3.decode().replace('\x00','').split())

            if ct == 0:
                logger.info(f'ball: {data2}')
                ct = 1

            ball_radius = movie_window_normalize(
                radius,
                radius_min,
                radius_max,
                0.01,
                0.25
            )

            if pre_ball_count != ball_count:
                change_dot_num(config_data)
                pre_ball_count = ball_count
                

        except socket.timeout:
            pass
        except ValueError:
            print("Invalid data received")

        # 球の位置更新
        sphere_positions = UpdateVisbleSpheres(
            sphere_positions, 
            movement,
            roll_x,
            roll_y,
            roll_z, 
            config_data)


        # 描画
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # 3D球描画
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (win_w / win_h), 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -4.0)
        SetMaterial()

        if ball_view_flg:
            for p in sphere_positions:
                DrawSphere_k(p, ball_radius, config_data)

        pygame.display.flip()

if __name__ == "__main__":
    logger.add("error.log", rotation="1 MB", level="DEBUG")
    main()