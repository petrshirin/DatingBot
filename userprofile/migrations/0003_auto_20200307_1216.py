# Generated by Django 3.0.4 on 2020-03-07 04:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_userprofile_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='restaurant',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='userprofile.UserRestaurant'),
        ),
    ]