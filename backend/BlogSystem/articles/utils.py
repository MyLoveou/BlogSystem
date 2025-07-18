from pypinyin import lazy_pinyin, Style
from django.utils.text import slugify

def generate_unique_slug(model, base_value, field_name='slug'):
    """
    将中文转拼音并生成唯一 slug
    :param model: 要查重的 Django 模型
    :param base_value: 原始字符串（可能含中文）
    :param field_name: 唯一字段名，默认 'slug'
    :return: 唯一 slug
    """
    # 1. 中文 → 拼音（带连字符，如 "ni-hao-shi-jie"）
    pinyin = slugify('-'.join(lazy_pinyin(base_value)))
    # 2. 兜底
    base = pinyin or 'untitled'
    candidate = base
    counter = 1
    while model.objects.filter(**{field_name: candidate}).exists():
        candidate = f"{base}-{counter}"
        counter += 1
    return candidate