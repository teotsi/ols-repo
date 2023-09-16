# Generated by Django 4.2.5 on 2023-09-16 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_term_id_alter_term_parents_delete_ontology'),
    ]

    operations = [
        migrations.AlterField(
            model_name='synonym',
            name='label',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='id',
            field=models.CharField(default='FAKE_6252961', max_length=32, primary_key=True, serialize=False),
        ),
    ]