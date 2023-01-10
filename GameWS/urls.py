from django.contrib import admin
from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from server.models import Player


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ['url', 'username', 'password', 'castle', 'money']


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register(r'players', PlayerViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path("api/v1/", include("api.urls")),
]