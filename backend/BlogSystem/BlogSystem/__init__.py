from .celery import app as celery_app

__all__ = ['celery_app']     # 定义 __all__ 变量，用于控制导出的模块