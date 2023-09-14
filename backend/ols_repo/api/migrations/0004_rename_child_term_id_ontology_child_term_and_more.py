# Generated by Django 4.2.5 on 2023-09-14 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_term_id_synonym_ontology'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ontology',
            old_name='child_term_id',
            new_name='child_term',
        ),
        migrations.RenameField(
            model_name='ontology',
            old_name='parent_term_id',
            new_name='parent_term',
        ),
        migrations.RenameField(
            model_name='synonym',
            old_name='term_id',
            new_name='term',
        ),
        migrations.AlterField(
            model_name='term',
            name='id',
            field=models.CharField(default='FAKE_8274901', max_length=12, primary_key=True, serialize=False),
        ),
    ]
