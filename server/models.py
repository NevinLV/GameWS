from django.db import models

class Player(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField('Имя', max_length=50)
    password = models.CharField('Пароль', max_length=50)
    money = models.IntegerField()
    castle = models.CharField('Замок', max_length=1000)

    def __str__(self):
        return self.username


class Map(models.Model):
    level = models.AutoField(primary_key=True)
    attempt_count = models.IntegerField()
    money_count = models.IntegerField()
    castle = models.CharField('Замок', max_length=1000)

    def __str__(self):
        return str(self.level)


class Results(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    stars = models.IntegerField(default=3)
    is_completed = models.BooleanField(default=False)
    attempt = models.IntegerField()

    def __str__(self):
        return self.player
