# Generated by Django 4.2.16 on 2024-12-02 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_colis_is_validated'),
    ]

    operations = [
        migrations.RenameField(
            model_name='colis',
            old_name='is_validated',
            new_name='est_valide',
        ),
    ]
