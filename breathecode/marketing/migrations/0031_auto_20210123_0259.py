# Generated by Django 3.1.4 on 2021-01-23 02:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketing', '0030_activecampaignacademy_event_attendancy_automation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activecampaignacademy',
            name='event_attendancy_automation',
            field=models.ForeignKey(blank=True,
                                    default=None,
                                    null=True,
                                    on_delete=django.db.models.deletion.CASCADE,
                                    to='marketing.automation'),
        ),
    ]
