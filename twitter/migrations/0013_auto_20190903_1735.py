# Generated by Django 2.2.5 on 2019-09-03 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0012_auto_20190903_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitter',
            name='term',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='twitter.SearchLog'),
        ),
    ]