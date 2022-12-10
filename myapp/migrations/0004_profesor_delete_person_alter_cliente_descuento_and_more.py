# Generated by Django 4.1.3 on 2022-11-30 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_cliente_vendedor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('idSalon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.salon')),
            ],
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='descuento',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='vendedor',
            name='sueldo',
            field=models.FloatField(),
        ),
        migrations.AddConstraint(
            model_name='profesor',
            constraint=models.UniqueConstraint(fields=('id', 'first_name', 'last_name'), name='primary_key_profesor'),
        ),
    ]