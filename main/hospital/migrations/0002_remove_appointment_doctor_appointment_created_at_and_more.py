# Generated by Django 4.2.11 on 2024-04-03 22:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("hospital", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="appointment",
            name="doctor",
        ),
        migrations.AddField(
            model_name="appointment",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="appointment",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="department",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="department",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="doctor",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="doctor",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="doctoravailability",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="doctoravailability",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="medicalhistory",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="medicalhistory",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="patient",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="patient",
            name="doctor",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="hospital.doctor",
            ),
        ),
        migrations.AddField(
            model_name="patient",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="doctoravailability",
            name="day",
            field=models.IntegerField(
                choices=[
                    (1, "MONDAY"),
                    (2, "TUESDAY"),
                    (3, "WEDNESDAY"),
                    (4, "THURSDAY"),
                    (5, "FRIDAY"),
                    (6, "SATURDAY"),
                    (7, "SUNDAY"),
                ]
            ),
        ),
        migrations.AlterField(
            model_name="patient",
            name="gender",
            field=models.CharField(
                choices=[("M", "MALE"), ("F", "FEMALE"), ("O", "OTHER")], max_length=1
            ),
        ),
    ]
