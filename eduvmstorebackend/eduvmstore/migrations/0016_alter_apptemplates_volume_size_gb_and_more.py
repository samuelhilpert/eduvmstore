# Generated by Django 4.2.16 on 2025-04-08 10:06

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('eduvmstore', '0015_apptemplates_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apptemplates',
            name='volume_size_gb',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.CreateModel(
            name='AppTemplateSecurityGroups',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('app_template_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='security_groups', to='eduvmstore.apptemplates')),
            ],
        ),
    ]
