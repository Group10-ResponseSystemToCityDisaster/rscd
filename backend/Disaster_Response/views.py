from django.shortcuts import render
from django.views import View
from rest_framework import viewsets
from rest_framework.decorators import action


from django.http import JsonResponse
import json


class DisasterView(viewsets.ViewSet):
    @action(detail=False, methods=['post', 'get'])
    def post_location(self, request, pk=None):
        try:
            # 将请求的 JSON 转换成 Python 字典
            data = request.data

            # 提取纬度和经度数据
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            # 在这里处理数据（例如，保
            # 返回成功响应
            return JsonResponse({"status": "success", "message": "Location received successfully."})
        except json.JSONDecodeError:
            # 如果请求的内容不是有效的 JSON，返回错误响应
            return JsonResponse({"status": "error", "message": "Invalid JSON."}, status=400)
        except Exception as e:
            # 处理其他意外错误
            return JsonResponse({"status": "error", "message": str(e)}, status=500)