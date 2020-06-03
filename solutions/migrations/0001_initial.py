# Generated by Django 2.2.12 on 2020-06-03 13:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import solutions.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('name_en', models.CharField(blank=True, max_length=100, null=True)),
                ('name_fr', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Categorie',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('titre', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to=solutions.models.Question.content_file_name)),
                ('priorite', models.CharField(choices=[('F', 'Low'), ('M', 'Medium'), ('H', 'Height'), ('U', 'Urgent')], default='F', max_length=1)),
                ('status', models.CharField(choices=[('EA', 'Waiting'), ('RS', 'Resolved'), ('OV', 'Open'), ('FR', 'Closed'), ('RF', 'Refused'), ('AN', 'Canceled'), ('DS', 'Deactiveted')], default='OV', max_length=2)),
                ('description', models.TextField(blank=True, verbose_name='comment')),
                ('viwed_at', models.DateTimeField(blank=True, null=True)),
                ('time_to_view', models.DurationField(blank=True, null=True, verbose_name='time to view')),
                ('first_react_at', models.DateTimeField(blank=True, null=True)),
                ('time_to_react', models.DurationField(blank=True, null=True, verbose_name='time to react')),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('time_to_resolv', models.DurationField(blank=True, null=True, verbose_name='time to resolv')),
                ('last_action', models.DateTimeField(auto_now=True)),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quesions', to='solutions.Categorie')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SousCategorie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('name_en', models.CharField(blank=True, max_length=100, null=True)),
                ('name_fr', models.CharField(blank=True, max_length=100, null=True)),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SousCategories', to='solutions.Categorie')),
            ],
            options={
                'verbose_name': 'SousCategorie',
                'verbose_name_plural': 'SousCategories',
            },
        ),
        migrations.CreateModel(
            name='Reponce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('status', models.CharField(choices=[('EA', 'Waiting'), ('RS', 'Resolved'), ('FR', 'Closed'), ('RF', 'Refused'), ('AN', 'Canceled')], default='EA', max_length=2)),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reponces', to='solutions.Question')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reponces', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='souscategorie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quesions', to='solutions.SousCategorie'),
        ),
        migrations.AddField(
            model_name='question',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tickets', to=settings.AUTH_USER_MODEL),
        ),
    ]
