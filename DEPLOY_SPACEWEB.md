# Деплой на SpaceWeb

Проект подготовлен для двух сценариев:

- **SpaceWeb shared hosting с Apache mod_wsgi**: основной вариант для обычного виртуального хостинга.
- **VPS/сервер с SSH и systemd**: альтернативный вариант, если у вас есть root/sudo.

## Что нужно уточнить в панели SpaceWeb

Перед фактическим деплоем нужны данные, которых пока нет:

- включён ли SSH в тарифе;
- SSH host, user и port;
- путь к директории сайта на сервере;
- доступная команда Python: `python3.11`, `python3`, или другая;
- где в панели меняется обработчик домена на Python/mod_wsgi;
- можно ли выбрать document root для домена `arsyredgma.temp.swtest.ru`.

Без этих данных нельзя безопасно выполнить копирование и настройку на сервере.

## Вариант A: SpaceWeb shared hosting / Apache mod_wsgi

Этот вариант подходит, если нет root/sudo и нельзя запускать постоянный `uvicorn`-процесс.

В проект добавлены:

- `wsgi.py` — WSGI entry point для Apache mod_wsgi;
- `.htaccess` — rewrite на `wsgi.py`;
- `a2wsgi` в `requirements.txt` — адаптер FastAPI ASGI -> WSGI.

### Настройка в панели

1. Откройте `https://cp.sweb.ru/hosting`.
2. Перейдите в настройки сайта/домена `arsyredgma.temp.swtest.ru`.
3. Включите Python/WSGI, если эта опция доступна.
4. Укажите версию Python 3.11, если есть выбор.
5. Укажите корень приложения: директория, куда загружен репозиторий.
6. Укажите startup/entry file: `wsgi.py`.
7. Укажите callable/entry point: `application`.
8. Убедитесь, что `.htaccess` загружен в корень сайта.

### Загрузка через Git по SSH

На сервере:

```bash
git clone https://github.com/Rorikit/father-wrapped.git ~/father-wrapped
cd ~/father-wrapped
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
```

Если SSH недоступен, загрузите эти файлы через файловый менеджер панели или FTP/SFTP:

```text
app/
tests/
.gitignore
.htaccess
DEPLOY_SPACEWEB.md
README.md
deploy.sh
render.yaml
requirements.txt
wsgi.py
```

Не загружайте `.venv/`, `.git/`, `.pytest_cache/`, `__pycache__/`, локальные пароли и приватные ключи.

## Вариант B: VPS / SSH + systemd + nginx

Этот вариант подходит только если есть root/sudo.

Установка:

```bash
sudo mkdir -p /var/www/father-wrapped
sudo chown "$USER":"$USER" /var/www/father-wrapped
git clone https://github.com/Rorikit/father-wrapped.git /var/www/father-wrapped
cd /var/www/father-wrapped
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pytest -q
```

Проверка запуска:

```bash
.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Пример systemd service:

```ini
[Unit]
Description=father-wrapped FastAPI app
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/father-wrapped
Environment=PATH=/var/www/father-wrapped/.venv/bin
ExecStart=/var/www/father-wrapped/.venv/bin/gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Пример nginx:

```nginx
server {
    listen 80;
    server_name arsyredgma.temp.swtest.ru;

    location /static/ {
        alias /var/www/father-wrapped/app/static/;
        expires 7d;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Повторный деплой

Через SSH:

```bash
cd ~/father-wrapped
git pull --ff-only
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

Для shared hosting/mod_wsgi обычно достаточно обновить файлы. Если панель SpaceWeb даёт кнопку перезапуска Python-приложения, нажмите её. Если нет, измените timestamp `wsgi.py`:

```bash
touch wsgi.py
```

Для VPS/systemd:

```bash
sudo systemctl restart father-wrapped
sudo systemctl status father-wrapped
```

## Проверка после деплоя

```bash
curl -I https://arsyredgma.temp.swtest.ru/
curl -I https://arsyredgma.temp.swtest.ru/static/css/styles.css
curl -I https://arsyredgma.temp.swtest.ru/static/js/app.js
curl -I https://arsyredgma.temp.swtest.ru/static/media/photos/demo-memory.svg
```

Ожидаемо: `200 OK` для главной и static-файлов.

## Логи

Shared hosting:

- смотрите раздел логов Apache/Python в панели SpaceWeb;
- если есть SSH, проверьте файлы логов, которые указывает панель.

VPS/systemd:

```bash
sudo journalctl -u father-wrapped -n 100 --no-pager
sudo journalctl -u father-wrapped -f
sudo tail -n 100 /var/log/nginx/error.log
```

## Если сайт не открывается

1. Проверьте, что домен `arsyredgma.temp.swtest.ru` привязан к нужному сайту в панели.
2. Проверьте, что загружены `app/`, `wsgi.py`, `.htaccess`, `requirements.txt`.
3. Проверьте, что зависимости установлены в виртуальное окружение.
4. Проверьте, что `wsgi.py` импортируется:

```bash
python -c "from wsgi import application; print(application)"
```

5. Если главная открывается без CSS/JS, проверьте доступность `/static/css/styles.css`.
6. Если ошибка 500, смотрите Python/Apache logs в панели.
