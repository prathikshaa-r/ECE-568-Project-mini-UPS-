# Generated by Django 2.2 on 2019-04-23 01:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UPS', '0003_incomingsequa_incomingseqworld_outgoingsequa_outgoingseqworld'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('w_id', models.IntegerField(primary_key=True, serialize=False)),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='package',
            name='truck',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='package_set', to='UPS.Truck'),
        ),
    ]