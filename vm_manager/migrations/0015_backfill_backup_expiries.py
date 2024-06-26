# Generated by Django 3.2.12 on 2022-08-25 06:15

from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.db import migrations

from vm_manager.models import EXP_INITIAL


class Migration(migrations.Migration):

    dependencies = [
        ('vm_manager', '0014_add_backup_expiration'),
    ]

    def add_backup_expirations(apps, schema_editor):
        Volume = apps.get_model("vm_manager", "Volume")
        BackupExpiration = apps.get_model("vm_manager", "BackupExpiration")

        # If a positive backup lifetime is configured, create a backup
        # expiration for each existing backup, base on when they were created.
        # We don't know if the backup has been deleted already, but the next
        # run of the expirer will check that, and quietly complete any
        # unnecessary expirations
        backup_lifetime = settings.BACKUP_LIFETIME
        if backup_lifetime and backup_lifetime > 0:
            for v in Volume.objects.exclude(backup_id=None) \
                                   .exclude(archived_at=None):
                expiration = BackupExpiration(
                    stage=EXP_INITIAL, stage_date=datetime.now(timezone.utc),
                    expires=(v.archived_at + timedelta(days=backup_lifetime)))
                expiration.save()
                v.backup_expiration = expiration
                v.save()

    def remove_backup_expirations(apps, schema_editor):
        Volume = apps.get_model("vm_manager", "Volume")
        for v in Volume.objects.exclude(backup_expiration=None):
            # Just clear it.
            v.backup_expiration = None
            v.save()

    operations = [
        migrations.RunPython(add_backup_expirations,
                             remove_backup_expirations)
    ]
