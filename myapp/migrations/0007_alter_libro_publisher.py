# Generated by Django 4.1.3 on 2022-12-02 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_libro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='publisher',
            field=models.CharField(max_length=100),
        ),
    ]