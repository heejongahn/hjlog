# hjlog
**HJ**s' lifelog

## Production

0. 가상환경 활성화

1. 패키지 설치
  ``` bash
  pip3 install -r requirements.txt
  ```

2. 서버 시작
  ``` bash
  sudo service hjlog start
  ```

## Development

0. 가상환경 활성화

1. 패키지 설치 및 환경 변수 설정
  ```bash
  pip3 install -r dev_requirements.txt
  export RUN_OPT=../dev_config.py
  ```

2. 디비 및 더미 유저 생성
  ``` bash
  touch hjlog.db
  ```

  (in python console)
  ```python
  from hjlog import db
  from hjlog.models import User

  u = User()
  u.username = 'admin'
  u.password = 'supersecret'

  db.create_all()
  db.session.add(u)
  db.session.commit()
  ```

3. 서버 시작
  ``` bash
  python dev_run.py
  ```
