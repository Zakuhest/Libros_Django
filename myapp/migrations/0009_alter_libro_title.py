# Generated by Django 4.1.3 on 2022-12-02 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_libro_authors_alter_libro_publisher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]