# Generated by Django 2.1.7 on 2019-05-08 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service_development', '0003_product_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='voice_label',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service_development.VoiceLabel', verbose_name='Voice label'),
        ),
        migrations.AddField(
            model_name='region',
            name='voice_label',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service_development.VoiceLabel', verbose_name='Voice label'),
        ),
    ]
