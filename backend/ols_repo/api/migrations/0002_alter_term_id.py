# Generated by Django 4.2.5 on 2023-09-13 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='id',
            field=models.CharField(default='FAKE_3406562', max_length=12, primary_key=True, serialize=False),
        ),
    ]
