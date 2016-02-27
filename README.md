# hjlog
**HJ**s' lifelog

## Basic dependency
- Python 3.4 or higher
- node 5.x & npm

## Production

``` bash
source venv/bin/activate          # 가상 환경 활성화

pip3 install -r requirements.txt  # 파이썬 디펜던시 설치
npm install                       # npm 디펜던시 설치
WEBPACK=release npm run build     # Webpack 빌드

sudo service hjlog start          # 프로덕션 서버 시작
```

## Development

```bash
source venv/bin/activate              # 가상 환경 활성화

pip3 install -r dev_requirements.txt  # 파이썬 개발 디펜던시 설치
npm install                           # npm 디펜던시 설치
npm run build                         # Webpack 빌드

touch hjlog.db                        # 테스트용 SQLite3 디비 생성
export RUN_OPT=../dev_config.py       # 환경 변수 설정

python dev_run.py                     # 개발 서버 시작
```
