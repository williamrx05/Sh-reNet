from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model
)
from account.models import item_request, subcategory, category, item_available
from phone_field import PhoneField
import pgeocode
import math
User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('User does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    organization_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    organization_website = forms.URLField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    organization_description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    admin_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = [
            'email', 'password', 'organization_name', 'organization_website', 'organization_description', 'admin_name', 'phone_number', 'country', 'postal_code', 'logo'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(
                "This email is already being used"
            )
        return email

    def clean_organization_website(self):
        organization_website = self.cleaned_data.get('organization_website')
        website_qs = User.objects.filter(organization_website=organization_website)
        if website_qs.exists():
            raise forms.ValidationError(
                "This website URL is already being used"
            )
        return organization_website

    def clean_organization(self):
        cd = self.cleaned_data
        organization_name = cd.get('organization_name')
        organization_name_qs = User.objects.filter(organization_name=organization_name)
        if organization_name_qs.exists():
            raise forms.ValidationError(
                "This organization name is already being used"
            )
        return cd.get('organization')

    def clean_country(self):
        cd = self.cleaned_data
        try:
            nomi = pgeocode.Nominatim(cd.get('country'))
        except:
            raise forms.ValidationError("Your country is not supported currently")
        return cd.get('country')

    def clean_postal_code(self):
        cd = self.cleaned_data
        try:
            nomi = pgeocode.Nominatim(cd.get('country'))
            if (str(nomi.query_postal_code(cd.get('postal_code')).loc["country code"]) != str (cd.get('country'))):
                raise forms.ValidationError("Your postal code is invalid")
        except:
            raise forms.ValidationError("Your postal code is invalid")
        return cd.get('postal_code')

class ItemForm(forms.ModelForm):
    item_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    item_description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    item_quantity = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = item_available
        exclude = ('item_organization',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_subcategory'].queryset = subcategory.objects.none()

        if 'item_category' in self.data:
            try:
                category_id = int(self.data.get('item_category'))
                self.fields['item_subcategory'].queryset = subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['item_subcategory'].queryset = self.instance.item_category.item_subcategory_set

class ItemRequestForm(forms.ModelForm):
    item_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    item_description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    item_reason = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    item_quantity = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    item_start_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    item_end_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = item_request
        exclude = ('item_organization',)

    def clean(self):
        cd = self.cleaned_data
        start = cd.get("item_start_date")
        end = cd.get("item_end_date")
        if end < start:
            raise forms.ValidationError("End date should be greater than or equal to start date")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_subcategory'].queryset = subcategory.objects.none()

        if 'item_category' in self.data:
            try:
                category_id = int(self.data.get('item_category'))
                self.fields['item_subcategory'].queryset = subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['item_subcategory'].queryset = self.instance.item_category.item_subcategory_set

class organizationSearchForm(forms.Form):
    DISTANCE_CHOICES = [
        ('anywhere', 'Anywhere'),
        ('country', 'Within My Country'),
        ('100', "Within 100 km"),
        ('50', "Within 50 km"),
        ('25', "Within 25 km"),
        ('10', "Within 10km"),
        ('postalcode', "Within my postal code")
    ]
    organization_name = forms.CharField(label="Organization Name", max_length=100, required=False)
    organization_distance = forms.CharField(widget=forms.Select(choices=DISTANCE_CHOICES))

class searchForm2(forms.Form):
    DISTANCE_CHOICES = [
        ('anywhere', 'Anywhere'),
        ('country', 'Within My Country'),
        ('100', "Within 100 km"),
        ('50', "Within 50 km"),
        ('25', "Within 25 km"),
        ('10', "Within 10km"),
        ('postalcode', "Within my postal code")
    ]
    item_request_name = forms.CharField(label="Item Name", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    item_organization_name = forms.CharField(label="Organization Name", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    item_distance = forms.CharField(widget=forms.Select(choices=DISTANCE_CHOICES))
    item_category = forms.ModelChoiceField(queryset=category.objects.all(), required=False)
    item_subcategory = forms.ModelChoiceField(queryset=subcategory.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_subcategory'].queryset = subcategory.objects.none()

        if 'item_category' in self.data:
            try:
                category_id = int(self.data.get('item_category'))
                self.fields['item_subcategory'].queryset = subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass

class searchForm(forms.Form):
    DISTANCE_CHOICES = [
        ('anywhere', 'Anywhere'),
        ('country', 'Within My Country'),
        ('100', "Within 100 km"),
        ('50', "Within 50 km"),
        ('25', "Within 25 km"),
        ('10', "Within 10km"),
        ('postalcode', "Within my postal code")
    ]
    item_request_name = forms.CharField(label="Item Name", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    item_organization_name = forms.CharField(label="Organization Name", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    item_start_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    item_end_date = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    item_distance = forms.CharField(widget=forms.Select(choices=DISTANCE_CHOICES))
    item_category = forms.ModelChoiceField(queryset=category.objects.all(), required=False)
    item_subcategory = forms.ModelChoiceField(queryset=subcategory.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_subcategory'].queryset = subcategory.objects.none()

        if 'item_category' in self.data:
            try:
                category_id = int(self.data.get('item_category'))
                self.fields['item_subcategory'].queryset = subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass

class emailForm(forms.Form):
    message_name = forms.CharField(widget=forms.Textarea(attrs={'readonly':'readonly', 'rows': 1, 'columns': 20, 'class': 'form-control'}))
    message_email_to = forms.EmailField(widget=forms.TextInput(attrs={'readonly':'readonly', 'class': 'form-control'}))
    message = forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'rows': 5, 'columns': 10, 'class': 'form-control'}))