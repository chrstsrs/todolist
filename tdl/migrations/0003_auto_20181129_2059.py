# Generated by Django 2.1.2 on 2018-11-29 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tdl', '0002_auto_20181128_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.CharField(default='abc', max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(max_length=4000),
        ),
    ]
