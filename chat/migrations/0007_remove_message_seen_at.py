# Generated by Django 5.1.5 on 2025-01-27 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_alter_message_seen_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='seen_at',
        ),
    ]
