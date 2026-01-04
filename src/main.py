import pyttsx3
import speech_recognition as sr
import os
import sys
import json
import commands
import gigachat
import settings


def speak(text):
    global voice_engine
    try:
        voice_engine.say(text)
        voice_engine.runAndWait()
    except Exception as e:
        voice_engine = pyttsx3.init()
        voice_engine.say(text)
        voice_engine.runAndWait()


def get_config_path():
    if getattr(sys, 'frozen', False):
        config_path = os.path.join(os.path.dirname(sys.executable), 'config.json')
    else:
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    return config_path


def set():
    print("Калибровка шума... молчите 10 секунд")
    with mic as source:
       recognizer.adjust_for_ambient_noise(source, duration=10)
    config['micro']['ambient_noise'] = recognizer.energy_threshold
    with open(config_path, 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=2)
    setting = settings.Settings(config=config, config_path=config_path)
    setting.main()


config_path = get_config_path()
with open(config_path, 'r', encoding='utf-8') as file:
    config = json.load(file)

setting = settings.Settings(config=config, config_path=config_path)
setting.field_checker()





voice_engine = pyttsx3.init()
recognizer = sr.Recognizer()
mic = sr.Microphone()
recognizer.dynamic_energy_threshold=False
recognizer.pause_threshold = 0.5

is_first_launch = False

if config.get('micro', {}).get('ambient_noise', 0) == 0:
    is_first_launch = True
    set()

else:
    recognizer.energy_threshold = config['micro']['ambient_noise']

if not is_first_launch:
    print('Говорите, я слушаю')
speak('Говорите, я слушаю')
# Основной цикл
try:
    while True:
        with mic as source:
            audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)
            
            try:
                # Превращение звука в текст
                text = recognizer.recognize_google(audio, language='ru-RU').lower()
                print('Текст:',text)

                # Есть ли эта команда? Да - выполняем, нет - идём дальше
                res = commands.executing_command(text)
                if res:
                    print(res)
                    speak(res)

                # Здесь должен происходить запрос к GigaChat
                else:
                    if 'ассистент' in text:
                        answer = gigachat.processor(text)
                        if config['context']['is_enabled'] == True:
                            pass
                        print(answer)
                        speak(answer)

            except sr.UnknownValueError:
                print("Речь не распознана")

            except sr.RequestError:
                print("Ошибка соединения с Google")
                    
except KeyboardInterrupt:
    print("\nПрограмма остановлена")