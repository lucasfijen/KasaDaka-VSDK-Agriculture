# Generated by Django 2.0.4 on 2019-05-20 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('service_development', '0009_auto_20190513_1444'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vse_Own_Added',
            fields=[
                ('voiceserviceelement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='service_development.VoiceServiceElement')),
                ('final_element', models.BooleanField(default=False, verbose_name='This element will terminate the call')),
                ('_redirect', models.ForeignKey(blank=True, help_text='The element to redirect to after the message has been played.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_development_vse_own_added_related', to='service_development.VoiceServiceElement', verbose_name='Redirect element')),
            ],
            options={
                'verbose_name': 'Own Added Elements',
            },
            bases=('service_development.voiceserviceelement',),
        ),
        migrations.AddField(
            model_name='callsession',
            name='_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service_development.Product'),
        ),
        migrations.AddField(
            model_name='callsession',
            name='_region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='service_development.Region'),
        ),
    ]
