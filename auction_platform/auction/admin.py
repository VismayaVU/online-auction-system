from django.contrib import admin
from .models import Auction, Item, Bid, Review, Tag, AuctionTag, Admin, AdminApproval

admin.site.register(Auction)
admin.site.register(Item)
admin.site.register(Bid)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(AuctionTag)
admin.site.register(Admin)
admin.site.register(AdminApproval)
