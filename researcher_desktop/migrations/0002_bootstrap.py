# Generated by Django 3.2.7 on 2021-09-15 07:04

from django.db import migrations

from django.conf import settings

from researcher_desktop.constants import APP_NAME


class Migration(migrations.Migration):

    def addDesktopTypes(apps, schema_editor):
        Feature = apps.get_model('researcher_workspace', 'Feature')
        app_feature = Feature.objects.get(app_name=APP_NAME)
        DesktopType = apps.get_model('researcher_desktop', 'DesktopType')

        # Populate initial desktops from the settings.
        if hasattr(settings, 'DESKTOP_TYPES'):
            field_names = [f.name for f in DesktopType._meta.get_fields()]
            for desktop_type in settings.DESKTOP_TYPES:
                # Make sure we only incorporate fields that have been defined
                # at this point in the migration history.  Other fields may
                # need to be incorporated by later migrations.
                filtered_desktop_type = {
                    key: value for (key, value) in desktop_type.items()
                    if key in field_names}
                DesktopType.objects.create(**filtered_desktop_type,
                                           feature=app_feature)

    def removeDesktopTypes(apps, schema_editor):
        DesktopType = apps.get_model('researcher_desktop', 'DesktopType')
        DesktopType.objects.all().delete()

    dependencies = [
        ('researcher_desktop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(addDesktopTypes, removeDesktopTypes)
    ]
