# Setup

## Requirements
- Ubuntu 16.04 or higher
- Python 3.5 or higher
    - + `virtualenv`, `gunicorn`
- Node 8.0.0 or higher
- Postgres 9.5 or higher
- `python-certbot-nginx` 

## Postgres Setup
```
sudo -u postgres psql
```

inside psql shell:

```
CREATE DATABASE hjlog;
CREATE USER hjlog WITH PASSWORD 'hjlog';
ALTER ROLE hjlog SET client_encoding TO 'utf8';
ALTER ROLE hjlog SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE hjlog TO hjlog;
```

If there's DB dump file, get the dump (`yyyy-mm-dd.dump`) from S3 bucket and pour it to DB.

```
psql hjlog < yyyy-mm-dd.dump
```

## Gunicorn Service
`/etc/systemd/system/hjlog.service`

```
[Unit]
Description=Gunicorn instance to serve hjlog 
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/hjlog
Environment="PATH=/home/ubuntu/hjlog/venv/bin"
ExecStart=/home/ubuntu/hjlog/venv/bin/gunicorn --workers 3 --bind unix:hjlog.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```

Start and enable the service.

```
$ sudo systemctl start myproject
$ sudo systemctl enable myproject
```

## Nginx
For the configuration content, see `conf/hjlog.conf`

```
sudo cp conf/hjlog.conf /etc/nginx/sites-available/hjlog
sudo ln -s /etc/nginx/sites-available/hjlog /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

For SSL, use certbot. The domain must be directed to the machine's static IP beforhand.

```
sudo certbot --nginx -d hjlog.me -d www.hjlog.me
```

---

## Links
- https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04#create-the-postgresql-database-and-user
- https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04
- https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04
