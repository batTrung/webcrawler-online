# webcrawler-online

## Cài đặt

Đầu tiên, tải repository về máy tính:

```bash
git clone https://github.com/batTrung/webcrawler-online.git
```

Cài đặt requirements:

```bash
cd webcrawler-online
pip install -r requirements.txt
```

Tạo database:

```bash
python manage.py migrate
```

Chạy development server:

```bash
python manage.py runserver
```

Mở terminal mới để chạy Celery:

```bash
celery -A myproject worker -l info
```

Mở Chrome hay FireFox : **localhost:8000**

## DEMO

[DEMO]

[DEMO]: https://webcrawler-online.herokuapp.com/

