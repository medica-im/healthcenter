# Generated by Django 4.0.4 on 2022-05-16 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_grammatical_gender'),
        ('workforce', '0008_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='gender',
            field=models.ManyToManyField(related_name='labels', to='accounts.grammaticalgender'),
        ),
        migrations.AddField(
            model_name='label',
            name='grammatical_number',
            field=models.CharField(blank=True, choices=[('S', 'Singular'), ('P', 'Plural')], max_length=1),
        ),
    ]