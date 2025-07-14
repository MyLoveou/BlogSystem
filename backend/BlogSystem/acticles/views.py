from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def test(request):
    return HttpResponse("测试项目搭建成功")