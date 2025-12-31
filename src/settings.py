import json
import os


class Settings:

    def __init__(self, config, config_path):
        self.config = config
        self.config_path = config_path


    def field_checker(self):
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
        print(' 6. Настройка фонового шума')
        print(' 7. Завершить настройку')
        choice = input('Выберите действие: ').strip()
        return choice




    def full_setup(self):
        self.get_steam_path()
        self.get_api_key()
        self.browser_url()
        self.music_url()
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
                self.ambient_noise()

            elif choice == '7':
                os.system('cls')
                break
        
            else:
                print("Команда не найдена")
            
            os.system('cls')

        print('Говорите, я слушаю')

        self.save()
