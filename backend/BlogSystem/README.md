# BlogSystem

## 运行项目
```
cd backend/BlogSystem
celery -A BlogSystem worker -l info -P gevent
celery -A BlogSystem beat -l info 
python manage.py runserver
```

