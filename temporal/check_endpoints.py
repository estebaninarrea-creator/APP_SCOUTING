import requests
paths=['/roles/','/clubes/','/ligas/','/torneos/','/partidos/','/usuarios/']
for path in paths:
    try:
        r = requests.get('http://127.0.0.1:8001' + path, timeout=8)
        print(path, r.status_code)
        print(r.text[:800])
        print('---')
    except Exception as e:
        print(path, 'ERROR', e)
        print('---')
