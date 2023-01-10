import json
from operator import itemgetter

from django.shortcuts import render

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView

from server.models import Results, Player, Map


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'username', 'password', 'money', 'castle']


class Players(APIView):
    def post(self, request):
        player_data = request.data

        if "username" in player_data:
            if "password" in player_data:
                res = Player(username=player_data["username"], password=player_data["password"], money=100)
                res.save()
                return Response({"id": res.id, "username": res.username, "password": res.password,}, HTTP_201_CREATED)
            else:
                return Response({"msg": "Не указано поле password"}, HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "Не указано поле username"}, HTTP_400_BAD_REQUEST)

    def get(self, request):
        players = []
        for player in Player.objects.all():
            players.append({
                "id": player.id,
                "username": player.username,
                "password": player.password,
                "money": player.money,
                "castle": player.castle
            })

        return Response(players, HTTP_200_OK)


class Maps(APIView):
    def get(self, request):
        maps = []
        for map in Map.objects.all():
            print(map.castle)
            jj = json.loads(map.castle)

            maps.append({
                "level": map.level,
                "attempt_count": map.attempt_count,
                "money_count": map.money_count,
                "castle": jj,
            })

        return Response(maps, HTTP_200_OK)


class PlayerAuth(APIView):
    def post(self, request):
        player_data = request.data

        if "username" in player_data:
            if "password" in player_data:
                player_qs = Player.objects.filter(username=player_data["username"], password=player_data["password"])
                if player_qs.exists():
                    player = Player.objects.get(username=player_data["username"], password=player_data["password"])
                    return Response({"id": player.id}, HTTP_200_OK)
                else:
                    return Response({"msg": "Неверный username или пароль"}, HTTP_400_BAD_REQUEST)
            else:
                return Response({"msg": "Не указано поле password"}, HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg": "Не указано поле username"}, HTTP_400_BAD_REQUEST)


class GameResults(APIView):
    def post(self, request):
        result = request.data
        player_qs = Player.objects.filter(id=result["id"])

        if player_qs.exists():
            player = Player.objects.get(id=result["id"])
            game_map = Map.objects.get(level=result["level"])

            res = Results(player=player, map=game_map, stars=result["stars"], is_completed=result["is_completed"], attempt=result["attempt"])
            res.save()
            return Response({"msg": "Результат сохранён"}, HTTP_201_CREATED)
        else:
            return Response({"msg": "Игрока с таким id не существует"}, HTTP_400_BAD_REQUEST)

    def get(self, request, user_id):
        user_result = 0
        for result in Results.objects.all():
            if result.player.id == user_id:
                user_result += result.stars

        return Response(user_result, HTTP_200_OK)

class AllGameResults(APIView):
    def get(self, request):
        all_results = []

        all_player = Player.objects.all()
        for player in all_player:
            user_result = 0
            for result in Results.objects.all():
                if result.player.id == player.id:
                    user_result += result.stars
            all_results.append({
                "user_id": player.id,
                "username": player.username,
                "stars": user_result
            })
        all_results.sort(key=itemgetter('stars'))
        all_results.reverse()
        return Response(all_results, HTTP_200_OK)



