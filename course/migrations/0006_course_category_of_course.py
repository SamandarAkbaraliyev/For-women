# Generated by Django 4.2.7 on 2024-02-01 09:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
        ("course", "0005_course_buy_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="category_of_course",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to="main.category"),
        ),
    ]