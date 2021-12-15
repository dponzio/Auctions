# Generated by Django 3.2.4 on 2021-07-29 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_bid_bidder'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_won', to=settings.AUTH_USER_MODEL),
        ),
    ]