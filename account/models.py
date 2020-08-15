from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phone_field import PhoneField
from django_countries.fields import CountryField
from django.conf import settings
# pip install django-phone-field
# pip install django-countries

class category(models.Model):
    category_name=models.CharField(max_length=50)

    def __str__(self):
        return self.category_name

class subcategory(models.Model):
    sub_category_name=models.CharField(max_length=50)
    category=models.ForeignKey(category, on_delete=models.CASCADE)

    def __str__(self):
        return self.sub_category_name

class item_request(models.Model):
    item_name=models.CharField(max_length=50)
    item_category=models.ForeignKey(category, on_delete=models.CASCADE)
    item_subcategory=models.ForeignKey(subcategory, on_delete=models.CASCADE)
    item_description=models.CharField(max_length=200)
    item_reason=models.CharField(max_length=200)
    item_quantity=models.CharField(max_length=100)
    item_image=models.ImageField(upload_to="account/media",default="")
    item_start_date=models.DateField()
    item_end_date=models.DateField()
    item_organization=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_return=models.BooleanField()
    def __str__(self):
        return self.item_name

class item_available(models.Model):
    item_name = models.CharField(max_length=50)
    item_category = models.ForeignKey(category, on_delete=models.CASCADE)
    item_subcategory = models.ForeignKey(subcategory, on_delete=models.CASCADE)
    item_description = models.CharField(max_length=200)
    item_quantity = models.CharField(max_length=100)
    item_image = models.ImageField(upload_to="account/media", default="")
    item_organization = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item_return = models.BooleanField()
    def __str__(self):
        return self.item_name

class MyAccountManager(BaseUserManager):
    def create_user(self, email, organization_name, organization_website, organization_description, admin_name, phone_number, country, postal_code, logo, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            organization_name=organization_name,
            organization_website=organization_website,
            organization_description=organization_description,
            admin_name=admin_name,
            phone_number=phone_number,
            country=country,
            postal_code=postal_code,
            logo = logo
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, organization_name, organization_website, organization_description, admin_name, phone_number, country, postal_code, logo, password):
        user = self.create_user(
            email=self.normalize_email(email),
            organization_name=organization_name,
            organization_website=organization_website,
            organization_description=organization_description,
            admin_name=admin_name,
            phone_number=phone_number,
            country=country,
            postal_code=postal_code,
            password=password,
            logo = logo
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# Create your models here.
class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    organization_name = models.CharField(max_length=60, unique=True)
    organization_website = models.URLField(max_length=1000, unique=True)
    organization_description = models.CharField(max_length=200)
    admin_name = models.CharField(max_length=60)
    phone_number = PhoneField(blank=True)
    country = CountryField(blank_label='(select country')
    postal_code = models.CharField(max_length=60)
    logo = models.ImageField(upload_to="account/media",default="")
    #Not important
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name='last login', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    #Not important

    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['organization_name', 'organization_website', 'organization_description', 'admin_name', 'phone_number', 'country', 'postal_code', 'logo']

    def __str__(self):
        return self.organization_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
