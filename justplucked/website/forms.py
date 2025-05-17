from django import forms
from farmer.models import Farmer
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit

class FarmerRegistrationForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['full_name', 'gender', 'date_of_birth', 'marital_status', 
                  'phone', 'alternate_phone', 'email', 'country', 'state', 
                  'district', 'municipality', 'ward_no', 'street_address', 
                  'nid_number', 'nid_document', 'bank_name', 'bank_account_number',
                  'bank_branch', 'profile_picture', 'land_area_in_acres', 
                  'primary_crop', 'farming_experience_years']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'profile_picture': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set placeholders for each field
        placeholders = {
            'full_name': 'Enter your full name',
            'gender': 'Select gender',
            'date_of_birth': 'Select your birth date',
            'marital_status': 'Select marital status',
            'phone': 'Enter primary phone number',
            'alternate_phone': 'Enter alternate phone number',
            'email': 'Enter email address',
            'country': 'Enter country',
            'state': 'Enter state',
            'district': 'Enter district',
            'municipality': 'Enter municipality',
            'ward_no': 'Enter ward number',
            'street_address': 'Enter full street address',
            'nid_number': 'Enter National ID number',
            'bank_name': 'Enter bank name',
            'bank_account_number': 'Enter bank account number',
            'bank_branch': 'Enter bank branch',
            'land_area_in_acres': 'e.g. 3.5',
            'primary_crop': 'e.g. Rice, Wheat',
            'farming_experience_years': 'e.g. 5',
        }

        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

        # Initialize crispy form layout
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(Column('full_name', css_class='col-md-6'), Column('gender', css_class='col-md-6')),
            Row(Column('date_of_birth', css_class='col-md-6'), Column('marital_status', css_class='col-md-6')),
            Row(Column('phone', css_class='col-md-6'), Column('alternate_phone', css_class='col-md-6')),
            Row(Column('email', css_class='col-md-6'), Column('country', css_class='col-md-6')),
            Row(Column('state', css_class='col-md-6'), Column('district', css_class='col-md-6')),
            Row(Column('municipality', css_class='col-md-6'), Column('ward_no', css_class='col-md-6')),
            Row(Column('street_address', css_class='col-md-12')),
            Row(Column('nid_number', css_class='col-md-6'), Column('nid_document', css_class='col-md-6')),
            Row(Column('bank_name', css_class='col-md-4'), Column('bank_account_number', css_class='col-md-4'), Column('bank_branch', css_class='col-md-4')),
            Row(Column('profile_picture', css_class='col-md-6'), Column('land_area_in_acres', css_class='col-md-6')),
            Row(Column('primary_crop', css_class='col-md-6'), Column('farming_experience_years', css_class='col-md-6')),
            Submit('submit', 'Register')
        )

    def save(self, commit=True):
        farmer = super().save(commit=False)
        farmer.is_active = False
        if commit:
            farmer.save()
        return farmer
