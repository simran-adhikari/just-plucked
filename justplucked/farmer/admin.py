from django.contrib import admin
from .models import Farmer, Farm, FarmerDocument, Certification
from django.core.mail import send_mail
from django.contrib.auth.models import User,Group
from django.conf import settings

class FarmerDocumentInline(admin.TabularInline):
    model = FarmerDocument
    extra = 1
    verbose_name = "Document"
    verbose_name_plural = "Documents"


class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 1
    verbose_name = "Certification"
    verbose_name_plural = "Certifications"


class FarmInline(admin.TabularInline):
    model = Farm
    extra = 1
    verbose_name = "Farm"
    verbose_name_plural = "Farms"


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "email", "country", "primary_crop", "verified", "is_active")
    list_filter = ("verified", "is_active", "country", "gender", "marital_status")
    search_fields = ("full_name", "phone", "email", "nid_number", "district", "municipality")
    ordering = ("-date_joined",)
    readonly_fields = ("uuid", "date_joined", "last_updated")
    actions=["approve_farmer",]

    inlines = [FarmInline, FarmerDocumentInline, CertificationInline]

    fieldsets = (
        ("Basic Information", {
            "fields": ("full_name", "gender", "date_of_birth", "marital_status", "profile_picture","user")
        }),
        ("Contact", {
            "fields": ("phone", "alternate_phone", "email")
        }),
        ("Location", {
            "fields": ("country", "state", "district", "municipality", "ward_no", "street_address")
        }),
        ("Identification", {
            "fields": ("nid_number", "nid_document")
        }),
        ("Banking", {
            "fields": ("bank_name", "bank_account_number", "bank_branch")
        }),
        ("Farming Details", {
            "fields": ("land_area_in_acres", "primary_crop", "farming_experience_years")
        }),
        ("Status", {
            "fields": ("verified", "is_active", "uuid", "date_joined", "last_updated")
        }),
    )
    def approve_farmer(self, request, queryset):
        for farmer in queryset:
            # Set the farmer as active
            farmer.is_active = True
            farmer.save()

            # Create a user for the farmer
            user = User.objects.create_user(
                username=farmer.phone,  # Using phone as username
                email=farmer.email,
                password='temporarypassword'  # Create a random password or generate one
            )

            # Assign the "farmer" group to the user
            farmer_group = Group.objects.get(name='farmer')  # Assuming you have a "farmer" group
            user.groups.add(farmer_group)

            # Send email to the farmer
            send_mail(
                'Welcome to Farmer Portal',
                f'Your account has been approved. Use this temporary password to log in: temporarypassword',
                settings.EMAIL_HOST_USER,
                [farmer.email],
                fail_silently=False,
            )

            self.message_user(request, "Selected farmers have been approved and notified.")

    approve_farmer.short_description = "Approve selected farmers"


 