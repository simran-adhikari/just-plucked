from django.contrib import admin
from .models import Country, State, District, City, UnitOfMeasure, Bank, BankBranch, Category, FarmingPracticeType, CropType, LivestockType, CertificationBody,Tag

# Inline Model Admins
class StateInline(admin.TabularInline):
    model = State
    extra = 1
    verbose_name = "State"
    verbose_name_plural = "States"


class DistrictInline(admin.TabularInline):
    model = District
    extra = 1
    verbose_name = "District"
    verbose_name_plural = "Districts"


class CityInline(admin.TabularInline):
    model = City
    extra = 1
    verbose_name = "City"
    verbose_name_plural = "Cities"


class BankBranchInline(admin.TabularInline):
    model = BankBranch
    extra = 1
    verbose_name = "Bank Branch"
    verbose_name_plural = "Bank Branches"


 


# Admin for Country Model
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code', 'active', 'created', 'updated')
    list_filter = ('active',)
    search_fields = ('name',)
    inlines = [StateInline]

    class Meta:
        model = Country


# Admin for State Model
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'active', 'created', 'updated')
    list_filter = ('active', 'country')
    search_fields = ('name',)
    inlines = [DistrictInline]

    class Meta:
        model = State


# Admin for District Model
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'active', 'created', 'updated')
    list_filter = ('active', 'state')
    search_fields = ('name',)
    inlines = [CityInline]

    class Meta:
        model = District


# Admin for City Model
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'active', 'created', 'updated')
    list_filter = ('active', 'district')
    search_fields = ('name',)

    class Meta:
        model = City


# Admin for UnitOfMeasure Model
class UnitOfMeasureAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'active', 'created', 'updated')
    list_filter = ('active',)
    search_fields = ('name', 'symbol')

    class Meta:
        model = UnitOfMeasure


# Admin for Bank Model
class BankAdmin(admin.ModelAdmin):
    list_display = ('name', 'swift_code', 'active', 'created', 'updated')
    list_filter = ('active',)
    search_fields = ('name',)

    class Meta:
        model = Bank


# Admin for BankBranch Model
class BankBranchAdmin(admin.ModelAdmin):
    list_display = ('branch_name', 'bank', 'location', 'ifsc_code', 'active', 'created', 'updated')
    list_filter = ('active', 'bank')
    search_fields = ('branch_name', 'ifsc_code')

    class Meta:
        model = BankBranch

 

# Admin for FarmingPracticeType Model
class FarmingPracticeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'created', 'updated')
    list_filter = ('active',)
    search_fields = ('name',)

    class Meta:
        model = FarmingPracticeType


# Admin for CropType Model
class CropTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'created', 'updated')
    list_filter = ('active',)
    search_fields = ('name',)
     

    class Meta:
        model = CropType


# Admin for LivestockType Model
class LivestockTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'created', 'updated')
    list_filter = ('active',)
    search_fields = ('name',)

    class Meta:
        model = LivestockType


# Admin for CertificationBody Model
class CertificationBodyAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'active', 'created', 'updated')
    list_filter = ('active', 'country')
    search_fields = ('name',)

    class Meta:
        model = CertificationBody


# Register Models in Admin Site
admin.site.register(Country, CountryAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(City, CityAdmin)
admin.site.register(UnitOfMeasure, UnitOfMeasureAdmin)
admin.site.register(Bank, BankAdmin)
admin.site.register(BankBranch, BankBranchAdmin)
admin.site.register(FarmingPracticeType, FarmingPracticeTypeAdmin)
admin.site.register(CropType, CropTypeAdmin)
admin.site.register(LivestockType, LivestockTypeAdmin)
admin.site.register(CertificationBody, CertificationBodyAdmin)
