# Generated by Django 2.2.12 on 2020-06-03 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('address', models.TextField(blank=True, verbose_name='Address')),
                ('tel', models.CharField(blank=True, max_length=40, verbose_name='Telephone')),
                ('url', models.URLField(blank=True, verbose_name='Web site')),
                ('email', models.EmailField(max_length=254, verbose_name='DSI Email')),
                ('contact', models.CharField(blank=True, max_length=100, verbose_name='Contact')),
                ('contact_tel', models.CharField(blank=True, max_length=100, verbose_name="Contact's tel")),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
