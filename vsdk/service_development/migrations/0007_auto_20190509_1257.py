# Generated by Django 2.1.7 on 2019-05-09 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service_development', '0006_auto_20190509_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='description',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service_development.VoiceLabel', verbose_name='Voice label'),
        ),
    ]