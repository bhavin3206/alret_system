# Generated by Django 5.0.6 on 2024-07-10 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_subscription_alert_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='lorem_question',
            field=models.CharField(choices=[('>', 'Greater than'), ('<', 'Less than')], default='>', max_length=1, verbose_name='Lorem Question'),
        ),
    ]