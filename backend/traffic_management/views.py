from datetime import timedelta


from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from models.models import DrivingLocation, User
from apscheduler.schedulers.background import BackgroundScheduler

import logging


logger = logging.getLogger(__name__)

def disable_old_locations():
    print("Running disable_old_locations task")
    time_threshold = timezone.now() - timedelta(seconds=40)
    old_locations = DrivingLocation.objects.filter(update_time__lt=time_threshold)
    old_locations.update(is_disabled=True)
    print("Disabled {} old locations".format(len(old_locations)))
def delete_disabled_locations():
    print("Running delete_disabled_locations task")
    disabled_locations = DrivingLocation.objects.filter(is_disabled=True)
    count = disabled_locations.count()
    disabled_locations.delete()
    print("Deleted {} disabled locations".format(count))

class TrafficView(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def get_driving_location(self, request):
        time_threshold = timezone.now() - timedelta(seconds=30)
        print(time_threshold)
        locations = DrivingLocation.objects.filter(is_disabled=False, update_time__gte=time_threshold)
        print(locations.explain())
        locations_list = []
        for loc in locations:
            try:
                user = User.objects.get(username=loc.username)
            except User.DoesNotExist:
                user_role = 'public'
            else:
                user_role = user.role
            locations_list.append({
                "username": loc.username,
                "latitude": loc.latitude,
                "longitude": loc.longitude,
                "user_role": user_role
            })
        if locations_list is None or len(locations_list) == 0:
            return JsonResponse({"status": "error", "message": "No location data available."})

        return JsonResponse({"status": "success", "locations": locations_list})

    @action(detail=False, methods=['post'])
    def save_driving_location(self, request):
        # username = request.data.get("username")
        # 如果用户已登录，使用用户名，否则使用 session ID
        username = request.user.username if request.user.is_authenticated else request.session.session_key
        # 如果 session ID 不存在，创建一个新的 session
        if username is None:
            request.session.create()
            username = request.session.session_key
        print(username)
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        if username is None or latitude is None or longitude is None:
            return JsonResponse({"status": "error", "message": "Invalid request."})

        try:
            location = DrivingLocation.objects.get(username=username)
            location.latitude = latitude
            location.longitude = longitude
            location.update_time = timezone.now()
            location.is_disabled = False
            location.save()
        except DrivingLocation.DoesNotExist:
            DrivingLocation.objects.create(username=username, latitude=latitude, longitude=longitude,
                                           update_time=timezone.now())

        return JsonResponse({"status": "success", "message": "Location saved successfully."})
