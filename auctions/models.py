from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=280, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField(max_length = 200, default="https://i.imgur.com/Jlb60R5.png")
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="createds", default=2)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="won", null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE , related_name='categories', null=True)

    def __str__(self):
        return f"{self.title}: ${self.price}"

class Watchlist(models.Model):
    watcher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    body = models.TextField(max_length=280, default="")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment by {self.author} on {self.listing.title}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids", default=2)
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")

    def __str__(self):
        return f"{self.bid} on item no. {self.listing.title}"