# Generated by Django 4.2.21 on 2025-07-09 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snippet',
            name='category',
            field=models.CharField(choices=[('html', 'Html'), ('python', 'Python'), ('css', 'CSS'), ('javascript', 'JavaScript'), ('docker', 'Docker'), ('k8s', 'Kubernetes'), ('bash', 'Bash'), ('deploy', 'Deployment'), ('other', 'Other')], default='other', max_length=50),
        ),
    ]
