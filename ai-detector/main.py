from dotenv import load_dotenv
import os
import requests
import sys

load_dotenv()
connect_sid = os.getenv('CONNECT_SID')

def test_ai(inp_text):
    api_url = 'https://quillbot.scribbr.com/api'
    cookies = { 'connect.sid': connect_sid }
    response = requests.post(
        api_url + '/utils/detect-language',
        cookies=cookies,
        json={
            'text': inp_text
        }
    )
    assert response.status_code == 200, print('ERROR_1', response.json())
    language = response.json()['data']['language']
    response = requests.post(
        api_url + '/ai-detector/score',
        cookies=cookies,
        json={
            'text': inp_text,
            'language': language,
            'explain': False,
        }
    )
    assert response.status_code == 200, print('ERROR_2', response.json())
    pers = response.json()['data']['value']['aiScore'] * 100
    print([ pers ])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            inp_text = f.read()
        test_ai(inp_text)
    else:
        print('ERROR_3')
