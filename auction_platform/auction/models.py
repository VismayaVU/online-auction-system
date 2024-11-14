from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


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


class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


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


# Model for storing deleted items
class DeletedItem(models.Model):
    item_id = models.IntegerField()  # Keeping original item_id for reference
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    item_description = models.TextField()
    deleted_on = models.DateTimeField(null=True, blank=True, default=timezone.now)  # Timestamp for deletion

    def __str__(self):
        return f"Item ID:{self.item_id} || Name:{self.name} || Price:{self.price} || Desc:{self.item_description}"


# Model for storing deleted auctions
class DeletedAuction(models.Model):
    auction_id = models.IntegerField()  # Keeping original auction_id for reference
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=100)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    seller_id = models.IntegerField()  # Store seller_id directly or link to user model if needed
    item_id = models.IntegerField()  # Keep reference to the original item_id
    deleted_on = models.DateTimeField(null=True, blank=True, default=timezone.now)  # Timestamp for deletion

    def __str__(self):
        return f"AuctionID:{self.auction_id} || Name:{self.title} || Starting Bid:{self.starting_bid} || Current Bid:{self.current_bid} || SellerID:{self.seller_id} || ItemID:{self.item_id}"


# Model for storing deleted bids
class DeletedBid(models.Model):
    bid_id = models.IntegerField()  # Keeping original bid_id for reference
    bid_time = models.DateTimeField()
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    auction_id = models.IntegerField()  # Keep reference to the original auction_id
    bidder_id = models.IntegerField()  # Store bidder_id directly or link to user model if needed
    deleted_on = models.DateTimeField(null=True, blank=True, default=timezone.now)  # Timestamp for deletion

    def __str__(self):
        return f"BidID:{self.bid_id} || Bid Amount:{self.bid_amount} || AuctionID:{self.auction_id} || BidderID:{self.bidder_id}"
