# Generated by Django 4.2.16 on 2024-12-02 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_est_valide_colis_is_validated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colis',
            name='status_retour',
            field=models.CharField(choices=[('en_attente', 'En attente de validation'), ('aucun', 'Aucun')], default='aucun', max_length=20),
        ),
    ]
