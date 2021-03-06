# Generated by Django 3.2.6 on 2021-08-25 13:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.TextField()),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=150)),
                ('answer_type', models.CharField(choices=[('TEXT', 'ответ текстом'), ('SINGLE', 'ответ с выбором одного варианта'), ('MULTIPLE', 'ответ с выбором нескольких вариантов')], default='TEXT', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('start_data', models.DateField(default=datetime.date.today, editable=False)),
                ('end_data', models.DateField(default=datetime.date.today)),
                ('description', models.TextField()),
            ],
            options={
                'ordering': ['-start_data'],
            },
        ),
        migrations.AlterModelOptions(
            name='survey',
            options={'ordering': ['-schema']},
        ),
        migrations.RemoveField(
            model_name='survey',
            name='description',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='end_data',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='name',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='start_data',
        ),
        migrations.AddField(
            model_name='survey',
            name='participant',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='survey.participant'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='schema',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='survey.schema'),
            preserve_default=False,
        ),
    ]
