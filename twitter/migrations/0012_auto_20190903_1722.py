# Generated by Django 2.2.5 on 2019-09-03 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0011_auto_20190903_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitter',
            name='term',
            field=models.ForeignKey(blank=True, default='abc', null=True, on_delete=django.db.models.deletion.CASCADE, to='twitter.SearchLog'),
        ),
    ]