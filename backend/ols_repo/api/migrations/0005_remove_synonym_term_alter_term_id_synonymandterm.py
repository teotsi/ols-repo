# Generated by Django 4.2.5 on 2023-09-14 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_rename_child_term_id_ontology_child_term_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='synonym',
            name='term',
        ),
        migrations.AlterField(
            model_name='term',
            name='id',
            field=models.CharField(default='FAKE_7446606', max_length=12, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='SynonymAndTerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('synonym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.synonym')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.term')),
            ],
        ),
    ]
