# Generated by Django 2.2.12 on 2020-05-22 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0003_auto_20200522_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorie',
            name='name_en',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='categorie',
            name='name_fr',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
