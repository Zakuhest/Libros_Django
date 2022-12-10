# Generated by Django 4.1.3 on 2022-11-30 00:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aula', models.CharField(max_length=2)),
                ('hora_entrada', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Alumno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('idSalon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.salon')),
            ],
        ),
        migrations.AddConstraint(
            model_name='alumno',
            constraint=models.UniqueConstraint(fields=('id', 'first_name', 'last_name'), name='primary_key_alumno'),
        ),
    ]