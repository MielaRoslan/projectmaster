# Generated by Django 2.2.5 on 2019-09-03 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0003_twitter_screenname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitter',
            name='term',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='twitter.SearchLog'),
        ),
    ]