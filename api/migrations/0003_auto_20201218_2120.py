# Generated by Django 3.0 on 2020-12-18 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_activity_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='note',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]