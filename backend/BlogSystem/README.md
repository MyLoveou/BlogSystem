# BlogSystem

## 运行项目
```
cd backend/BlogSystem
# 启动redis
./redis-server.exe
# 启动celery
celery -A BlogSystem worker -l info -P gevent
# 启动celery beat
celery -A BlogSystem beat -l info 
python manage.py runserver
```

