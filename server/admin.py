from django.contrib import admin
from .models import Player, Map, Results

admin.site.register(Player)
admin.site.register(Map)

@admin.register(Results)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("player", "map", "stars", "is_completed", "attempt")
