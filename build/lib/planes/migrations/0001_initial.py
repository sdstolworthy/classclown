# Generated by Django 3.0.7 on 2020-06-28 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Airplane',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.TextField(blank=True, null=True)),
                ('url', models.TextField()),
            ],
        ),
    ]