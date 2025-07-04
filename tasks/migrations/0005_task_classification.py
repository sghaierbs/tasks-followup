# Generated by Django 4.2.21 on 2025-05-28 21:26

from django.db import migrations, models
import django.db.models.deletion
import tasks.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_trackableclassification'),
        ('tasks', '0004_task_urgency'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='classification',
            field=models.ForeignKey(default=tasks.models.get_default_classification, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.trackableclassification'),
        ),
    ]
