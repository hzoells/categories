# Generated by Django 3.0.7 on 2020-07-09 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scatter_api', '0003_auto_20200709_1741'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='scatter_api.Question'),
        ),
    ]
