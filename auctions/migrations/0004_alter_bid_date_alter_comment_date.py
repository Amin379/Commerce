# Generated by Django 4.1.7 on 2023-03-10 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_bid_date_alter_comment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
