# Generated by Django 3.0.4 on 2020-03-07 01:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=255)),
                ('step', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('second_name', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('photo', models.FileField(blank=True, default=None, null=True, upload_to='image/profile/')),
                ('sex', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('age', models.IntegerField(blank=True, default=None, null=True)),
                ('something_about_you', models.TextField(blank=True, default=None, null=True)),
                ('chat', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='userprofile.Chat')),
            ],
        ),
        migrations.CreateModel(
            name='UserRestaurant',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserView',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('result', models.BooleanField(default=True)),
                ('user_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='userprofile.UserProfile')),
                ('view_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='userprofile.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userprofile.UserRestaurant'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
