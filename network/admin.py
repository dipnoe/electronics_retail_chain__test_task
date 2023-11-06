from django.contrib import admin

from network.models import NetworkElement, Contact, Product


@admin.register(NetworkElement)
class NetworkElementAdmin(admin.ModelAdmin):
    list_display = ['name', 'contacts', 'provider', 'debt', 'created_at', 'level']
    list_display_links = ['name', 'provider']
    list_filter = ['provider__contacts__city']
    actions = ["clear_debt"]

    @admin.action(description="clears the debt to the supplier for selected objects")
    def clear_debt(self, request, queryset):
        queryset.update(debt=0)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['email', 'country', 'city', 'street', 'building_num']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'launch_date']
