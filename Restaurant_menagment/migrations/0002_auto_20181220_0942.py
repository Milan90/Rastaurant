# Generated by Django 2.1.4 on 2018-12-20 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurant_menagment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='order',
        ),
        migrations.AddField(
            model_name='comments',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Restaurant_menagment.Orders'),
            preserve_default=False,
        ),
    ]
