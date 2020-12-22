# Generated by Django 3.1.4 on 2020-12-22 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bigdata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grocery',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('all_grocery_id', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('reg_date', models.DateTimeField(blank=True, null=True)),
                ('gubun', models.IntegerField(blank=True, null=True)),
                ('coordinate', models.JSONField(blank=True, null=True)),
                ('expiration_date', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'GROCERY',
            },
        ),
    ]
