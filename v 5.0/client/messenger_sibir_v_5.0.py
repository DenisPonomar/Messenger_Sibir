import pygame
import os
import copy
import time
import clipboard

import pygame_gui
from pygame_gui.windows.ui_file_dialog import UIFileDialog
from pygame_gui.elements.ui_button import UIButton
from pygame_gui.windows import UIColourPickerDialog
from pygame.rect import Rect
from pygame_gui.core import ObjectID

import shutil

import base64

import colorsys

import random

import requests
from threading import Thread
import hashlib

pygame.init()
#size = width, height = pygame.display.Info().current_w/2, pygame.display.Info().current_h/2
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)
#pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.DOUBLEBUF)
screen.set_alpha(None)

f12 = pygame.font.Font("OpenSans-Regular.ttf", 12)
f16 = pygame.font.Font("OpenSans-Regular.ttf", 16)
f24 = pygame.font.Font("OpenSans-Regular.ttf", 24)
f32 = pygame.font.Font("OpenSans-Regular.ttf", 32)

#загрузка ip-адреса и порта
f = open("ip.txt", 'r')
ip = str(f.read())
f.close()

#Загрузка настроек приватности
f = open("private.txt", 'r')
private = str(f.read())
f.close()

running = True
buffer_soob_otpavit = []
buffer_soob_vremya = []
def otpravka_soob():
    global buffer_soob_vremya
    global buffer_soob_otpavit
    global izmenenie
    while running:
        time.sleep(0.1)
        #Если не надо ничего отправлять, проверяем на наличие новых сообщение
        if len(buffer_soob_otpavit) == 0:
            try:
                response = requests.get(str("http://"+ip+"/"+"a"+"!"+token))
            except Exception:
                continue
            if response.status_code != 200:
                continue
            vhod_soob = response.text.split("!")
            hash_token_otpravitel = vhod_soob[0]
            time_soob = float(vhod_soob[1])
            code_soob = vhod_soob[2][:1]
            text_soob = vhod_soob[2][2:]

            #Если нет папки контакта, то создаём её
            if not os.path.isdir(hash_token_otpravitel):
                if private == "Мои контакты":
                    continue
                
                os.mkdir(hash_token_otpravitel)

                shutil.copyfile("15421/face.jpg", str(hash_token_otpravitel+"/face.jpg"))
                                
                f = open(str(hash_token_otpravitel+"/message.txt"), 'w')
                f.write("[]")
                f.close()
                                
                f = open(str(hash_token_otpravitel+"/name.txt"), 'w')
                f.write("")
                f.close()

            f = open(str(hash_token_otpravitel+"/message.txt"), 'r')
            soob_poluch = eval(str(f.read()))
            f.close()

            f = open(str(put+"/"+soob_pol+"/name.txt"), 'r')
            name_poluch = str(f.read())[:24]
            f.close()

            if name_poluch == "" and private == "Мои контакты":
                continue

            if code_soob == "a": #Получить новое сообщение
                u = [text_soob, "1", time_soob, 1]
                soob_poluch.append(u)
            if code_soob == "b": #Изменить сообщение
                izm_soob = text_soob.split("&")[0]
                izm_vremya = float(text_soob.split("&")[1])
                if time_soob - izm_vremya < 86400.0:
                    for j in range(len(soob_poluch)):
                        if soob_poluch[j][2] == izm_vremya:
                            soob_poluch[j][0] = izm_soob
                            break
            
            if code_soob == "c": #Удалить сообщение
                udalit_vremya = float(text_soob)
                for j in range(len(soob_poluch)):
                    if soob_poluch[j][2] == udalit_vremya:
                        soob_poluch.pop(j)
                        break
            
            f = open(str(hash_token_otpravitel+"/message.txt"), 'w')
            f.write(str(soob_poluch))
            f.close()
                                                
            izmenenie = True
        #Если есть что отправить, отправляем на сервер
        if len(buffer_soob_otpavit) != 0:
            code_soob = buffer_soob_otpavit[0][0]
            
            soob_bufer = buffer_soob_otpavit[0][1]
            vremya_buffer = buffer_soob_otpavit[0][2]
            soob_pol_buffer = buffer_soob_otpavit[0][3]
            try:
                if code_soob == "a": #Запрос на отправку сообщения
                    response = requests.get(str("http://"+ip+"/"+"b"+"!"+token+"!"+str(soob_pol_buffer)+"!a&"+soob_bufer))
                if code_soob == "b": #Запрос на изменения сообщения
                    response = requests.get(str("http://"+ip+"/"+"b"+"!"+token+"!"+str(soob_pol_buffer)+"!b&"+soob_bufer+"&"+str(vremya_buffer)))
                if code_soob == "c": #Запрос на удаления сообщения
                    response = requests.get(str("http://"+ip+"/"+"b"+"!"+token+"!"+str(soob_pol_buffer)+"!c&"+str(vremya_buffer)))
            except Exception:
                continue
            
            server_time = float(response.text)
            buffer_soob_vremya = [vremya_buffer, server_time, soob_pol_buffer]
            buffer_soob_otpavit.pop(0)

            #Если получен ответ от сервера в ответ на отправку сообщения, то заменить в отправленном сообщении время компьютера серверным временем

            f = open(str(put+"/"+str(buffer_soob_vremya[2])+"/message.txt"), 'r')
            soob_buff = eval(str(f.read()))
            f.close()
            soob_buff.reverse()
            for j in range(len(soob_buff)):
                if soob_buff[j][2] == buffer_soob_vremya[0] and soob_buff[j][3] == 0:
                    soob_buff[j][2] = buffer_soob_vremya[1]
                    soob_buff[j][3] = 1
                    
                    soob_buff.reverse()
                    f = open(str(put+"/"+buffer_soob_vremya[2]+"/message.txt"), 'w')
                    f.write(str(soob_buff))
                    f.close()
                    soob_buff.reverse()
                                                    
                    izmenenie = True

                    buffer_soob_vremya = []
                    break
                
            
thread1 = Thread(target=otpravka_soob, args=())
thread1.start()
#Добавление в буфер неотправленных сообщений
def otpravka_neotpravlennyh_soob():
    global buffer_soob_otpavit
    papka = os.listdir(".")
    for i in range(len(papka)):
        if os.path.isfile(papka[i]):
            pass
        else:
            f = open(str(papka[i]+"/message.txt"), 'r')
            soob = eval(str(f.read()))
            f.close()
            for k in range(len(soob)):
                if soob[k][3] == 0: 
                    buffer_soob_otpavit.append(["a", soob[k][0], soob[k][2], papka[i]])
otpravka_neotpravlennyh_soob()

try:
    #Загрузка токена
    f = open("token.txt", 'r')
    token = str(f.read())
    f.close()
except Exception:
    #Установка токена
    size = width, height = 360, 270
    screen = pygame.display.set_mode(size)
    manager_ustanovit = pygame_gui.UIManager((width, height), "vvod.json")
    
    obnovit_ustanovit = UIButton(relative_rect=Rect(50, height/2+36/2, width-100, 36), manager=manager_ustanovit, text='Создать новый', object_id=ObjectID(object_id="#16"))
    token_ustanovit = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=Rect(50, height/2-36/2, width-150, 36), manager=manager_ustanovit, object_id=ObjectID(object_id="#16"))
    token_ustanovit.set_text_length_limit(16)
    token_ustanovit.set_allowed_characters(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"])
    otpravit_ustanovit = UIButton(relative_rect=Rect(width-100, height/2-36/2, 50, 36), manager=manager_ustanovit, text='>', object_id=ObjectID(object_id="#24"))
    clock = pygame.time.Clock()
    time_delta = clock.tick(60)/1000
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    #Сгенерировать новый случайный токен
                    if event.ui_element == obnovit_ustanovit:
                        tkn = random.randint(0, (2**64)-1)
                        tkn = (tkn).to_bytes(8, byteorder="big")
                        tkn = base64.b16encode(tkn).decode('UTF-8')
                        token_ustanovit.set_text(str(tkn))
                    #Установить токен
                    if event.ui_element == otpravit_ustanovit:
                        if len(token_ustanovit.get_text()) == 16:
                            token = token_ustanovit.get_text()
                            f = open("token.txt", 'w')
                            f.write(str(token))
                            f.close()
                            size = width, height = 1280, 720
                            screen = pygame.display.set_mode(size)
                            running = False
                        
            manager_ustanovit.process_events(event)
        screen.fill((47, 47, 47))
        manager_ustanovit.update(time_delta)
        manager_ustanovit.draw_ui(screen)

        t1 = f24.render("Введите токен:", 1, (208, 208, 208))
        t_rr = (50, height/2-36*1.5)
        screen.blit(t1, t_rr)
        
        pygame.display.flip()
        clock.tick(144)
#Установка хэш-токена
hash_token = hashlib.sha256(token.encode("utf-8")).hexdigest()

#Загрузка фонового цвета
f = open("colour.txt", 'r')
colour = eval(str(f.read()))
f.close()

#Установление цвета текста
colour_txt = [abs(255-colour[0]), abs(255-colour[1]), abs(255-colour[2])]

#Загрузка цвета сообщения
f = open("colour_soob.txt", 'r')
colour_soob = eval(str(f.read()))
f.close()

#Преобразование RGB в HSV
def rgb_to_hsv(rgb):
    r = rgb[0]/255
    g = rgb[1]/255
    b = rgb[2]/255
    hsv = colorsys.rgb_to_hsv(r, g, b)
    hsv = (hsv[0] * 360, hsv[1] * 100, hsv[2] * 100)
    return hsv

#Загрузка пути фонового изображения
f = open("photo.txt", 'r')
photo = str(f.read())
try:
    photo_load = pygame.transform.scale((pygame.image.load(photo).convert()), (width, height))
except Exception:
    pass
f.close()

#Функция, выполняющая перенос текста
def razd_text(text, font, dlina):
        line_width = 0
        txt=""
        mas_t = []
        for i in range(len(text)):
            if font.size(text[i])[0] > dlina:
                for j in range(len(text[i])):
                    line_width =line_width+font.size(text[i][j])[0]
                    if line_width > dlina:
                        mas_t.append(txt)
                        txt = text[i][j]
                        line_width = font.size(text[i][j])[0]
                    else:
                        txt=txt+text[i][j]
            else:
                line_width =line_width +font.size(text[i]+" ")[0]
                if line_width > dlina:
                    mas_t.append(txt)
                    txt = text[i]+" "
                    line_width = font.size(text[i]+" ")[0]
                else:
                    txt=txt+text[i]+" "
        mas_t.append(txt)
        return mas_t
        
soob=[]
def mest_soob():
    #Загрузка сообщений
    global soob
    f = open(str(put+"/"+soob_pol+"/message.txt"), 'r')
    while True:
        try:
            soob = eval(str(f.read()))
            f.close()
            break
        except Exception:
            continue
    
    soob.reverse()

    #Загрузка имени контакта
    f = open(str(put+"/"+soob_pol+"/name.txt"), 'r')
    global name_soob
    name_soob = str(f.read())[:24]
    f.close()

    #Добавление перенесённого текста сообщения в массив
    global mest_soob_mas
    mest_soob_mas = []
    for i in range(len(soob)):
        
        text = base64.b64decode(soob[i][0].encode("utf-8")).decode("utf-8")
        n = soob[i][1]
        text_mas = text.split()
    
        txt = razd_text(text_mas, f16, width-300-width/3)
        mest_soob_mas.append(txt)

#Словарь положения скроллинга экрана
per_y = {}
per_y["glav_okno"] = 0
#Словарь положения полосы скроллинга сообщений
per_ys = {}
#Словарь текста, введённого в поле ввода
temp_vvod = {}
#Словарь выделения окна сообщения
soob_vybran = {}
#ID отображаемого окна сообщения (по умолчанию ID избранного)
soob_pol = "15421"
#Не показывать окно добавления контакта
dob_pol = False
#Не показывать окно настроек
nastrojki = False
#Не показывать окно изменения контакта
izmenit_contact = False
#Не показывать окно удаления
udalit = False

#Список ID контактов
pol=[]
#Список имён контактов
name=[]
#Список фото контактов, отображаемых в окне выбора диалога
face=[]
#Список фото контактов, отображаемых в собщенияй
face_pol = {}
#Список, сортируемый по дате последнего сообщения
pos_soob = []
#Количество контактов
kol_pol = 0
#Путь по умолчанию
put = '.'
#Необходимо загрузить или обновить данные, необходимые для отображения окна выбора диалога
izmenenie = True
#Загрузка необходимых элементов для главного экран
papka = os.listdir(put)
def zagruzka_glavnoe_okno():
    global papka
    papka = os.listdir(put)
    global izmenenie
    izmenenie = False
    
    global pol
    global name
    global face
    global pos_soob
    global kol_pol
    global face_pol

    kol_pol = 0
    pol=[]
    name=[]
    face=[]
    pos_soob = []
    papki = []
    face_pol = {}

    for i in range(len(papka)):
        if os.path.isfile(put+"/"+papka[i]):
            pass
        else:
            papki.append(papka[i])
    
    for i in range(len(papki)):
            pol_temp = str(papki[i])
            f = open(str(put+"/"+papki[i]+"/name.txt"), 'r')
            name_temp = str(f.read())[:24]
            
            face_temp = pygame.transform.scale((pygame.image.load(papki[i]+"/face.jpg").convert()), (75, 75))
            f.close()

            face_pol[papki[i]] = pygame.transform.scale((pygame.image.load(papki[i]+"/face.jpg").convert()), (60, 60))
            
            f = open(str(put+"/"+papki[i]+"/message.txt"), 'r')
            p_soob = eval(str(f.read()))
            f.close()
            
            if len(p_soob) == 0:
                p_soob = [["", '0', 0, 1]]
                pos_soob.append(p_soob[len(p_soob)-1])
                
                pos_soob[i].append(pol_temp)
                pos_soob[i].append(name_temp)
                pos_soob[i].append(face_temp)
            else:
                pos_soob.append(p_soob[len(p_soob)-1])
                
                pos_soob[i].append(pol_temp)
                pos_soob[i].append(name_temp)
                pos_soob[i].append(face_temp)
            
    pos_soob.sort(key = lambda x: x[2], reverse=True)
    
    for i in range(len(papki)):
            pol.append(pos_soob[i][4])
            name.append(pos_soob[i][5])
            face.append(pos_soob[i][6])
            
            kol_pol=kol_pol+1
        
screen.fill([0, 0, 0])
fs = pygame.font.SysFont(None, 96)
t1 = fs.render("Загрузка графики", 1, [200, 200, 200])
t_r = t1.get_rect(center=(width/2, height/2))
screen.blit(t1, t_r)
pygame.display.flip()
#Отображение окна выбора диалога
def Spisok_soob():
    global per_y
    global soob_pol
    d = per_y["glav_okno"]
    if event.type == pygame.MOUSEWHEEL:
        if pygame.mouse.get_pos()[0] > 0 and pygame.mouse.get_pos()[0] < width/3:
            d = d + event.y*10
            if d > 0:
                d = 0
            if d < -kol_pol*80+80:
                d = -kol_pol*80+80
            event.y = 0
    for i in range(kol_pol):
        
        pygame.draw.aaline(screen, [200, 200, 200], [0, 80+80*i+d+80], [width/3, 80+80*i+d+80])
        #Если нажать на блок с последним сообщением, фотом и именем контакта, то отобразить диалог этого контакта
        if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                                if event.pos[0] > 0 and event.pos[0] < width/3:
                                        if event.pos[1] > 80+80*i+d and event.pos[1] < 80+80*i+d+80:
                                                global temp_vvod
                                                temp_vvod[soob_pol] = vvod_soob_okno_soob.get_text()
                                                
                                                soob_pol = pol[i]
                                                d = 0
                                                global mest_soob
                                                mest_soob()
                                                
                                                
                                                if soob_pol not in temp_vvod:
                                                    temp_vvod[soob_pol] = ""
                                                vvod_soob_okno_soob.set_text(temp_vvod[soob_pol])

        
        #Отображение имени контакта
        t1 = f16.render(name[i], 1, colour_txt)
        t_r = (100, 80+80*i+d+10)
        screen.blit(t1, t_r)
        cropped_background = pygame.Surface((75, 75), pygame.SRCALPHA)
        pygame.draw.ellipse(cropped_background, (255, 255, 255, 255), (0, 0, 75, 75))
        cropped_background.blit(face[i], (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        screen.blit(cropped_background, (10, 80+80*i+d+5))

        #Отображение последнего сообщения в диалоге контакта
        t = base64.b64decode(pos_soob[i][0].encode("utf-8")).decode("utf-8")
        t1 = f16.render(t[:32], 1, (int(colour_txt[0]*0.8), int(colour_txt[1]*0.8), int(colour_txt[2]*0.8)))
        t_r = (100, 120+80*i+d+10)
        screen.blit(t1, t_r)

        #Отображение даты последнего сообщения в диалоге контакта
        l = time.localtime(pos_soob[i][2])
        if pos_soob[i][2] != 0:
            t = time.strftime("%d/%m", l)
            t1 = f16.render(str(t), 1, (int(colour_txt[0]*0.8), int(colour_txt[1]*0.8), int(colour_txt[2]*0.8)))
            t_r = (width/3-75, 80+80*i+d+10)
            screen.blit(t1, t_r)
        
    per_y["glav_okno"] = d
#Отображение верхнего меню    
manager_sibir_text = pygame_gui.UIManager((width, height), "vvod.json")
nastrojki_sibir_text = UIButton(relative_rect=Rect(25, 15, 50, 50), manager=manager_sibir_text, text='=', object_id=ObjectID(object_id="#24"))
dob_pol_sibir_text = UIButton(relative_rect=Rect(width/3-75, 15, 50, 50), manager=manager_sibir_text, text='+', object_id=ObjectID(object_id="#24"))
def Sibir_text():
    pygame.draw.rect(screen, colour, [0, 0, width/3, 80], 0)
    
    t1 = f32.render("Сибирь", 1, colour_txt)
    t_r = t1.get_rect(center=(width/6, 40))
    screen.blit(t1, t_r)
    
    pygame.draw.aaline(screen, [200, 200, 200], [0, 80], [width/3, 80])

#Переменная, поднимающая или опускающая сообщения
vd = 364

#Отображения окна сообщения
manager_okno_soob = pygame_gui.UIManager((width, height), "vvod.json")
skopirovat_okno_soob = UIButton(relative_rect=Rect(width-250, 15, 50, 50), manager=manager_okno_soob, text='C', object_id=ObjectID(object_id="#24"))
izmenit_contact_okno_soob = UIButton(relative_rect=Rect(width-175, 15, 50, 50), manager=manager_okno_soob, text='I', object_id=ObjectID(object_id="#24"))
udalit_okno_soob =UIButton(relative_rect=Rect(width-100, 15, 50, 50), manager=manager_okno_soob, text='X', object_id=ObjectID(object_id="#24"))
vvod_soob_okno_soob = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=Rect(width/3+100, height-400+vd, width-width/3-200, 36), manager=manager_okno_soob, object_id=ObjectID(object_id="#16"))
vvod_soob_okno_soob.set_text_length_limit(12000)
dobavit_okno_soob = UIButton(relative_rect=Rect(width/3+50, height-400+vd, 50, 36), manager=manager_okno_soob, text='+', object_id=ObjectID(object_id="#24"))
otpravit_okno_soob = UIButton(relative_rect=Rect(width-100, height-400+vd, 50, 36), manager=manager_okno_soob, text='>', object_id=ObjectID(object_id="#24"))
scroll_bar_okno_soob = pygame_gui.elements.UIVerticalScrollBar(relative_rect=pygame.Rect(width-25, 0, 25, height), visible_percentage=0.1,manager=manager_okno_soob)
scroll_bar_okno_soob.scroll_position = 607
def okno_soob():
    global soob_pol
    #Скрыть кнопки изменения и удаления контакта, если отображается избранное
    if soob_pol == "15421":
        izmenit_contact_okno_soob.hide()
        udalit_okno_soob.hide()
    #Иначе показать
    else:
        izmenit_contact_okno_soob.show()
        udalit_okno_soob.show()
    
    global vd
    
    vd = 364

    #Если в словаре нету ключа для текущего окна сообщения, то создать его
    global per_y
    if soob_pol not in per_y:
        per_y[soob_pol] = 0
    d = per_y[soob_pol]

    #Код, отвечающий за отображение или скрытие кнопок удаления, изменения и копирования сообщений
    global soob_vybran
    if soob_pol not in soob_vybran:
        soob_vybran[soob_pol] = []
        
    if len(soob_vybran[soob_pol]) > 1:
        izmenit_contact_okno_soob.hide()
        skopirovat_okno_soob.hide()
    elif len(soob_vybran[soob_pol]) == 1:
        if (time.time() - soob_vybran[soob_pol][0]) < 86400.0:
            for i in range(len(soob)):
                if soob[i][2] == soob_vybran[soob_pol][0]:
                    if soob[i][1] == "0":
                        izmenit_contact_okno_soob.show()
                    else:
                        izmenit_contact_okno_soob.hide()
        else:
           izmenit_contact_okno_soob.hide()
        skopirovat_okno_soob.show()
    else:
        if soob_pol == "15421":
            izmenit_contact_okno_soob.hide()
        else:
            izmenit_contact_okno_soob.show()
        skopirovat_okno_soob.hide()
    if len(soob_vybran[soob_pol]) > 0:
        udalit_okno_soob.show()
    
    
    global x_soob
    x_soob=0
    if 42 == 42:
        for k in range(len(soob)):
            n = soob[k][1]
            txt = mest_soob_mas[k]
            x_soob = x_soob + len(txt)
            if len(txt) == 1:
                kr = True
            else:
                kr = False
                
            #Отображение блоков сообщения
            if height >  24*1+height-(24*x_soob )-425+d+vd-8 > 0 -(16+24*len(txt)+8+16):
                for i in range(1):
                    dlina_text = f16.size(txt[0])[0]
                    l = time.localtime(int(soob[abs(len(soob)-1-k)][2]))
                    if dlina_text < f12.size(time.strftime("%H:%M:%S", l))[0]:
                        dlina_text = f12.size(time.strftime("%H:%M:%S", l))[0]
                    
                    if n == "1":
                        t_rr = ((width/3+100, 24*i+height-(24*x_soob )-425+d+vd-8))
                    elif n == "0":
                            if kr:
                                t_rr = (int(width-dlina_text)-100, 24*i+height-(24*x_soob)-425+d+vd-8)
                            else:
                                t_rr = (width/3+200, 24*i+height-(24*x_soob)-425+d+vd-8)

                #Выбор блока сообщения
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if event.pos[0] > width/3 and event.pos[0] < width-25:
                            if event.pos[1] > 24*i+height-(24*x_soob )-425+d+vd-8 and event.pos[1] < (24*i+height-(24*x_soob )-425+d+vd-8)+(16+24*len(txt)+8) and event.pos[1] > 80 and event.pos[1] < height-36:
                                event.pos = [0, 0]
                                if soob[k][2] not in soob_vybran[soob_pol]:
                                    soob_vybran[soob_pol].append(soob[k][2])
                                else:
                                    soob_vybran[soob_pol].remove(soob[k][2])
                #Отображение блоков сообщения
                if soob[k][2] in soob_vybran[soob_pol]:
                    pygame.draw.rect(screen, (colour[0]+20, colour[0]+20, colour[0]+20), (width/3, 24*i+height-(24*x_soob )-425+d+vd-16, 2*width/3, 16+24*len(txt)+8+16), 0)
                
                if kr:
                    pygame.draw.rect(screen, colour_soob, (t_rr[0]-20, t_rr[1], dlina_text+40, 16+24*len(txt)+8), 0, 20)
                else:
                    pygame.draw.rect(screen, colour_soob, (t_rr[0]-20, t_rr[1], width-300+40-width/3, 16+24*len(txt)+8), 0, 20)

                    
            #Отображения текста сообщения
            for i in range(len(txt)):
                dlina_text = f16.size(txt[i])[0]
                l = time.localtime(int(soob[k][2]))
                if dlina_text < f12.size(time.strftime("%H:%M:%S", l))[0]:
                    dlina_text = f12.size(time.strftime("%H:%M:%S", l))[0]
                
                if height >  24*1+height-(24*x_soob )-425+d+vd-8 > 0 -(16+24*len(txt)+8+16):
                    t1 = f16.render(str(txt[i]), 1, colour_txt)
                    if n == "1":
                        t_rr = ((width/3+100, 24*i+height-(24*x_soob )-425+d+vd-8))
                    elif n == "0":
                        if kr:
                            t_rr = (int(width-dlina_text)-100, 24*i+height-(24*x_soob)-425+d+vd-8)
                        else:
                            t_rr = (width/3+200, 24*i+height-(24*x_soob)-425+d+vd-8)
                    screen.blit(t1, t_rr)

            #Отображение времени сообщения
            if height >  24*1+height-(24*x_soob )-425+d+vd-8 > 0 -(16+24*len(txt)+8+16):
                if soob[k][3] == 0:
                    t1 = f12.render("________", 1, colour_txt)
                else:
                    t1 = f12.render(time.strftime("%H:%M:%S", l), 1, colour_txt)
                if n == "0":
                    t_rr = (int(width-f16.size(time.strftime("%H:%M:%S", l))[0])-80, 24*len(txt)+16+height-(24*x_soob )-425+d+vd-16)
                elif n == "1":
                    if kr:
                        t_rr = (width/3+100+int(dlina_text)-int(f12.size(time.strftime("%H:%M:%S", l))[0]), 24*len(txt)+16+height-(24*x_soob )-425+d+vd-16)
                    else:
                        t_rr = ((width/3+int(width-f12.size(time.strftime("%H:%M:%S", l))[0])-200, 24*len(txt)+16+height-(24*x_soob )-425+d+vd-16))
                        
                screen.blit(t1, t_rr)

            #Отображение даты сообщения
            if k != len(soob)-1:
                l = time.localtime(int(soob[k][2]))
                ll = time.localtime(int(soob[k+1][2]))
                if time.strftime("%d/%m/%Y", l) != time.strftime("%d/%m/%Y", ll):
                    if height >  24*1+height-(24*x_soob )-425+d+vd-8 > 0 -(16+24*len(txt)+8+16):
                        t1 = f12.render(time.strftime("%d/%m/%Y", l), 1, colour_txt)
                        t_rr = (t1.get_rect(center=(width/6+width/2, 24*1+height-(24*x_soob )-425+d+vd-48)))
                        screen.blit(t1, t_rr)
                    x_soob = x_soob + 2.5
                else:
                    x_soob = x_soob + 1.5
            else:
                if height >  24*1+height-(24*x_soob )-425+d+vd-8 > 0 -(16+24*len(txt)+8+16):
                    t1 = f12.render(time.strftime("%d/%m/%Y", l), 1, colour_txt)
                    t_rr = (t1.get_rect(center=(width/6+width/2, 24*1+height-(24*x_soob )-425+d+vd-48)))
                    screen.blit(t1, t_rr)
                x_soob = x_soob + 2.5

    d = (height - (scroll_bar_okno_soob.scroll_position/(607/720)))/height* (-(24*0-(24*x_soob)+75))
    #Скроллинг окна колёсикомм мышки
    if event.type == pygame.MOUSEWHEEL:
        if pygame.mouse.get_pos()[0] > width/3 and pygame.mouse.get_pos()[0] < width:
            d = d + int(event.y*24)
            if d < 0:
                d = 0
            if d > -(24*0-(24*x_soob)+75):
                d = -(24*0-(24*x_soob)+75)
            event.y = 0
    
    scroll_bar_okno_soob.scroll_position = (height-(d/ (-(24*0-(24*x_soob)+75)))*height)*(607/720)

    #Отображение имени контакта
    pygame.draw.rect(screen, colour, [width/3, 0, width*2/3, 80], 0)
    t1 = f32.render(name_soob, 1, colour_txt)
    t_rr = (width/3+100, 20)
    screen.blit(t1, t_rr)

    #Отображение фото контакта
    global face_pol
    f = face_pol[soob_pol] 
    cropped_background = pygame.Surface((60, 60), pygame.SRCALPHA)
    pygame.draw.ellipse(cropped_background, (255, 255, 255, 255), (0, 0, 60, 60))
    cropped_background.blit(f, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    screen.blit(cropped_background, (width/3+20, 10))
    
    per_y[soob_pol] = d
    
    pygame.draw.rect(screen, colour, [width/3, height-400+vd, width*2/3, 80], 0)

    pygame.draw.aaline(screen, [200, 200, 200], [width/3, 0], [width/3, height])
    pygame.draw.aaline(screen, [200, 200, 200], [width/3, 80], [width, 80])

#Отображение окна добавления контакта                       
manager_dob_pol = pygame_gui.UIManager((width, height), "vvod.json")
nazad_dob_pol = UIButton(relative_rect=Rect(25, 15, 50, 50), manager=manager_dob_pol, text='<', object_id=ObjectID(object_id="#24"))
vvod_name_contact = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(relative_rect=Rect(25, 175, width/3-50, 50), manager=manager_dob_pol, object_id=ObjectID(object_id="#24"))
vvod_name_contact.set_text_length_limit(24)
id_contact_dob_pol = UIButton(relative_rect=Rect(25, 255, width/3-50, 50), manager=manager_dob_pol, text='Нажмите, чтобы вставить id', object_id=ObjectID(object_id="#24"))
file_selection_button = UIButton(relative_rect=Rect(25, 335, 250, 50), manager=manager_dob_pol, text='Выбрать фото', object_id=ObjectID(object_id="#24"))
dob_contact_button = UIButton(relative_rect=Rect(25, 415, width/3-50, 50), manager=manager_dob_pol, text='Сохранить', object_id=ObjectID(object_id="#24"))
id_contact="Нажмите для вставки id"
name_contact=""
foto_contact = ""
def okno_dob_pol():
    global id_contact
    global foto_contact
    global name_contact
    
    name_contact = vvod_name_contact.get_text()
    
    if izmenit_contact:
        t1 = f32.render("Изменить контакт", 1, colour_txt)
    if dob_pol:
        t1 = f32.render("Добавить контакт", 1, colour_txt)
    t_r = t1.get_rect(center=(width/6, 40))
    screen.blit(t1, t_r)
    
    t1 = f24.render("Имя контакта:", 1, colour_txt)
    t_rr = (50, 95+8)
    screen.blit(t1, t_rr)
    
    try:
        f = pygame.transform.scale((pygame.image.load(foto_contact).convert()), (75, 75))
        cropped_background = pygame.Surface((75, 75), pygame.SRCALPHA)
        pygame.draw.ellipse(cropped_background, (255, 255, 255, 255), (0, 0, 75, 75))
        cropped_background.blit(f, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        screen.blit(cropped_background, (300, 320+2.5))
    except Exception:
        foto_contact = ""
        
    for i in range(5):
        pygame.draw.aaline(screen, [200, 200, 200], [0, 80+80*i], [width/3, 80+80*i])

#Отображение окна настроек
manager_okno_nastrojki = pygame_gui.UIManager((width, height), "vvod.json")
nazad_okno_nastrojki = UIButton(relative_rect=Rect(25, 15, 50, 50), manager=manager_okno_nastrojki, text='<', object_id=ObjectID(object_id="#24"))
token_okno_nastrojki = UIButton(relative_rect=Rect(25, 95, width/3-50, 50), manager=manager_okno_nastrojki, text=str("Скопировать свой id"), object_id=ObjectID(object_id="#24"))
color_okno_nastrojki = UIButton(relative_rect=Rect(25, 175, width/3-50, 50), manager=manager_okno_nastrojki, text="Выбрать цвет фона", object_id=ObjectID(object_id="#24"))
photo_okno_nastrojki = UIButton(relative_rect=Rect(25, 255, width/3-100, 50), manager=manager_okno_nastrojki, text="Выбрать фото фона", object_id=ObjectID(object_id="#24"))
del_photo_okno_nastrojki = UIButton(relative_rect=Rect(width/3-75, 255, 50, 50), manager=manager_okno_nastrojki, text="X", object_id=ObjectID(object_id="#24"))
languages_dropdown = pygame_gui.elements.UIDropDownMenu(['Все пользователи', 'Мои контакты'], private,pygame.Rect(25, 415, width/3-50, 50),manager=manager_okno_nastrojki, object_id=ObjectID(object_id="#24"))
colour_soob_okno_nastrojki = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(relative_rect=Rect(25, 575, width/3-50, 50), manager=manager_okno_nastrojki, start_value=rgb_to_hsv(colour_soob)[0], value_range=(0, 360), object_id=ObjectID(object_id="#24"))
sbros_okno_nastrojki = UIButton(relative_rect=Rect(25, 655, width/3-50, 50), manager=manager_okno_nastrojki, text=str("Сбросить все настройки"), object_id=ObjectID(object_id="#24"))
def okno_nastrojki():
    t1 = f32.render("Настройки", 1, colour_txt)
    t_r = t1.get_rect(center=(width/6, 40))
    screen.blit(t1, t_r)
    
    t1 = f24.render("Кто может мне писать в лс:", 1, colour_txt)
    t_rr = (25, 335+8)
    screen.blit(t1, t_rr)
    
    for i in range(8):
        pygame.draw.aaline(screen, [200, 200, 200], [0, 80+80*i], [width/3, 80+80*i])

    t1 = f24.render("Цвет блока сообщения:", 1, colour_txt)
    t_rr = (25, 495+8)
    screen.blit(t1, t_rr)

    global colour_soob
    colour_soob = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(colour_soob_okno_nastrojki.get_current_value()/360, 75/100, 1))
    
    f = open("colour_soob.txt", 'w')
    f.write(str(colour_soob))
    f.close()

#Отображение окна удаления
all_udalit = False
manager_okno_udalit = pygame_gui.UIManager((width, height), "vvod.json")
nazad_okno_udalit = UIButton(relative_rect=Rect(25, 15, 50, 50), manager=manager_okno_udalit, text='<', object_id=ObjectID(object_id="#24"))
contact_okno_udalit = UIButton(relative_rect=Rect(25, 95, width/3-50, 50), manager=manager_okno_udalit, text=str("Удалить контакт"), object_id=ObjectID(object_id="#24"))
dialog_okno_udalit = UIButton(relative_rect=Rect(25, 175, width/3-50, 50), manager=manager_okno_udalit, text=str("Удалить диалог"), object_id=ObjectID(object_id="#24"))
contact_dialog_okno_udalit = UIButton(relative_rect=Rect(25, 255, width/3-50, 50), manager=manager_okno_udalit, text=str("Удалить контакт и диалог"), object_id=ObjectID(object_id="#24"))
all_okno_udalit = UIButton(relative_rect=Rect(25, 335, width/3-50, 50), manager=manager_okno_udalit, text=str("Удалить всё"), object_id=ObjectID(object_id="#24"))
podtverdit_all_okno_udalit =pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = Rect(25, 15, 400, 300), manager=manager_okno_udalit, action_long_desc='Вы действительно хотите удалить папку контакта вместе со всем содержимым? Вы не сможете ему больше писать и он не сможет вам писать, до тех пор, пока он также не удалит папку для повторного установления сквозного шифрования.', object_id=ObjectID(object_id="#24"))
podtverdit_all_okno_udalit.hide()
def okno_udalit():
    t1 = f32.render("Удаление", 1, colour_txt)
    t_r = t1.get_rect(center=(width/6, 40))
    screen.blit(t1, t_r)
    
    for i in range(5):
        pygame.draw.aaline(screen, [200, 200, 200], [0, 80+80*i], [width/3, 80+80*i])

global tek_fps
tek_fps = 1/60
clock = pygame.time.Clock()
time_delta = clock.tick(60)/1000
running = True
while running:
    if soob_pol not in per_ys:
                per_ys[soob_pol] = 607
    scroll_bar_okno_soob.scroll_position = per_ys[soob_pol]
    scroll_bar_okno_soob.rebuild()
    ty = time.time()
    mest_soob()
    #Если есть изменения в сообщениях, обновить главный экран
    if izmenenie:
        zagruzka_glavnoe_okno()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            soob_pol == None
            running = False
        #Установка цвета фона
        if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
            colour = event.colour
            colour_txt = [abs(255-colour[0]), abs(255-colour[1]), abs(255-colour[2])]
            if running:
                f = open("colour.txt", 'w')
                f.write(str(colour))
                f.close()
        #Установка настроек приватности
        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if event.text == 'Все пользователи':
                private = 'Все пользователи'
            elif event.text == 'Мои контакты':
                private = 'Мои контакты'
            f = open("private.txt", 'w')
            f.write(private)
            f.close()
        #Полное удаление контакта после подтверждения
        if event.type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
            all_udalit = True
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                #sibir_text
                #Кнопка открытия настроек
                if event.ui_element == nastrojki_sibir_text:
                    nastrojki = True
                #Кнопка открытия окна добавления контакта
                if event.ui_element == dob_pol_sibir_text:
                    vvod_name_contact.set_text("")
                    name_contact = ""
                    id_contact="Нажмите для вставки id"
                    id_contact_dob_pol.set_text("Нажмите для вставки id")
                    foto_contact = ""
                    dob_pol = True
                if event.ui_element == file_selection_button:
                    file_selection = UIFileDialog(rect=Rect(0, 0, 600, 600), manager=manager_dob_pol, allow_picking_directories=True)
                try:
                    if event.ui_element == file_selection.ok_button:
                        foto_contact = file_selection.current_file_path
                except Exception:
                    pass
                #dob_pol
                #Вернуться назад к окну выбора диалога
                if event.ui_element == nazad_dob_pol:
                        izmenit_contact = False
                        dob_pol = False
                #Кнопка вставки или копирования id (хэш-токена) контакта
                if event.ui_element == id_contact_dob_pol:
                    if dob_pol:
                        id_contact = clipboard.paste()
                        id_contact = list(id_contact)
                        #Удалить симолы, не встречающиеся в хэш-токене
                        for i in range(len(id_contact)):
                            if id_contact[i] not in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]:  
                                id_contact[i] = None
                        while None in id_contact:
                            id_contact.remove(None)
                        id_contact = "".join(id_contact)
                        #Если длина хэш-токена не равна 64, сбросить значение
                        if len(id_contact) != 64:
                            id_contact="Нажмите для вставки id"
                        id_contact_dob_pol.set_text(id_contact)
                    if izmenit_contact:
                        clipboard.copy(soob_pol)
                #Кнопка добавления или изменения контакта
                if event.ui_element == dob_contact_button:
                    if dob_pol:
                        if not os.path.isdir(id_contact) and foto_contact != "" and name_contact != "" and id_contact != "Нажмите для вставки id":
                            izmenenie = True

                            os.mkdir(id_contact)
                            
                            shutil.copyfile(foto_contact, str(id_contact+"/face.jpg"))
                            
                            f = open(str(id_contact+"/message.txt"), 'w')
                            f.write("[]")
                            f.close()
                            
                            f = open(str(id_contact+"/name.txt"), 'w')
                            f.write(str(name_contact))
                            f.close()
                if izmenit_contact:
                        izmenenie = True
                        try:
                            shutil.copyfile(foto_contact, str(id_contact+"/face.jpg"))
                        except Exception:
                            pass
                            
                        f = open(str(id_contact+"/name.txt"), 'w')
                        f.write(str(name_contact))
                        f.close()
                #okno_soob
                if event.ui_element == otpravit_okno_soob:
                    #Если поле ввода не пустое
                    if vvod_soob_okno_soob.get_text() != "":
                            #Если выделено только одно сообшение
                            if len(soob_vybran[soob_pol]) == 1:
                                #И оно не старше суток, то изменить
                                if (time.time() - soob_vybran[soob_pol][0]) < 86400.0:
                                    for i in range(len(soob_vybran[soob_pol])):
                                        for j in range(len(soob)):
                                            if soob[j][2] == soob_vybran[soob_pol][i]:
                                                soob[j][0] = base64.b64encode(bytes(vvod_soob_okno_soob.get_text().encode('utf-8'))).decode("utf-8").replace('DQ==', '', 0)

                                                if soob_pol != "15421": #Добавить в буфер изменённое сообщение
                                                    buffer_soob_otpavit.append(["b", soob[j][0], soob[j][2], soob_pol])
                                                
                                                soob.reverse()
                                                f = open(str(put+"/"+soob_pol+"/message.txt"), 'w')
                                                f.write(str(soob))
                                                f.close()
                                                soob.reverse()
                                                
                                                izmenenie = True
                                
                            else: #Иначе отправить новое
                                soob.reverse()
                                if soob_pol != "15421":
                                    u = [base64.b64encode(bytes(vvod_soob_okno_soob.get_text().encode('utf-8'))).decode("utf-8").replace('DQ==', '', 0), "0", time.time(), 0]
                                if soob_pol == "15421":
                                    u = [base64.b64encode(bytes(vvod_soob_okno_soob.get_text().encode('utf-8'))).decode("utf-8").replace('DQ==', '', 0), "0", time.time(), 1]
                                soob.append(u)

                                if soob_pol != "15421": #Добавляем в буфер новое сообщение
                                    buffer_soob_otpavit.append(["a", base64.b64encode(bytes(vvod_soob_okno_soob.get_text().encode('utf-8'))).decode("utf-8").replace('DQ==', '', 0), time.time(), soob_pol])
                                
                                f = open(str(put+"/"+soob_pol+"/message.txt"), 'w')
                                f.write(str(soob))
                                f.close()
                                soob.reverse()
                                vvod_soob_okno_soob.set_text("")
                                
                                izmenenie = True
                
                if soob_pol != "15421":
                    if event.ui_element == izmenit_contact_okno_soob:
                        if len(soob_vybran[soob_pol]) == 1:
                            for i in range(len(soob_vybran[soob_pol])):
                                for j in range(len(soob)):
                                    if soob[j][2] == soob_vybran[soob_pol][i]:
                                        vvod_soob_okno_soob.set_text(base64.b64decode(soob[j][0].encode("utf-8")).decode("utf-8"))
                        else:
                            izmenit_contact = True
                            vvod_name_contact.set_text(name_soob)
                            id_contact = soob_pol
                            id_contact_dob_pol.set_text(soob_pol)
                            foto_contact = soob_pol+"/face.jpg"
                    if event.ui_element == udalit_okno_soob:
                        if soob_vybran[soob_pol] != []:
                            for i in range(len(soob_vybran[soob_pol])):
                                for j in range(len(soob)):
                                    if soob[j][2] == soob_vybran[soob_pol][i]:
                                        #Добавить в буфер удалённое сообщение
                                        buffer_soob_otpavit.append(["c", soob[j][0], soob[j][2], soob_pol])
                                        soob.pop(j)
                                        soob_vybran[soob_pol][i] = None
                                        break
                            while None in soob_vybran[soob_pol]:
                                soob_vybran[soob_pol].remove(None)
                            
                            soob.reverse()
                            f = open(str(put+"/"+soob_pol+"/message.txt"), 'w')
                            f.write(str(soob))
                            f.close()
                            soob.reverse()
                            
                            izmenenie = True
                        else:
                            udalit = True
                if soob_pol == "15421":
                    if event.ui_element == izmenit_contact_okno_soob:
                        if len(soob_vybran[soob_pol]) == 1:
                            for i in range(len(soob_vybran[soob_pol])):
                                for j in range(len(soob)):
                                    if soob[j][2] == soob_vybran[soob_pol][i]:
                                        vvod_soob_okno_soob.set_text(base64.b64decode(soob[j][0].encode("utf-8")).decode("utf-8"))
                    if event.ui_element == udalit_okno_soob:
                        if soob_vybran[soob_pol] != []:
                            for i in range(len(soob_vybran[soob_pol])):
                                for j in range(len(soob)):
                                    if soob[j][2] == soob_vybran[soob_pol][i]:
                                        soob.pop(j)
                                        soob_vybran[soob_pol][i] = None
                                        break
                            while None in soob_vybran[soob_pol]:
                                soob_vybran[soob_pol].remove(None)
                            
                            soob.reverse()
                            f = open(str(put+"/"+soob_pol+"/message.txt"), 'w')
                            f.write(str(soob))
                            f.close()
                            soob.reverse()
                            
                            izmenenie = True
                #Если нажата кнопка скопировать сообщение
                if event.ui_element == skopirovat_okno_soob:
                    for i in range(len(soob_vybran[soob_pol])):
                                for j in range(len(soob)):
                                    if soob[j][2] == soob_vybran[soob_pol][i]:
                                        clipboard.copy(base64.b64decode(soob[j][0].encode("utf-8")).decode("utf-8"))
                #okno_nastrojki
                if nastrojki:
                    #Вернуться назад к окну выбора диалога
                    if event.ui_element == nazad_okno_nastrojki:
                        nastrojki = False
                    #Кнопка открытия окна выбора цвета
                    if event.ui_element == color_okno_nastrojki:
                        colour_picker = UIColourPickerDialog(pygame.Rect(0, 0, 420, 400),manager=manager_okno_nastrojki,window_title='Выбрать цвет')
                    #Кнопка копирования хэш-токена
                    if token_okno_nastrojki:
                        clipboard.copy(hash_token)
                    #Кнопка открытия окна выбора фонового фото
                    if event.ui_element == photo_okno_nastrojki:
                        photo_selection = UIFileDialog(rect=Rect(0, 0, 600, 600), manager=manager_okno_nastrojki, allow_picking_directories=True)
                    try:
                        if event.ui_element == photo_selection.ok_button:
                            photo = photo_selection.current_file_path
                            f = open("photo.txt", 'w')
                            f.write(str(photo))
                            f.close()
                            photo_load = pygame.transform.scale((pygame.image.load(photo).convert()), (width, height))
                    except Exception:
                        pass
                    #Кнопка удаления фонового фото
                    if event.ui_element == del_photo_okno_nastrojki:
                        photo=""
                        f = open("photo.txt", 'w')
                        f.write(str(photo))
                        f.close()
                        photo_load = ""
                    #Кнопка сброса настроек
                    if event.ui_element == sbros_okno_nastrojki:
                        colour = (47, 47, 47, 255)
                        colour_txt = [abs(255-colour[0]), abs(255-colour[1]), abs(255-colour[2])]
                        f = open("colour.txt", 'w')
                        f.write(str(colour))
                        f.close()

                        photo = ""
                        photo_load = ""
                        f = open("photo.txt", 'w')
                        f.write(str(photo))
                        f.close()

                        private = 'Все пользователи'
                        f = open("private.txt", 'w')
                        f.write(private)
                        f.close()

                        colour_soob = 240
                        colour_soob_okno_nastrojki.set_current_value(colour_soob)
                        f = open("colour_soob.txt", 'w')
                        f.write(str(colour_soob))
                        f.close()

                        languages_dropdown = pygame_gui.elements.UIDropDownMenu(['Все пользователи', 'Мои контакты'], private,pygame.Rect(25, 415, width/3-50, 50),manager=manager_okno_nastrojki, object_id=ObjectID(object_id="#24"))
                        
                #okno_udalit
                if udalit:
                    #Вернуться назад к окну выбора диалога
                    if event.ui_element == nazad_okno_udalit:
                        udalit = False
                        try:
                            f = open(soob_pol+"/name.txt")
                            f.close()
                        except Exception:
                            soob_pol = "15421"
                    #Удалить контакт (имя контакта)
                    if event.ui_element == contact_okno_udalit:
                            izmenenie = True
                            f = open(soob_pol+"/name.txt", 'w')
                            f.write(str(""))
                            f.close()
                    #Удалить всю переписку с контактом
                    if event.ui_element ==  dialog_okno_udalit:
                            izmenenie = True
                            soob = []
                    if event.ui_element == contact_dialog_okno_udalit:
                            izmenenie = True
                            f = open(soob_pol+"/name.txt", 'w')
                            f.write(str(""))
                            f.close()
                            soob = []
                    #Удалить полностью папку контакта со всем содержимым
                    if event.ui_element == all_okno_udalit:
                        podtverdit_all_okno_udalit = pygame_gui.windows.ui_confirmation_dialog.UIConfirmationDialog(rect = Rect(25, 15, 400, 300), manager=manager_okno_udalit, action_long_desc='Вы действительно хотите удалить папку контакта вместе со всем содержимым? Вы не сможете ему больше писать и он не сможет вам писать, до тех пор, пока он также не удалит папку для повторного установления сквозного шифрования.', object_id=ObjectID(object_id="#24"))
                        podtverdit_all_okno_udalit.show()
            
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    #Если поле ввода не пустое
                    if vvod_soob_okno_soob.get_text() != "":
                            #Если выделено только одно сообшение
                            if len(soob_vybran[soob_pol]) == 1:
                                #И оно не старше суток, то изменить
                                if (time.time() - soob_vybran[soob_pol][0]) < 86400.0:
                                    for i in range(len(soob_vybran[soob_pol])):
                                        for j in range(len(soob)):
                                            if soob[j][2] == soob_vybran[soob_pol][i]:
                                                soob[j][0] = base64.b64encode(bytes(vvod_soob_okno_soob.get_text().encode('utf-8'))).decode("utf-8").replace('DQ==', '', 0)

                                                if soob_pol != "15421":
                                                    buffer_soob_otpavit.append(["b", soob[j][0], soob[j][2], soob_pol])
                                                
                                                soob.reverse()
                                                f = open(str(put+"/"+soob_pol+"/message.txt"), 'w')
                                                f.write(str(soob))
                                                f.close()
                                                soob.reverse()
                                                
                                                izmenenie = True
                                
                            else: #Иначе отправить новое
                                soob.reverse()
                                if soob_pol != "15421":
                                    u = [base64.b64encode(bytes(vvod_soob_okno_soob.get_text().encode('utf-8'))).decode("utf-8").replace('DQ==', '', 0), "0", time.time(), 0]
                                if soob_pol == "15421":
                                    u = [base64.b64encode(bytes(vvod_soob_okno_soob.get_text().encode('utf-8'))).decode("utf-8").replace('DQ==', '', 0), "0", time.time(), 1]
                                soob.append(u)

                                if soob_pol != "15421": #Добавляем в буфер новое сообщение
                                    buffer_soob_otpavit.append(["a", base64.b64encode(bytes(vvod_soob_okno_soob.get_text().encode('utf-8'))).decode("utf-8").replace('DQ==', '', 0), time.time(), soob_pol])
                                
                                f = open(str(put+"/"+soob_pol+"/message.txt"), 'w')
                                f.write(str(soob))
                                f.close()
                                soob.reverse()
                                vvod_soob_okno_soob.set_text("")
                                
                                izmenenie = True
        if soob_pol != None:
            if dob_pol:
                manager_dob_pol.process_events(event)
            elif nastrojki:
                manager_okno_nastrojki.process_events(event)
            elif izmenit_contact:
                manager_dob_pol.process_events(event)
            elif udalit:
                manager_okno_udalit.process_events(event)
            else:
                manager_sibir_text.process_events(event)
        if True:
            manager_okno_soob.process_events(event)
    mest_soob()
    try:
        screen.blit(photo_load, (0, 0))
    except Exception:
        screen.fill(colour)
    okno_soob()
    manager_okno_soob.update(time_delta)
    manager_okno_soob.draw_ui(screen)
    per_ys[soob_pol] = scroll_bar_okno_soob.scroll_position
    if dob_pol:
        okno_dob_pol()
        manager_dob_pol.update(time_delta)
        manager_dob_pol.draw_ui(screen)
    elif nastrojki:
        okno_nastrojki()
        manager_okno_nastrojki.update(time_delta)
        manager_okno_nastrojki.draw_ui(screen)
    elif izmenit_contact:
        okno_dob_pol()
        manager_dob_pol.update(time_delta)
        manager_dob_pol.draw_ui(screen)
    elif udalit:
        okno_udalit()
        manager_okno_udalit.update(time_delta)
        manager_okno_udalit.draw_ui(screen)
    else:
        Spisok_soob()
        Sibir_text()
        manager_sibir_text.update(time_delta)
        manager_sibir_text.draw_ui(screen)

    if all_udalit:
            all_udalit = False
            udalit = False
            izmenenie = True
            shutil.rmtree(soob_pol)
            soob_pol = "15421"
    
    clock.tick(144)
    tek_fps = 1/(time.time()-ty)
    t1 = f32.render(str(int(tek_fps))+"fps", 1, colour_txt)
    t_r = t1.get_rect(center=(width-300, 40))
    screen.blit(t1, t_r)
    pygame.display.flip()
pygame.quit()
