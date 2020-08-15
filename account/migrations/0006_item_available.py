# Generated by Django 3.0.3 on 2020-08-15 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20200815_0328'),
    ]

    operations = [
        migrations.CreateModel(
            name='item_available',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('item_description', models.CharField(max_length=200)),
                ('item_quantity', models.CharField(max_length=100)),
                ('item_image', models.ImageField(default='', upload_to='account/media')),
                ('item_return', models.BooleanField()),
                ('item_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.category')),
                ('item_organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('item_subcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.subcategory')),
            ],
        ),
    ]