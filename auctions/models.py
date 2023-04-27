from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watchlist = models.ManyToManyField('Asset', blank=True, related_name="watchlist")

class Bid(models.Model):
    price = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE, related_name="bid")

    def __str__(self):
        return f"'{self.price}' by {self.user.username} at {self.date.strftime('%Y-%m-%d %H:%M:%S')}"

class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey('Asset', on_delete=models.CASCADE, related_name="comment")

class Asset(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    open = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="img")