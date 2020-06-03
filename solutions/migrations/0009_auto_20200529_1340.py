# Generated by Django 2.2.12 on 2020-05-29 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0008_auto_20200528_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.TextField(blank=True, verbose_name='comment'),
        ),
        migrations.AlterField(
            model_name='reponce',
            name='status',
            field=models.CharField(choices=[('EA', 'Waiting'), ('RS', 'Resolved'), ('FR', 'Closed'), ('RF', 'Refused'), ('AN', 'Canceled')], default='EA', max_length=2),
        ),
    ]