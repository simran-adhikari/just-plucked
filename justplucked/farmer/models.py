from django.db import models
from django_countries.fields import CountryField
import uuid
from django.contrib.auth.models import User

class Farmer(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('widowed', 'Widowed'),
        ('divorced', 'Divorced'),
    ]

    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Personal Info
    full_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)

    # Contact Info
    phone = models.CharField(max_length=20, unique=True)
    alternate_phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    # Address Info
    country = CountryField()
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    municipality = models.CharField(max_length=100, null=True, blank=True)
    ward_no = models.CharField(max_length=10, null=True, blank=True)
    street_address = models.TextField()

    # Identification
    nid_number = models.CharField("National ID", max_length=50, unique=True, null=True, blank=True)
    nid_document = models.FileField(upload_to='documents/nid/', null=True, blank=True)

    # Bank Details
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    bank_account_number = models.CharField(max_length=50, null=True, blank=True)
    bank_branch = models.CharField(max_length=100, null=True, blank=True)

    # Profile Image
    profile_picture = models.ImageField(upload_to='farmers/profile_pics/', null=True, blank=True)

    # Farming Details
    land_area_in_acres = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    primary_crop = models.CharField(max_length=100, null=True, blank=True)
    farming_experience_years = models.PositiveIntegerField(null=True, blank=True)

    # Status and Metadata
    is_active = models.BooleanField(default=True)
    verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)


    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        ordering = ['-date_joined']
        verbose_name = "Farmer"
        verbose_name_plural = "Farmers"

    def __str__(self):
        return f"{self.full_name} - {self.phone}"


class Farm(models.Model):
    FARM_TYPE_CHOICES = [
        ('organic', 'Organic'),
        ('conventional', 'Conventional'),
        ('mixed', 'Mixed'),
    ]

    id = models.BigAutoField(primary_key=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=100)
    location_description = models.TextField()
    farm_type = models.CharField(max_length=20, choices=FARM_TYPE_CHOICES)
    land_area_in_acres = models.DecimalField(max_digits=10, decimal_places=2)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    established_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.farmer.full_name})"


class FarmerDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('nid', 'National ID'),
        ('land_ownership', 'Land Ownership Certificate'),
        ('tax', 'Tax Clearance'),
        ('other', 'Other'),
    ]

    id = models.BigAutoField(primary_key=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPE_CHOICES)
    document_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='farmers/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} - {self.farmer.full_name}"


class CropProduction(models.Model):
    id = models.BigAutoField(primary_key=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='crop_productions')
    crop_name = models.CharField(max_length=100)
    season = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    yield_quantity_kg = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.crop_name} - {self.year} ({self.farm.name})"


class Certification(models.Model):
    id = models.BigAutoField(primary_key=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=100)
    issuing_authority = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    certificate_file = models.FileField(upload_to='farmers/certifications/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.farmer.full_name}"