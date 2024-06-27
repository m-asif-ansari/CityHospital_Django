# Generated by Django 5.0.6 on 2024-06-26 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0012_alter_appointment_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.CharField(choices=[('09:00', '09:00'), ('09:30', '09:30'), ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'), ('12:00', '12:00'), ('12:30', '12:30'), ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'), ('16:00', '16:00'), ('16:30', '16:30'), ('17:00', '17:00'), ('17:30', '17:30')], max_length=10),
        ),
    ]