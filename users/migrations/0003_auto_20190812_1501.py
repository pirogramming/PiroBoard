# Generated by Django 2.2.4 on 2019-08-12 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190812_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='master_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slave_group', to='users.Profile'),
        ),
    ]
