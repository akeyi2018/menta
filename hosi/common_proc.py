import pygame
import socket
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math
from socket import gethostname
import importlib
import json
import argparse

# configファイル
def set_config():

    # argparseで引数を定義
    parser = argparse.ArgumentParser(description="JSONファイルを読み込むスクリプト")
    parser.add_argument("config", help="設定ファイル (JSON) のパス")
    args = parser.parse_args()

    # 引数で指定されたJSONファイルを読み込む
    try:
        with open(args.config, "r", encoding="utf-8") as f:
            config_data = json.load(f)
        # logger.info(config_data)
    except FileNotFoundError:
        print(f"エラー: ファイル '{args.config}' が見つかりません。")
    except json.JSONDecodeError:
        print(f"エラー: ファイル '{args.config}' のフォーマットが正しくありません。")
    
    return config_data

# ソケットの設定
def setup_socket(ip="127.0.0.1",port=5052):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDPソケットを作成
    s.bind((ip, port))  # IPとポートにバインド
    return s

def dynamic_import(module_name):
    try:
        # モジュールをインポート
        module = importlib.import_module(module_name)
        return module
    except ModuleNotFoundError:
        print(f"モジュール '{module_name}' が見つかりません。")
        return None
    
def joystick_initial(num=0):
    joystick = None
    # ジョイスティックの初期化
    pygame.joystick.init()
    # ジョイスティックが接続されているか確認
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(num)
        joystick.init()
        # print("Joystick Name: ", joystick.get_name())
    else:
        print("No joystick connected.")
        # pygame.quit()
        # sys.exit()
    return joystick
        
def set_display():
    host_name = gethostname()
    if host_name == "JPMH007648":
        w,h = (1200, 800)
    else:
        w,h = (10000, 1800)

    return w,h

def GenerateRandomColor():
    """ランダムな色を生成"""
    config_data = set_config()
    if config_data["GENERAL_RANDOM_COLOR"]:
        r = random.uniform(0.0, 1.0)  # 赤成分
        g = random.uniform(0.0, 1.0)  # 緑成分
        b = random.uniform(0.0, 1.0)  # 青成分
    else:
        r, g, b, _ = config_data["BALL_COLOR"]

    return [r, g, b]  # RGBA形式で返す

def calculate_view_angles(camera_pos, target_pos):
    """カメラの位置と注視点からYawとPitch角を計算"""
    camera_x, camera_y, camera_z = camera_pos
    target_x, target_y, target_z = target_pos

    # 注視点に向かうベクトルを計算
    direction_x = target_x - camera_x
    direction_y = target_y - camera_y
    direction_z = target_z - camera_z

    # 水平面での角度を計算
    horizontal_distance = math.sqrt(direction_x ** 2 + direction_z ** 2)
    yaw = math.atan2(direction_z, direction_x)  # Yaw角（水平回転）

    # 垂直方向の角度を計算
    pitch = math.atan2(direction_y, horizontal_distance)  # Pitch角（上下回転）
    return yaw, pitch

def convert_camera_y(a, CAMERA_Y_MIN, CAMERA_Y_MAX):
    """ジョイスティックの値をカメラのY軸範囲に変換"""
    normalized_a = (a + 1) / 2  # Aの正規化
    b_value = CAMERA_Y_MIN + (normalized_a * CAMERA_Y_MAX)  # Bの値に変換
    return b_value

def convert_camera_x(a, CAMERA_X_MIN, CAMERA_X_MAX):
    """ジョイスティックの値をカメラのX軸範囲に変換"""
    normalized_a = (a + 1) / 2  # Aの正規化
    b_value = CAMERA_X_MIN + (normalized_a * (CAMERA_X_MAX - CAMERA_X_MIN))  # Bの値に変換
    return b_value
