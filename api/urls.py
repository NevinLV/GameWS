from django.urls import path

from .views import Players, PlayerAuth, Maps, GameResults, AllGameResults

urlpatterns = [
    path("results/", GameResults.as_view(), name="game_results"),
    path("results/<int:user_id>/", GameResults.as_view(), name="game_results"),
    path("all-results/", AllGameResults.as_view(), name="game_results"),
    path("player/", Players.as_view(), name="players"),
    path("player-auth/", PlayerAuth.as_view(), name="players"),
    path("maps/", Maps.as_view(), name="maps"),
]
