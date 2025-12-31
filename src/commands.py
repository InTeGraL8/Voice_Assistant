import os, sys
import subprocess
import time
import webbrowser
import json
import ctypes
import settings
from datetime import datetime, timedelta


if getattr(sys, 'frozen', False):
    config_path = os.path.join(os.path.dirname(sys.executable), 'config.json')
else:
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

with open(config_path, 'r', encoding='utf-8') as file:
    config = json.load(file)



def is_run(name):
    try:
        res = subprocess.run(
            ['tasklist', '/FI', f'IMAGENAME eq {name}'],
            capture_output=True, 
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return name in res.stdout
    except:
        return False




def open_window(name):
    try:
        hwnd = ctypes.windll.user32.FindWindowW(None, name)
        
        if hwnd:
            # Если окно свёрнуто - восстанавливаем
            if ctypes.windll.user32.IsIconic(hwnd):
                ctypes.windll.user32.ShowWindow(hwnd, 9)
            
            # Активируем окно
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            return True
        return False
    except:
        return False






def open_steam():
    steam_path = config['paths']['steam']
    if steam_path == '':
        return 'Не найден путь к steam.exe'

    if is_run('Steam.exe'):
        try:
            open_window('Steam')

        except Exception as e:
            print(e)
    
    try:
        os.startfile(steam_path)
        return("Открываю steam")

    except Exception as e:
        print(f'Не удалось запустить steam: {e}')
        return f"Не удалось запустить steam: {e}"



def open_in_browser(web='', view=''):
    if web == '':
        try:
            if config['browser']['browser_url'].strip() != "":
                webbrowser.open(config['browser']['browser_url'], new=0)
                return "Открываю браузер"
            else:
                return "Ссылка на браузер не найдена. Пожалуйста, введите её в настройках"
        except Exception as e:
            return f'Ошибка {e}'
        
    if web == 'youtube':
        if view == '':
            webbrowser.open('https://www.youtube.com/', new=0, autoraise=True)
            return "Открываю YouTube"
        if view == 'music':
            if config['browser']['music_url'] != "":
                webbrowser.open(config['browser']['music_url'], new=0, autoraise=True)
                return "Открываю плейлист"
            else:
                return "Ссылка на плейлист не найдена. Пожалуйста, введите её в настройках"
    return "Выполнено"




def open_settings(config, config_path):
    sett = settings.Settings(config, config_path)
    sett.main()



week_day = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']

commands = { 
    lambda: f"Сейчас {time.strftime('%H:%M')}": ['который час', 'время', 'сколько времени', 'подскажи время', 'текущее время', 'сколько сейчас времени', 'скажи который час', 'сколько на часах', 'время'],
    lambda: f"Сегодня {time.strftime('%d.%m.%Y')}": ['какое сегодня число', 'число', 'какое число', 'скажи дату', 'какое сегодня число месяца', 'какая сегодня дата', 'назови сегодняшнюю дату', 'какой сегодня день и число', 'дата', 'число'],
    lambda: f"Сегодня {week_day[datetime.now().weekday()]}": ['какой сегодня день','день недели', 'какой день недели', 'какой сегодня день недели', 'скажи какой сегодня день', 'сегодня что', 'что у нас сегодня за день', 'какое число и день', 'какой день'],
    lambda: sys.exit() : ['выход','отключись','отключаемся','отключайся'],

    lambda: open_in_browser(): ['открой браузер', 'запусти браузер', 'включи браузер', 'открой интернет', 'запусти интернет', 'открой новое окно', 'новая вкладка', 'браузер'],
    lambda: open_in_browser('youtube'): ['открой youtube', 'youtube', 'запусти youtube', 'запусти ютуб', 'открой ютюб', 'зайди на youtube', 'включи youtube', 'хочу посмотреть видео', 'поищи видео на youtube', 'включи youtube', 'найди', 'открой мой youtube', 'открой ютуб', 'зайди на ютуб', 'включи ютуб'],
    lambda: open_in_browser('youtube', 'music'): ['музыка', 'включи музыку', 'музыку','включи музыку', 'запусти музыку', 'включи плейлист', 'включи плеер'],

    lambda: open_steam():['открой steam', 'запусти steam', 'steam', 'открой стим', 'запусти стим', 'стим'],
    lambda: open_settings(config, config_path):['настройки', 'открой настройки']
}




def executing_command(text):
    for command_func, keywords in commands.items():
        if text in keywords:
            result = command_func()
            return result
    return None