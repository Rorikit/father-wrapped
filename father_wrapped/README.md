# Папа Wrapped

Интерактивный fullscreen-сайт-подарок в стиле Spotify Wrapped / Яндекс Музыка Итоги года: история про папу, семейные моменты, фото, цитаты, статистика и финальное поздравление.

## Локальный запуск

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Откройте в браузере:

```text
http://127.0.0.1:8000
```

## Открыть на телефоне в одной Wi-Fi сети

1. Узнайте локальный IP компьютера. На Windows можно выполнить:

```powershell
ipconfig
```

Нужен адрес вида `192.168.x.x` или `10.x.x.x`.

2. Запустите сервер так, чтобы он слушал не только `localhost`:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

3. На телефоне, подключённом к той же Wi-Fi сети, откройте:

```text
http://ВАШ-IP:8000
```

Например:

```text
http://192.168.1.25:8000
```

Production-команда для Render:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Где менять контент

- Тексты, статистика, цитаты, карточки и пути к медиа: `app/data/memories.json`
- Фото: `app/static/media/photos/`
- Аудио: `app/static/media/audio/`
- Видео: `app/static/media/video/`

В JSON уже есть демо-данные. Замените пути вроде `/static/media/photos/moment-1.jpg` на свои файлы или положите реальные файлы с такими же именами.

## Деплой на GitHub

1. Создайте новый репозиторий на GitHub.
2. В корне проекта `father_wrapped` выполните:

```bash
git init
git add .
git commit -m "Prepare father wrapped for deploy"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/father-wrapped.git
git push -u origin main
```

Если репозиторий уже создан, достаточно сделать `git add .`, `git commit` и `git push`.

## Деплой на Render

1. Откройте [Render](https://render.com/) и подключите GitHub.
2. Нажмите **New +** -> **Blueprint**.
3. Выберите репозиторий `father-wrapped`.
4. Render прочитает `render.yaml` и создаст web service.
5. Дождитесь завершения build/deploy.

Render использует:

```yaml
buildCommand: pip install -r requirements.txt
startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Как обновлять сайт

1. Измените данные в `app/data/memories.json` или замените файлы в `app/static/media`.
2. Проверьте локально:

```bash
uvicorn app.main:app --reload
```

3. Закоммитьте и отправьте изменения:

```bash
git add .
git commit -m "Update memories"
git push
```

Render автоматически запустит новый deploy после push в GitHub.

## Структура

```text
father_wrapped/
  app/
    main.py
    data/
      memories.json
    templates/
      index.html
      error.html
    static/
      css/
        styles.css
      js/
        app.js
      media/
        photos/
        audio/
        video/
  .gitignore
  render.yaml
  requirements.txt
  README.md
```

## Production notes

- Приложение не использует debug mode.
- Static-файлы подключены через `app.mount("/static", StaticFiles(...))`.
- Templates подключены через `Jinja2Templates`.
- Пути строятся относительно папки `app`, поэтому проект совместим с Linux-средой Render.
