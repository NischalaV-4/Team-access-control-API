from django.contrib import admin
from .models import Organization, OrganizationMembership


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):

    list_display = ('id','name','created_at',)
    search_fields = ('name',)

@admin.register(OrganizationMembership)
class OrganizationMembershipAdmin(admin.ModelAdmin):

    list_display = ('id','user','organization','role','created_at',)

    list_filter = ('role',)

    search_fields = ('user__username','organization__name',)
