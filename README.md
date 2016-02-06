# hjlog
**HJ**s' lifelog

## Production

1. 가상환경 활성화 &  디펜던시 설치
  ``` bash
  source venv/bin/activate
  pip3 install -r requirements.txt
  ```

2. 서버 시작
  ``` bash
  sudo service hjlog start
  ```

## Development

1. 가상환경, 디펜던시, 디비 및 환경변수 설정
  ```bash
  source venv/bin/activate
  pip3 install -r dev_requirements.txt
  touch hjlog.db
  export RUN_OPT=../dev_config.py
  ```

2. 서버 시작
  ``` bash
  python dev_run.py
  ```
