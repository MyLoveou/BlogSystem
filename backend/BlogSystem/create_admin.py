#!/usr/bin/env python


# # 设置 Django 环境


from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BlogSystem.settings")
django.setup()
User = get_user_model()

def create_superuser():
    username = "admin"
    email = "admin@example.com"
    password = "admin123456"  # 可自行修改

    if User.objects.filter(username=username).exists():
        print(f"用户 {username} 已存在，跳过创建。")
        return

    User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print("✅ 超级用户创建成功！")
    print(f"  用户名: {username}")
    print(f"  邮箱: {email}")
    print(f"  密码: {password}")

if __name__ == "__main__":
    create_superuser()