# Импорты
import json
import requests
import os
import sys
import uuid
import tempfile
import atexit

cert = '''-----BEGIN CERTIFICATE-----
MIIFwjCCA6qgAwIBAgICEAAwDQYJKoZIhvcNAQELBQAwcDELMAkGA1UEBhMCUlUx
PzA9BgNVBAoMNlRoZSBNaW5pc3RyeSBvZiBEaWdpdGFsIERldmVsb3BtZW50IGFu
ZCBDb21tdW5pY2F0aW9uczEgMB4GA1UEAwwXUnVzc2lhbiBUcnVzdGVkIFJvb3Qg
Q0EwHhcNMjIwMzAxMjEwNDE1WhcNMzIwMjI3MjEwNDE1WjBwMQswCQYDVQQGEwJS
VTE/MD0GA1UECgw2VGhlIE1pbmlzdHJ5IG9mIERpZ2l0YWwgRGV2ZWxvcG1lbnQg
YW5kIENvbW11bmljYXRpb25zMSAwHgYDVQQDDBdSdXNzaWFuIFRydXN0ZWQgUm9v
dCBDQTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBAMfFOZ8pUAL3+r2n
qqE0Zp52selXsKGFYoG0GM5bwz1bSFtCt+AZQMhkWQheI3poZAToYJu69pHLKS6Q
XBiwBC1cvzYmUYKMYZC7jE5YhEU2bSL0mX7NaMxMDmH2/NwuOVRj8OImVa5s1F4U
zn4Kv3PFlDBjjSjXKVY9kmjUBsXQrIHeaqmUIsPIlNWUnimXS0I0abExqkbdrXbX
YwCOXhOO2pDUx3ckmJlCMUGacUTnylyQW2VsJIyIGA8V0xzdaeUXg0VZ6ZmNUr5Y
Ber/EAOLPb8NYpsAhJe2mXjMB/J9HNsoFMBFJ0lLOT/+dQvjbdRZoOT8eqJpWnVD
U+QL/qEZnz57N88OWM3rabJkRNdU/Z7x5SFIM9FrqtN8xewsiBWBI0K6XFuOBOTD
4V08o4TzJ8+Ccq5XlCUW2L48pZNCYuBDfBh7FxkB7qDgGDiaftEkZZfApRg2E+M9
G8wkNKTPLDc4wH0FDTijhgxR3Y4PiS1HL2Zhw7bD3CbslmEGgfnnZojNkJtcLeBH
BLa52/dSwNU4WWLubaYSiAmA9IUMX1/RpfpxOxd4Ykmhz97oFbUaDJFipIggx5sX
ePAlkTdWnv+RWBxlJwMQ25oEHmRguNYf4Zr/Rxr9cS93Y+mdXIZaBEE0KS2iLRqa
OiWBki9IMQU4phqPOBAaG7A+eP8PAgMBAAGjZjBkMB0GA1UdDgQWBBTh0YHlzlpf
BKrS6badZrHF+qwshzAfBgNVHSMEGDAWgBTh0YHlzlpfBKrS6badZrHF+qwshzAS
BgNVHRMBAf8ECDAGAQH/AgEEMA4GA1UdDwEB/wQEAwIBhjANBgkqhkiG9w0BAQsF
AAOCAgEAALIY1wkilt/urfEVM5vKzr6utOeDWCUczmWX/RX4ljpRdgF+5fAIS4vH
tmXkqpSCOVeWUrJV9QvZn6L227ZwuE15cWi8DCDal3Ue90WgAJJZMfTshN4OI8cq
W9E4EG9wglbEtMnObHlms8F3CHmrw3k6KmUkWGoa+/ENmcVl68u/cMRl1JbW2bM+
/3A+SAg2c6iPDlehczKx2oa95QW0SkPPWGuNA/CE8CpyANIhu9XFrj3RQ3EqeRcS
AQQod1RNuHpfETLU/A2gMmvn/w/sx7TB3W5BPs6rprOA37tutPq9u6FTZOcG1Oqj
C/B7yTqgI7rbyvox7DEXoX7rIiEqyNNUguTk/u3SZ4VXE2kmxdmSh3TQvybfbnXV
4JbCZVaqiZraqc7oZMnRoWrXRG3ztbnbes/9qhRGI7PqXqeKJBztxRTEVj8ONs1d
WN5szTwaPIvhkhO3CO5ErU2rVdUr89wKpNXbBODFKRtgxUT70YpmJ46VVaqdAhOZ
D9EUUn4YaeLaS8AjSF/h7UkjOibNc4qVDiPP+rkehFWM66PVnP1Msh93tc+taIfC
EYVMxjh8zNbFuoc7fzvvrFILLe7ifvEIUqSVIC/AzplM/Jxw7buXFeGP1qVCBEHq
391d/9RAfaZ12zkwFsl+IKwE/OZxW8AHa9i1p4GO0YSNuczzEm4=
-----END CERTIFICATE-----'''


def create_temp_cert():
    """Создаёт временный файл с сертификатом и возвращает путь к нему"""
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.pem', delete=False)
    temp_file.write(cert)
    temp_file.close()
    
    # Удалим файл при завершении программы
    atexit.register(lambda: os.unlink(temp_file.name))
    
    return temp_file.name

# Создаём файл сертификата один раз при загрузке модуля
CERT_PATH = create_temp_cert()


# Получаем конфиг
if getattr(sys, 'frozen', False):
    config_path = os.path.join(os.path.dirname(sys.executable), 'config.json')

else:
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

# Считываем конфиг
with open(config_path, 'r',  encoding='utf-8') as file:
    config = json.load(file)


# Запрос на получение токена
def get_token(api_key):
    # Url куда отправлять запрос
    auth_url = config['GigaChat']['auth_url']

    # Права
    payload ={'scope': config['GigaChat']['payload']}

    # Заголовок HTML запроса 
    headers = {
      # Кодировка тела
      'Content-Type': 'application/x-www-form-urlencoded',
      # Что хочу получить
      'Accept': 'application/json',
      # ID запроса
      'RqUID': str(uuid.uuid4()),
      # Ключ
      'Authorization': f'Basic {api_key}'
      }

    # Получаем токен
    response = requests.request("POST", auth_url, headers=headers, data=payload, verify=CERT_PATH)
    
    # Обрабатываем и записываем
    token_data = response.json()
    config['GigaChat']['token'] = token_data.get('access_token', '')

    try:
        with open(config_path, 'w', encoding='utf-8') as file:
            json.dump(config, file, ensure_ascii=True, indent=2)

    except Exception as e:
            print(f"[Токен] Ошибка записи в файл: {e}")

    # Возвращаем токен
    return token_data.get('access_token', '')


def test_token():
    token = config['GigaChat']['token']

    if token != '':

        payload={}
        headers = {
          'Accept': 'application/json',
          'Authorization': f'Bearer {token}'
        }

        response = requests.request("GET", config['GigaChat']['model_url'], headers=headers, data=payload, verify=CERT_PATH)
        if response.status_code == 200:
            return True
        else:
            print(f'{response.status_code}: {response.text}')
            return False


def GigaChat_ask(question = None, token = None):
    if question is None or token is None:
        return question, token

    chat_url = config['GigaChat']['chat_url']

    sys_prompt = config['assistant']['system_prompt']

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    data = {
        "model": config['GigaChat']['gigachat_model'],
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": question}
        ],
        "temperature": config['GigaChat']['temperature'],
        "max_tokens": config['GigaChat']['max_tokens']
    }
    
    response = requests.post(chat_url, headers=headers, json=data, verify=CERT_PATH)

    return response.text


def parse_gigachat_response(response):
    data = json.loads(response)
    try:
        if 'choices' in data and data['choices']:

            config['GigaChat']['all_used_tokens'] = data['usage']['total_tokens']
            with open(config_path, 'w', encoding='utf-8') as file:
                json.dump(config, file, ensure_ascii=False, indent=2)

            return f"{data['choices'][0]['message']['content']}"

        elif 'error' in data:
            return f"Ошибка{data['error']}"
        else:
            return 'Не удалось обработать ответ'

    except json.JSONDecodeError:
        return f'Ошибка: Некоректный Json {response}'

    except Exception as e:
        return f'Ошибка парсинга: {str(e)}'




def processor(prompt = None): 
    # Получение ключа
    api_key = config['GigaChat']['api_key']
    token = config['GigaChat']['token']

    # Проверка есть ли токен, нету - запрашиваем
    if token == '':
        token = get_token(api_key)
        if not test_token():
            print('Ошибка получения токена')

    # Валиден ли токен?
    if not test_token():
        token = get_token(api_key)

    answer = GigaChat_ask(prompt, token)
    return parse_gigachat_response(answer)