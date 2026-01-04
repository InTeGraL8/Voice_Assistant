import json
import os, sys
import time


class Settings:

    def __init__(self, config, config_path):
        self.config = config
        self.config_path = config_path


    def field_checker(self):
        if 'assistant' not in self.config:
            self.config['assistant'] = {}

        if 'system_prompt' not in self.config['assistant']:
            self.config['assistant']['system_prompt'] = "ты голосовой ассистент,отвечай кратко,ответы озвучиваються"

        if 'auto_start' not in self.config['assistant']:
            self.config['assistant']['auto_start'] = False

        if 'paths' not in self.config:
            self.config['paths'] = {}

        if 'discord' not in self.config['paths']:
            self.config['paths']['discord'] = ''

        if 'steam' not in self.config['paths']:
            self.config['paths']['steam'] = ''

        if 'browser' not in self.config:
            self.config['browser'] = {}

        if 'browser_url' not in self.config['browser']:
            self.config['browser']['browser_url'] = "https://google.com"

        if 'music_url' not in self.config['browser']:
            self.config['browser']['music_url'] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1"

        if 'context' not in self.config:
            self.config['context'] = {}

        if 'is_enabled' not in self.config['context']:
            self.config['context']['is_enabled'] = False

        if 'message' not in self.config['context']:
            self.config['context']['message'] = []

        if 'max_lenght' not in self.config['context']:
            self.config['context']['max_lenght'] = 4

        self.save()





    def auto_start(self):
        import win32com.client

        print(f'Сейчас автозапуск {"выключен" if self.config["assistant"]["auto_start"] == False else "включен"}')
        print(f'Введите 0 если хотите оставить так')
        choice = input(f'Введите 1 если хотите {"включить" if self.config["assistant"]["auto_start"] == False else "выключить"}')
        

        auto_path = os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming', 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'Voice_Assistant.lnk')
        if choice == '1':

            if self.config['assistant']['auto_start'] == False:

                if getattr(sys, 'frozen', False):
                    exe_path = sys.executable
                    exe_folder = os.path.dirname(exe_path)
                    shell = win32com.client.Dispatch("WScript.Shell")

                    lnk = shell.CreateShortcut(auto_path)
                    lnk.TargetPath = exe_path
                    lnk.WorkingDirectory = exe_folder
                    lnk.IconLocation = exe_path
                    lnk.Save()

                else:
                    python_exe_path = sys.executable
                    main = os.path.join(os.path.dirname(__file__), 'main.py')
                    working_dir = os.path.join(os.path.dirname(__file__), '..')
                    ico = os.path.join(os.path.dirname(__file__), '..', 'ico.ico')

                    shell = win32com.client.Dispatch("WScript.Shell")

                    lnk = shell.CreateShortcut(auto_path)
                    lnk.TargetPath = python_exe_path
                    lnk.WorkingDirectory = working_dir
                    lnk.Arguments = main
                    lnk.IconLocation = ico
                    lnk.Save()


            else:
                if os.path.exists(auto_path):
                    os.remove(auto_path)

            self.config['assistant']['auto_start'] = not self.config['assistant']['auto_start']
            print(f'Автозапуск {"включен" if self.config["assistant"]["auto_start"] == True else "выключен"}')
            time.sleep(1)




    def browser_url(self):
        print("Введите ссылку вашего браузера")
        url = input("Ваша ссылка(Введите 0 для отмены): ")
        if url == '0':
            pass
        else:
            self.config['browser']['browser_url'] = url




    def music_url(self):
        print("Введите ссылку на плейлист или видео")
        url = input('Ваша ссылка(Введите 0 для отмены): ')
        if url == '0':
            pass
        else:
            self.config['browser']['music_url'] = url




    def get_discord_path(self, record = 0):
        if record == 0:
            print("Введите путь к Discord.exe(лежит в ...\Discord\app(версия)\Discord.exe)")
        else:
            print('Введите путь к Discord.exe повторно')

        print('Путь (0 если не хотите вводить): ', end='')

        path = input().strip()

        if path == '0':
            pass

        else:
            if not os.path.exists(path):
                return self.get_discord_path(record=1)
            self.config['paths']['discord'] = path




    def get_steam_path(self, record = 0):
        if record == 0:
            print("Введите путь к steam.exe(лежит в ...\Steam\steam.exe)")
        else:
            print('Введите путь к steam.exe повторно')

        print('Путь (0 если не хотите вводить): ', end='')

        path = input()

        if path == '0':
            pass

        else:
            if not os.path.exists(path):
                return self.get_steam_path(record=1)
            self.config['paths']['steam'] = path




    def ambient_noise(self):
        import speech_recognition as sr

        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        print("Калибровка шума, подождите 10 секунд")

        with mic as source:
           recognizer.adjust_for_ambient_noise(source, duration=10)

        self.config['micro']['ambient_noise'] = recognizer.energy_threshold




    def context(self):
        context = self.config['context']['is_enabled']
        print(f'Сейчас сохранение контекста {"включено" if context else "выключено"}')
        print("Введите 0 если не хотите менять")
        print(f"Введите 1 если хотите {'включить' if not context else 'выключить'}")
        choice = input()
        if choice == '1':
            self.config['context']['is_enabled'] = not self.config['context']['is_enabled']



    def get_api_key(self):
        print('Введите ключ к API GigaChat')
        print('Ключ (0 если не хотите вводить): ', end='')

        key = input()

        if key == '0':
            pass
        else:
            self.config['GigaChat']['api_key'] = key




    def choise(self):
        print('\nВыберите что вы хотите сделать')
        #print(' 1. Настроить путь к Discord.exe')
        print(' 1. Настроить путь к steam.exe')
        print(' 2. Ввести ключ к GigaChat API')
        print(' 3. Полная настройка путей и ключа')
        print(' 4. Ввести ссылку на ваш браузер')
        print(' 5. Ввести ссылку на ваш плейлист или видео')
        print(' 6. Настроить автозапуск')
        print(' 7. Настройка истории')
        print(' 8. Настройка фонового шума')
        print(' 9. Завершить настройку')
        choice = input('Выберите действие: ').strip()
        return choice




    def full_setup(self):
        self.get_steam_path()
        self.get_api_key()
        self.browser_url()
        self.music_url()
        self.auto_start()
        self.context()
        self.ambient_noise()




    def save(self):
        with open(self.config_path, 'w', encoding='utf-8') as file:
            json.dump(self.config, file, indent=2, ensure_ascii=False)




    def main(self):
        self.field_checker()

        while True:
            choice = self.choise()
            #if choice == '1':
            #    self.get_discord_path()
        
            if choice == '1':
                self.get_steam_path()
        
            elif choice == '2':
                self.get_api_key()
        
            elif choice == '3':
                self.full_setup()

            elif choice == '4':
                self.browser_url()

            elif choice == '5':
                self.music_url()
            
            elif choice == '6':
                self.auto_start()

            elif choice == '7':
                self.context()

            elif choice == '8':
                self.ambient_noise()

            elif choice == '9':
                os.system('cls')
                break
        
            else:
                print("Команда не найдена")
            os.system('cls')

        print('Говорите, я слушаю')
        self.save()