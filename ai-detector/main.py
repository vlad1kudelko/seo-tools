from dotenv import load_dotenv
import os
import requests
import sys
import time

#  https://www.scribbr.com/ai-detector/

load_dotenv()
connect_sid = os.getenv('CONNECT_SID')

def get_md(inp_file):
    ret = []
    with open(inp_file) as f:
        lines = f.readlines()
        lines = list(map(str.rstrip, lines))
        if len(lines) > 0 and lines[0] == '---':
            is_toml = True
            for line in lines[1:]:
                if line == '---':
                    is_toml = False
                    continue
                else:
                    if not is_toml:
                        ret.append(line)
        else:
            raise Exception('ERROR parse')
    return '\n'.join(ret)

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
    assert response.status_code == 200, print('ERROR_1', response)
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
    assert response.status_code == 200, print('ERROR_2', response)
    pers = response.json()['data']['value']['aiScore'] * 100
    return [ int(pers) ]

def test_ai_wrap(inp_file):
    inp_text = get_md(inp_file)
    inp_text = ' '.join(inp_text.split()[:1200])
    return test_ai(inp_text)

def test_dir(inp_dir):
    for root, dirs, files in os.walk(inp_dir):
        for file in files:
            filename = f'{root}/{file}'
            print(test_ai_wrap(filename), filename)
            time.sleep(1)

def main():
    if len(sys.argv) > 1:
        if os.path.isdir(sys.argv[1]):
            test_dir(sys.argv[1])
        else:
            print(test_ai_wrap(sys.argv[1]))
    else:
        print('ERROR_3')

if __name__ == '__main__':
    main()
