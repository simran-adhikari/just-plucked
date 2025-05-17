from django.db import models
from django.utils.text import slugify


class Country(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, verbose_name="Country Name")
    iso_code = models.CharField(max_length=5, blank=True, null=True, verbose_name="ISO Code")
    active = models.BooleanField(default=True, verbose_name="Is Active")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ['name']

    def __str__(self):
        return self.name


class State(models.Model):
    id = models.BigAutoField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Country")
    name = models.CharField(max_length=100, verbose_name="State/Province Name")
    active = models.BooleanField(default=True, verbose_name="Is Active")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
        unique_together = ("country", "name")
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.country.name}"


class District(models.Model):
    id = models.BigAutoField(primary_key=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, verbose_name="State")
    name = models.CharField(max_length=100, verbose_name="District Name")
    active = models.BooleanField(default=True, verbose_name="Is Active")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.state.name}"


class City(models.Model):
    id = models.BigAutoField(primary_key=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="District")
    name = models.CharField(max_length=100, verbose_name="City Name")
    active = models.BooleanField(default=True, verbose_name="Is Active")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        ordering = ['name']

    def __str__(self):
        return f"{self.name}, {self.district.name}"


class UnitOfMeasure(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Unit Name")
    symbol = models.CharField(max_length=20, verbose_name="Symbol")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    active = models.BooleanField(default=True, verbose_name="Is Active")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Unit of Measure"
        verbose_name_plural = "Units of Measure"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class Bank(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name="Bank Name")
    swift_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="SWIFT Code")
    active = models.BooleanField(default=True, verbose_name="Is Active")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Bank"
        verbose_name_plural = "Banks"
        ordering = ['name']

    def __str__(self):
        return self.name


class BankBranch(models.Model):
    id = models.BigAutoField(primary_key=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, verbose_name="Bank")
    branch_name = models.CharField(max_length=150, verbose_name="Branch Name")
    location = models.CharField(max_length=150, blank=True, null=True, verbose_name="Location")
    ifsc_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="IFSC Code")
    active = models.BooleanField(default=True, verbose_name="Is Active")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Bank Branch"
        verbose_name_plural = "Bank Branches"
        ordering = ['branch_name']

    def __str__(self):
        return f"{self.bank.name} - {self.branch_name}"


class Category(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name="Category Name")
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True, verbose_name="Slug")
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategories',
        verbose_name="Parent Category"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    active = models.BooleanField(default=True, verbose_name="Is Active")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
 


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Tag Name")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Product Tag"
        verbose_name_plural = "Product Tags"

    def __str__(self):
        return self.name


class FarmingPracticeType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Farming Practice")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    active = models.BooleanField(default=True, verbose_name="Is Active")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Farming Practice"
        verbose_name_plural = "Farming Practices"
        ordering = ['name']

    def __str__(self):
        return self.name


class CropType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Crop Type")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Category")
    active = models.BooleanField(default=True, verbose_name="Is Active")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Crop Type"
        verbose_name_plural = "Crop Types"
        ordering = ['name']

    def __str__(self):
        return self.name


class LivestockType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Livestock Type")
    active = models.BooleanField(default=True, verbose_name="Is Active")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Livestock Type"
        verbose_name_plural = "Livestock Types"
        ordering = ['name']

    def __str__(self):
        return self.name


class CertificationBody(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name="Certification Body")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Country")
    active = models.BooleanField(default=True, verbose_name="Is Active")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Certification Body"
        verbose_name_plural = "Certification Bodies"
        ordering = ['name']

    def __str__(self):
        return self.name
