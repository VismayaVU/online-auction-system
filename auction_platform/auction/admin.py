# auction/admin.py

from django.urls import path
from django.contrib import admin
from .models import Auction, AdminApproval, Admin, User, Item
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from django.db import connection


def approve_auction_view(request, auction_id):
    auction = get_object_or_404(Auction, pk=auction_id)
    if auction.status == 'Pending':
        auction.status = 'Approved'
        auction.save()

        # Retrieve the corresponding Admin instance based on the logged-in User
        admin_instance = Admin.objects.get(admin_email=request.user.email)

        # Log the approval in AdminApproval model
        AdminApproval.objects.create(
            admin=admin_instance,
            item=auction.item,
            approved_on=timezone.now(),
            is_approved=True
        )
        messages.success(request, f"Auction {auction.item} has been approved.")
    return redirect('admin:auction_auction_changelist')


class AuctionAdmin(admin.ModelAdmin):
    list_display = ['auction_id', 'status', 'item', 'approve_button']
    list_filter = ['status']
    actions = ['approve_auctions']

    def approve_button(self, obj):
        if obj.status == 'Pending':
            return format_html(
                '<a class="button" href="{}">Approve</a>',
                reverse('admin:approve_auction', args=[obj.auction_id])
            )
        return "Approved"

    approve_button.short_description = "Approve Auction"

    def approve_auctions(self, request, queryset):
        for auction in queryset:
            if auction.status == 'Pending':
                auction.status = 'Approved'
                auction.save()
                AdminApproval.objects.create(
                    admin=request.user,
                    item=auction.item,
                    approved_on=timezone.now(),
                    is_approved=True
                )
        self.message_user(request, "Selected auctions have been approved.")

    approve_auctions.short_description = "Approve selected auctions"

    def delete_model(self, request, obj):
        # Save the deleted auction record to deleted_auctions
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO deleted_auctions (auction_id, title, description, start_time, end_time, status, starting_bid, current_bid, seller_id, item_id, deleted_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                [
                    obj.auction_id, obj.title, obj.description, obj.start_time,
                    obj.end_time, obj.status, obj.starting_bid, obj.current_bid,
                    obj.seller_id, obj.item_id, timezone.now()
                ]
            )
        # Delete the original auction
        super().delete_model(request, obj)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')

    def delete_model(self, request, obj):
        # Save the deleted user record to deleted_users
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO deleted_users (user_id, username, email, first_name, last_name, deleted_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                [obj.id, obj.username, obj.email, obj.first_name, obj.last_name, timezone.now()]
            )
        # Delete the original user
        super().delete_model(request, obj)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'name', 'price')
    search_fields = ('name',)

    def delete_model(self, request, obj):
        # Save the deleted item record to deleted_items
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO deleted_items (item_id, name, description, starting_price, deleted_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                [obj.item_id, obj.name, obj.description, obj.price, timezone.now()]
            )
        # Delete the original item
        super().delete_model(request, obj)


# Register the models with custom admin classes
admin.site.register(Item, ItemAdmin)
admin.site.register(Auction, AuctionAdmin)


# Custom admin URLs
original_admin_get_urls = admin.site.get_urls


def get_admin_urls():
    urls = original_admin_get_urls()
    custom_urls = [
        path('auction/approve/<int:auction_id>/', approve_auction_view, name='approve_auction'),
    ]
    return custom_urls + urls


admin.site.get_urls = get_admin_urls
