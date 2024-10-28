from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Auction(models.Model):
    auction_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=100)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="seller_auctions")
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name="auctions")  # ForeignKey to Item
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Auction for {self.title} ({self.item.name})"


class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item_description = models.TextField()

    def __str__(self):
        return self.name


class Bid(models.Model):
    bid_id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid_time = models.DateTimeField(auto_now_add=True)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField()
    reviewed_on = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class AuctionTag(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    assigned_on = models.DateTimeField(auto_now_add=True)


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_email = models.EmailField(unique=True)
    admin_name = models.CharField(max_length=100)
    admin_password = models.CharField(max_length=100)  # Store encrypted in production

    def __str__(self):
        return self.admin_name


class AdminApproval(models.Model):
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    approved_on = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

