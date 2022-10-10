###やりたいこと
###ヘルプ画面表示(操作方法,NGSLについて)
###単語一覧表示
###ボスカットイン追加


from re import L
from tkinter import font
import pygame
from pygame.locals import *
import sys
import time
import random
import os

#### ↓↓↓↓初期化↓↓↓↓ ####

INF = 1<<28
WIDTH = 1500
HEIGHT = 900
FONT_PATH = "jkmarugo\JK-Maru-Gothic-M.otf"
JPN_PATH = ".\japanese.txt"
EN_PATH = ".\english.txt"
DIRECTON_KEY = [K_UP, K_RIGHT, K_DOWN, K_LEFT]
MAXIMUM_HP = 10
TIME_LIMIT = 10
MISS_TIME = 1
COMBO_TIME = 2
ATTACK_TIME = 0.1
QUESTION_NUM = 50
LAST_STAGE = 56

#可変グローバル
NOW_STAGE = 1
NOW_TIME = 60
LIFE = 3
BOSS_FLG = True
USER = ""
PASS = ""
DATA = []

#場面
SCENE_START = 0
SCENE_MENU = 1
SCENE_GAME = 2
SCENE_FAILED = 3
SCENE_CLEAR = 4
SCENE_PRACTICE = 5
SCENE_REGISTER = 6
SCENE_LOGIN = 7
SCENE_HELP = 8
SCENE_LIST = 9

#pygameの初期化
pygame.init()
SURFACE = pygame.display.set_mode((WIDTH, HEIGHT)) #ウィンドウ作成((w, h), FULLSCREEN)
pygame.display.set_caption("英語ゲーム") #タイトルセット
pygame.mixer.init(frequency = 44100)    # 初期設定

#### ↑↑↑↑初期化↑↑↑↑ ####

#### ↓↓↓↓クラス↓↓↓↓ ####

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.color)
        self.active = False

    def handle_event(self, event):

        ret = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    pass
                    #self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                    ret = True
                # Re-render the text.
                self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)
                print(self.text, event.key)
        
        return ret
    
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

#### ↑↑↑↑クラス↑↑↑↑ ####


#### ↓↓↓↓関数宣言↓↓↓↓ ####

#テキストセット(ボタン用)
def set_button_font(button, text, font_path, rgb):

    ok = 0
    ng = 100
    
    #ボタンサイズ丁度にテキストサイズを合わせる(Binary Search)
    while (ng - ok) > 1:
        
        mid = (ok + ng) // 2

        font_config = pygame.font.Font(font_path, mid)
        font_w, font_h = font_config.size(text)

        if font_w <= button.width and font_h <= button.height:
             ok = mid
        else:
             ng = mid

    return pygame.font.Font(font_path, ok).render(text, True, rgb), (button.left, button.top)

#ウィンドウ閉じ
def press_quit_mouse(event):
    if event.type == QUIT:
        pygame.quit()
        sys.exit()

#マウスで押されたかどうか
def judge_mouse_button(event, button):

    if event.type == pygame.MOUSEBUTTONDOWN:
        if button.collidepoint(event.pos):
            return True

    return False

#ファイル存在確認
def judge_register(path):
    if not os.path.isfile(path):
        return True
    else:
        return False

#ログイン出来るかどうか
def judge_login(path, password):
    if os.path.isfile(path):
        data = file_read(path)
        if data[0] == password:
            return True
    
    return False

#テキストファイル読み込み
def file_read(path):
    text_list = []

    with open(path, 'r', encoding='utf-8') as f:
        for s_line in f:
            s_line = s_line.strip('\n')
            text_list.append(s_line)

    return text_list

#ユーザー登録
def file_user_write(boxes):

    text = []
    text.append(boxes[1].text+"\n")
    for i in range(56):
        text.append(str(INF)+"\n")

    try:
        with open("./user/" + boxes[0].text + ".txt", mode='w') as f:
            f.writelines(text)
            return True
    except FileExistsError:
        return False

def calc_damage(combo_num):

    return 2 + (combo_num * 0.2)

#正誤判定
def judge(select_idx, ans_idx, hp, now_combo):
    
    if select_idx == ans_idx:
        hoge = pygame.mixer.Sound("./msc/ok.wav")
        pygame.mixer.set_reserved(1)
        music1 =  pygame.mixer.Channel(1)
        music1.play(hoge)
        music1.set_volume(1)
    
        print("ok")
        return True, hp - calc_damage(now_combo), time.time(), time.time() + COMBO_TIME, now_combo + 1 #isShuffle, hp, miss_time, combo_time, combo_cnt
    else:
        #effect_music = pygame.mixer.music.load("./msc/ng.mp3")     # 音楽ファイルの読み込み
        #effect_music.play(1)              # 音楽の再生回数(1回)
        hoge = pygame.mixer.Sound("./msc/ng.wav")
        pygame.mixer.set_reserved(1)
        music1 =  pygame.mixer.Channel(1)
        music1.play(hoge)
        music1.set_volume(1)

        print("ng")
        return False, min(hp + 2, MAXIMUM_HP), time.time() + MISS_TIME, time.time(), 0 #isShuffle, hp, miss_time, combo_time, combo_cnt

#### ↑↑↑↑関数宣言↑↑↑↑ ####

##### ↓↓↓画面切り替え↓↓↓  ##### 

def start_loop():

    global USER
    global PASS
    global DATA

    USER = ""
    PASS = ""
    DATA = []

    SURFACE.fill((0, 0, 0))
    pic = pygame.image.load("./pic/tower_back3.jpg")
    SURFACE.blit(pygame.transform.scale(pic, (WIDTH, HEIGHT)), (0, 0))

    music1 =  pygame.mixer.Channel(0)
    print("music", music1.get_busy)
    if music1.get_busy() == False:
        hoge = pygame.mixer.Sound("./msc/start_bgm.wav")
        pygame.mixer.set_reserved(1)
        music1.play(hoge, -1)
        music1.set_volume(1)

    #ボタン作成･表示
    button = pygame.Rect(400, 700, 500, 100)
    pygame.draw.rect(SURFACE, (255, 0, 0), button)

    #ボタン上のテキスト作成･表示
    text, text_pos = set_button_font(button, "すたーと", FONT_PATH, (255, 0, 255))
    SURFACE.blit( text, text_pos )

    #イベント処理
    for event in pygame.event.get():
        press_quit_mouse(event)
        if judge_mouse_button(event, button):
            return SCENE_MENU

    return SCENE_START

def menu_loop():
    
    global USER
    global LIFE
    global NOW_STAGE
    global BOSS_FLG

    #可変グローバル初期化
    LIFE = 3
    NOW_STAGE = 1
    BOSS_FLG = True

    SURFACE.fill((0, 0, 0))

    pic = pygame.image.load("./pic/brick_back.jpg")
    SURFACE.blit(pygame.transform.scale(pic, (WIDTH, HEIGHT)), (0, 0))

    music1 =  pygame.mixer.Channel(0)
    if music1.get_busy() == False:
        hoge = pygame.mixer.Sound("./msc/start_bgm.wav")
        pygame.mixer.set_reserved(1)
        music1.play(hoge, -1)
        music1.set_volume(1)

    #ボタン作成･表示
    if USER == "":
        button3 = pygame.Rect(400, 700, 500, 100)
        button4 = pygame.Rect(400, 500, 500, 100)
        pygame.draw.rect(SURFACE, (255, 0, 0), button3)
        pygame.draw.rect(SURFACE, (255, 0, 0), button4)
        text3, text_pos3 = set_button_font(button3, "ユーザー登録", FONT_PATH, (255, 255, 255))
        text4, text_pos4 = set_button_font(button4, "ログイン", FONT_PATH, (255, 255, 255))
        SURFACE.blit(text3, text_pos3 )
        SURFACE.blit(text4, text_pos4 )


    else:
        button = pygame.Rect(400, 700, 500, 100)
        button2 = pygame.Rect(400, 500, 500, 100)
        pygame.draw.rect(SURFACE, (255, 0, 0), button)
        pygame.draw.rect(SURFACE, (255, 0, 0), button2)
        text, text_pos = set_button_font(button, "ボスを倒す", FONT_PATH, (255, 255, 255))
        text2, text_pos2 = set_button_font(button2, "練習", FONT_PATH, (255, 255, 255))    
        SURFACE.blit(text, text_pos )
        SURFACE.blit(text2, text_pos2 )
        #テキスト表示
        txt1 = pygame.font.Font(FONT_PATH, 60).render("ようこそ!" + USER + "さん", True, (255,255,255))
        SURFACE.blit(txt1, [50, 100])   

    #イベント処理
    for event in pygame.event.get():
        press_quit_mouse(event)
        if USER == "":
            if judge_mouse_button(event, button3):
                return SCENE_REGISTER
            if judge_mouse_button(event, button4):
                return SCENE_LOGIN
        else:
            if judge_mouse_button(event, button):
                return SCENE_GAME
            if judge_mouse_button(event, button2):
                BOSS_FLG = False
                return SCENE_PRACTICE

    return SCENE_MENU

def game_loop():

    #↓↓↓初期化↓↓↓
    global NOW_STAGE
    global NOW_TIME
    global LIFE

    en = file_read(EN_PATH)
    jpn = file_read(JPN_PATH)

    isShuffle = True
    hp = MAXIMUM_HP
    start_time = time.time()
    miss_time = time.time()
    combo_time = time.time()
    attack_time = time.time()

    now_combo = 0
    effect_cnt = 9

    question_list = []
    button_pos_x = [450, 850, 450, 50]
    button_pos_y = [600, 700, 800, 700]
    button = []

    F_question = QUESTION_NUM * (NOW_STAGE - 1)
    L_question = QUESTION_NUM * NOW_STAGE
    if NOW_STAGE == LAST_STAGE:
        L_question = L_question + 1
    #↑↑↑初期化↑↑↑

    #game_bgm = pygame.mixer.music.load("./msc/game_bgm.mp3")     # 音楽ファイルの読み込み
    #game_bgm.play(-1)              # 音楽の再生回数(1回)

    hoge = pygame.mixer.Sound("./msc/game_bgm.wav")
    pygame.mixer.set_reserved(1)
    music1 =  pygame.mixer.Channel(0)
    music1.play(hoge, -1)
    music1.set_volume(0.2)
    

    while True:
        
        #時間測定
        NOW_TIME = TIME_LIMIT - (time.time() - start_time)

        #時間切れ
        if NOW_TIME < 0:
            LIFE = LIFE - 1
            return SCENE_FAILED

        if combo_time < time.time():
            now_combo = 0

        #ボス撃破
        if hp <= 0:
            print(DATA)
            update_score = min(float(DATA[NOW_STAGE-1]), TIME_LIMIT-NOW_TIME)
            DATA[NOW_STAGE-1] = str(update_score)
            print(DATA)

            write_text = []
            for char in DATA:
                write_text.append(char + "\n")

            write_text.insert(0, PASS + "\n")
            
            with open("./user/" + USER + ".txt", mode='w') as f:
                f.writelines(write_text)

            NOW_STAGE = NOW_STAGE + 1
            if NOW_STAGE > LAST_STAGE:
                NOW_STAGE = 1

            return SCENE_CLEAR

        #問題リスト作成
        if isShuffle and len(question_list) == 0:
            question_list = list(range(F_question, L_question))
            print(question_list)
            print(len(question_list), NOW_STAGE, F_question, L_question, len(en), len(jpn))
            random.shuffle(question_list)
        
        #問題選択肢作成
        if isShuffle:
            isShuffle = False
            now_question_num = question_list.pop(0)
            ans_idx = random.randint(0, 3)
            list_tmp = list(range(F_question, L_question))
            list_tmp.remove( now_question_num )
            selection_ans = random.sample( list_tmp, 4 )
            selection_ans[ans_idx] = now_question_num
            effect_cnt = 0
            attack_time = time.time()

        ###↓↓↓↓表示↓↓↓↓

        #ミスした時のエフェクト
        if miss_time > time.time():
            SURFACE.fill((0, 0, 0))
            pic = pygame.image.load("./pic/battle_back2.jpg")
            SURFACE.blit(pygame.transform.scale(pic, (WIDTH, HEIGHT)), (0, 0))
            pic2 = pygame.image.load("./pic/miss.png")  
            num = int(((miss_time-time.time())/MISS_TIME)*255)
            print(num)
            #pic2.set_alpha(int(((miss_time-time.time())/miss_time)*255))
            pic2.set_alpha(100)
            SURFACE.blit(pygame.transform.scale(pic2, (WIDTH, HEIGHT)), (0, 0))


        else:
            SURFACE.fill((0, 0, 0))
            pic = pygame.image.load("./pic/battle_back2.jpg")
            SURFACE.blit(pygame.transform.scale(pic, (WIDTH, HEIGHT)), (0, 0))

        for i in range(4):
            #ボタン作成･表示
            button.append( pygame.Rect(button_pos_x[i], button_pos_y[i], 350, 100) ) 
            pygame.draw.rect(SURFACE, (255, 0, 0), button[i])

            #ボタン上のテキスト作成･表示
            text, text_pos = set_button_font(button[i], en[selection_ans[i]], FONT_PATH, (100, 0, 255))
            SURFACE.blit(text, text_pos)

        #体力ゲージ
        pygame.draw.rect(SURFACE,(0,80,0),Rect(500,10,200,50),5) #塗りつぶしなし
        pygame.draw.rect(SURFACE,(0,80,0),Rect(500,10,hp,50)) #塗りつぶし

        #問題文        
        question_txt = pygame.font.Font(FONT_PATH, 30).render(jpn[now_question_num], True, (255,255,255))
        #question_txt = pygame.font.Font(FONT_PATH, 30).render("あいうえおかきくけこさしすせ", True, (255,255,255))
        SURFACE.blit(question_txt, [400, 750])

        #残り時間
        now_time_txt = pygame.font.Font(FONT_PATH, 60).render("残り"+str(int(NOW_TIME + 1))+"秒!", True, (255,255,255))
        SURFACE.blit(now_time_txt, [10, 10])

        #現在ステージ
        now_stage_txt = pygame.font.Font(FONT_PATH, 60).render(str(NOW_STAGE)+"ステージ目!", True, (255,255,255))
        SURFACE.blit(now_stage_txt, [10, 70])

        #現在コンボ
        now_combo_txt = pygame.font.Font(FONT_PATH, 60).render(str(now_combo)+"コンボ!", True, (255,255,255))
        SURFACE.blit(now_combo_txt, [10, 130])

        #画像表示
        img1 = pygame.image.load("./pic/enemy_001.png")
        SURFACE.blit(img1, (1000, 200))

        if effect_cnt < 9 and combo_time > time.time():
            print(effect_cnt)
            img2 = pygame.image.load("./pic/attack_00" + str(effect_cnt + 1) + ".png")
            SURFACE.blit(img2, (1100, 300))
            if attack_time + ATTACK_TIME < time.time():
                effect_cnt = effect_cnt + 1

        ###↑↑↑↑表示↑↑↑↑

        #イベント処理
        for event in pygame.event.get():
            press_quit_mouse(event)
            
            #マウス用
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(4):
                    if button[i].collidepoint(event.pos):
                        isShuffle, hp, miss_time, combo_time, now_combo = judge(i, ans_idx, hp, now_combo)
            #キーボード用
            if event.type == pygame.KEYDOWN:
                for i in range(4):
                    if event.key == DIRECTON_KEY[i]:
                        isShuffle, hp, miss_time, combo_time, now_combo = judge(i, ans_idx, hp, now_combo)

        pygame.display.update() #一番最後に記述

    return SCENE_GAME

def failed_loop():

    pic = []
    SURFACE.fill((0, 0, 0))

    pic1 = pygame.image.load("./pic/miss.png")
    SURFACE.blit(pygame.transform.scale(pic1, (WIDTH, HEIGHT)), (0, 0))

    for i in range(3):
        if i < LIFE:
            pic_path = "./pic/life_true.png"
        else:
            pic_path = "./pic/life_false.png"

        if BOSS_FLG:
            pic.append(pygame.image.load(pic_path))
            SURFACE.blit(pygame.transform.scale(pic[i], (100, 100)), (i * 120 + 900, 600))


    #ボタン作成･表示
    button = pygame.Rect(400, 700, 500, 100)
    pygame.draw.rect(SURFACE, (255, 0, 0), button)

    #ボタン上のテキスト作成･表示
    if not BOSS_FLG:
        button_text = "メニュー画面へ"
    elif LIFE == 0:
        button_text = "ゲームオーバー"
    else:
        button_text = "リトライ"
    text, text_pos = set_button_font(button, button_text, FONT_PATH, (255, 0, 255))
    SURFACE.blit(text, text_pos)

    #イベント処理
    for event in pygame.event.get():
        press_quit_mouse(event)
        #マウス用
        if judge_mouse_button(event, button):
            if LIFE == 0 or not BOSS_FLG:
                return SCENE_MENU
            else:
                return SCENE_GAME
        #キーボード用
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                if LIFE == 0 or not BOSS_FLG:
                    return SCENE_MENU
                else:
                    return SCENE_GAME
        
    return SCENE_FAILED

def clear_loop():

    pic = []
    SURFACE.fill((0, 0, 0))

    pic1 = pygame.image.load("./pic/clear_back2.jpg")
    SURFACE.blit(pygame.transform.scale(pic1, (WIDTH, HEIGHT)), (0, 0))

    for i in range(3):
        if i < LIFE:
            pic_path = "./pic/life_true.png"
        else:
            pic_path = "./pic/life_false.png"

        if BOSS_FLG:
            pic.append(pygame.image.load(pic_path))
            SURFACE.blit(pygame.transform.scale(pic[i], (100, 100)), (i * 120 + 900, 600))

    #クリア時間
    clear_time_txt = pygame.font.Font(FONT_PATH, 60).render("クリア時間:"+str(round(TIME_LIMIT-NOW_TIME, 3))+"秒!", True, (255,255,255))
    SURFACE.blit(clear_time_txt, [500, 400])

    #ボタン作成･表示
    button = pygame.Rect(400, 700, 500, 100)
    pygame.draw.rect(SURFACE, (255, 0, 0), button)

    #ボタン上のテキスト作成･表示
    if BOSS_FLG:
        text, text_pos = set_button_font(button, "ネクスト!", FONT_PATH, (255, 0, 255))
    else:
        text, text_pos = set_button_font(button, "メニュー画面へ", FONT_PATH, (255, 0, 255))
    SURFACE.blit(text, text_pos)

    #イベント処理
    for event in pygame.event.get():
        press_quit_mouse(event)
        #マウス用
        if judge_mouse_button(event, button):
            if BOSS_FLG:
                return SCENE_GAME
            else:
                return SCENE_MENU
        #キーボード用
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                if BOSS_FLG:
                    return SCENE_GAME
                else:
                    return SCENE_MENU
    return SCENE_CLEAR

def practice_loop():

    global NOW_STAGE

    button = []
    button_text2 = "メニュー画面へ"
    flg = True


    SURFACE.fill((200, 200, 200))

    button2 = pygame.Rect(1000, 200, 400, 100)
    pygame.draw.rect(SURFACE, (255, 0, 0), button2)
    text2, text_pos2 = set_button_font(button2, button_text2, FONT_PATH, (255, 0, 255))
    SURFACE.blit(text2, text_pos2)

    for i in range(LAST_STAGE):    
        #ボタン作成･表示
        x = i % 7
        y = i // 7
        button.append( pygame.Rect( x*110 + 100, y*90 + 100, 100, 50) )
        pygame.draw.rect(SURFACE, (255, 0, 0), button[i])

        #ボタン上のテキスト作成･表示
        text, text_pos = set_button_font(button[i], "ステージ" + str(i + 1), FONT_PATH, (255, 0, 255))
        SURFACE.blit(text, text_pos)

        if DATA[i] != str(INF):
            time_txt = pygame.font.Font(FONT_PATH, 20).render(str(round(float(DATA[i]), 3)), True, (255,255,255))
            SURFACE.blit(time_txt, [x*110 + 100, y*90 + 150])
        else:
            break
    
    #イベント処理
    for event in pygame.event.get():
        press_quit_mouse(event)
        if judge_mouse_button(event, button2):
            return SCENE_MENU
        if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(LAST_STAGE):
                    if button[i].collidepoint(event.pos):
                        NOW_STAGE = i + 1
                        return SCENE_GAME

    return SCENE_PRACTICE

def register_loop():
    
    clock = pygame.time.Clock()
    input_box1 = InputBox(200, 100, 140, 32)
    input_box2 = InputBox(200, 300, 140, 32)
    input_boxes = [input_box1, input_box2]
    done = False
    button_text = "登録"
    button_text2 = "ログイン画面へ"

    while not done:
        
        SURFACE.fill((0, 0, 0))
    
        pic = pygame.image.load("./pic/brick_back.jpg")
        SURFACE.blit(pygame.transform.scale(pic, (WIDTH, HEIGHT)), (0, 0))

        #ボタン作成･表示
        button = pygame.Rect(400, 700, 500, 100)
        pygame.draw.rect(SURFACE, (255, 0, 0), button)
        button2 = pygame.Rect(1000, 200, 400, 100)
        pygame.draw.rect(SURFACE, (255, 0, 0), button2)

        #ボタン上のテキスト作成･表示
        text, text_pos = set_button_font(button, button_text, FONT_PATH, (255, 0, 255))
        SURFACE.blit(text, text_pos)
        text2, text_pos2 = set_button_font(button2, button_text2, FONT_PATH, (255, 0, 255))
        SURFACE.blit(text2, text_pos2)

        #テキスト表示
        txt1 = pygame.font.Font(FONT_PATH, 30).render("ユーザー名", True, (255,255,255))
        SURFACE.blit(txt1, [10, 100])

        txt2 = pygame.font.Font(FONT_PATH, 30).render("パスワード", True, (255,255,255))
        SURFACE.blit(txt2, [10, 300])

        for event in pygame.event.get():
            press_quit_mouse(event)

            for box in input_boxes:
                box.handle_event(event)
                if not judge_register("./user/" + input_boxes[0].text + ".txt") or input_boxes[0].text == "":
                    button_text = "この名前は使えません"
                elif input_boxes[1].text == "":
                    button_text = "パスワードがありません"
                else:
                    button_text = "登録"

            if judge_mouse_button(event, button):
                if judge_register("./user/" + input_boxes[0].text + ".txt"):
                    file_user_write(input_boxes)
                    return SCENE_LOGIN
                else:
                    pass
            if judge_mouse_button(event, button2):
                return SCENE_LOGIN

        for box in input_boxes:
            box.update()

        for box in input_boxes:
            box.draw(SURFACE)

        pygame.display.update()
        #clock.tick(30)

def login_loop():
    
    global USER
    global PASS
    global DATA

    clock = pygame.time.Clock()
    input_box1 = InputBox(200, 100, 140, 32)
    input_box2 = InputBox(200, 300, 140, 32)
    input_boxes = [input_box1, input_box2]
    done = False
    button_text = "ログイン"
    button_text2 = "ユーザー登録画面へ"

    while not done:
        
        SURFACE.fill((0, 0, 0))

        pic = pygame.image.load("./pic/brick_back.jpg")
        SURFACE.blit(pygame.transform.scale(pic, (WIDTH, HEIGHT)), (0, 0))


        #ボタン作成･表示
        button = pygame.Rect(400, 700, 500, 100)
        pygame.draw.rect(SURFACE, (255, 0, 0), button)
        button2 = pygame.Rect(1000, 200, 400, 100)
        pygame.draw.rect(SURFACE, (255, 0, 0), button2)

        #ボタン上のテキスト作成･表示
        text, text_pos = set_button_font(button, button_text, FONT_PATH, (255, 0, 255))
        SURFACE.blit(text, text_pos)
        text2, text_pos2 = set_button_font(button2, button_text2, FONT_PATH, (255, 0, 255))
        SURFACE.blit(text2, text_pos2)


        #テキスト表示
        txt1 = pygame.font.Font(FONT_PATH, 30).render("ユーザー名", True, (255,255,255))
        SURFACE.blit(txt1, [10, 100])

        txt2 = pygame.font.Font(FONT_PATH, 30).render("パスワード", True, (255,255,255))
        SURFACE.blit(txt2, [10, 300])

        for event in pygame.event.get():
            press_quit_mouse(event)

            for box in input_boxes:
                if box.handle_event(event):
                    button_text = "ログイン"

            if judge_mouse_button(event, button):
                if judge_login("./user/" + input_boxes[0].text + ".txt", input_boxes[1].text):
                    file_text = file_read("./user/" + input_boxes[0].text + ".txt")
                    USER = input_boxes[0].text
                    PASS = file_text[0]
                    DATA = file_text[1:]
                    print(USER, PASS, DATA)
                    return SCENE_MENU
                else:
                    button_text = "ログイン出来ませんでした"

            if judge_mouse_button(event, button2):
                return SCENE_REGISTER

        for box in input_boxes:
            box.update()

        for box in input_boxes:
            box.draw(SURFACE)

        pygame.display.update()
        #clock.tick(30)

##### ↑↑↑画面切り替え↑↑↑  ##### 

def main():

    now_scene = SCENE_START

    while True:

        if now_scene == SCENE_START:
           now_scene = start_loop()

        if now_scene == SCENE_MENU:
            now_scene = menu_loop()
        
        if now_scene == SCENE_GAME:
            now_scene = game_loop()

        if now_scene == SCENE_FAILED:
            now_scene = failed_loop()
        
        if now_scene == SCENE_CLEAR:
            now_scene = clear_loop()
        
        if now_scene == SCENE_PRACTICE:
            now_scene = practice_loop()

        if now_scene == SCENE_REGISTER:
            now_scene = register_loop()

        if now_scene == SCENE_LOGIN:
            now_scene = login_loop()

        pygame.display.update() #一番最後に記述

if __name__ == "__main__":
    main()