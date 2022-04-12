# Generated by Django 4.0.3 on 2022-04-03 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mesh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=10, unique=True)),
                ('fr', models.CharField(max_length=255)),
                ('en', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddIndex(
            model_name='mesh',
            index=models.Index(fields=['uid'], name='mesh_mesh_uid_f7a30f_idx'),
        ),
    ]