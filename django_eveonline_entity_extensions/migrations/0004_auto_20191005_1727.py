# Generated by Django 2.2.4 on 2019-10-05 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_eveonline_entity_extensions', '0003_eveskill_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='evejournalentry',
            name='first_party_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evejournalentry',
            name='second_party_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
