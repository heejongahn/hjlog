# hjlog
**HJ**s' lifelog

## Basic dependency
- Python 3.4 or higher
- node 5.x & npm

## Production

``` bash
source venv/bin/activate           # 가상 환경 활성화

pip3 install -r requirements.txt   # 파이썬 디펜던시 설치
npm install                        # npm 디펜던시 설치
npm run release                    # Webpack 릴리즈용 빌드

sudo service hjlog start           # 프로덕션 서버 시작
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

## /etc/nginx/sites-available

```nginx
server {
    client_max_body_size 16M;

    listen 443 ssl;

    server_name hjlog.me www.hjlog.me;

    ssl_certificate /etc/letsencrypt/live/hjlog.me/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/hjlog.me/privkey.pem;

    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_prefer_server_ciphers on;
    ssl_ciphers 'EECDH+AESGCM:EDH+AESGCM:ECDHE-RSA-AES128-GCM-SHA256:AES256+EECDH:DHE-RSA-AES128-GCM-SHA256:AES256+EDH:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-RSA-AES128-SHA256:ECDHE-RSA-AES256-SHA:ECDHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES128-SHA256:DHE-RSA-AES256-SHA:DHE-RSA-AES128-SHA:ECDHE-RSA-DES-CBC3-SHA:EDH-RSA-DES-CBC3-SHA:AES256-GCM-SHA384:AES128-GCM-SHA256:AES256-SHA256:AES128-SHA256:AES256-SHA:AES128-SHA:DES-CBC3-SHA:HIGH:!aNULL:!eNULL:!EXPORT:!DES:!MD5:!PSK:!RC4!EDH';

    error_log /var/log/nginx/error.log error;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/ubuntu/workspace/hjlog/hjlog.sock;
    }
}

server {
    listen 80;
    server_name hjlog.me;

    location ~ /.well-known {
        allow all;
    }

    return 301 https://$host$request_uri;
}
```

## /etc/init/hjlog.conf

```
description "uWSGI server instance configured to serve hjlog"

start on runlevel [2345]
stop on runlevel [!2345]

setuid ubuntu
setgid www-data

env PATH=/home/ubuntu/workspace/hjlog/venv/bin
chdir /home/ubuntu/workspace/hjlog
exec uwsgi --ini hjlog.ini
```
