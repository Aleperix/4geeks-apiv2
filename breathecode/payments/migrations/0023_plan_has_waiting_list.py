# Generated by Django 3.2.16 on 2023-03-08 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0022_auto_20230302_0633'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='has_waiting_list',
            field=models.BooleanField(default=False, help_text='Has waiting list?'),
        ),
    ]
