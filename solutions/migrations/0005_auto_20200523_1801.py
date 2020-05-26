# Generated by Django 2.2.12 on 2020-05-23 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solutions', '0004_auto_20200522_1027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-created_at'], 'verbose_name': 'Ticket', 'verbose_name_plural': 'Tickets'},
        ),
        migrations.AddField(
            model_name='question',
            name='first_react_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='resolved_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='time_to_react',
            field=models.DurationField(blank=True, null=True, verbose_name='time to react'),
        ),
        migrations.AddField(
            model_name='question',
            name='time_to_resolv',
            field=models.DurationField(blank=True, null=True, verbose_name='time to resolv'),
        ),
        migrations.AddField(
            model_name='question',
            name='time_to_view',
            field=models.DurationField(blank=True, null=True, verbose_name='time to view'),
        ),
        migrations.AddField(
            model_name='question',
            name='viwed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('EA', 'Waiting'), ('RS', 'Resolved'), ('OV', 'Open'), ('FR', 'Closed'), ('RF', 'Refused'), ('AN', 'Canceled'), ('DS', 'Deactiveted')], default='OV', max_length=2),
        ),
    ]