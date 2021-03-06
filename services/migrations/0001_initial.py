# Generated by Django 2.1.7 on 2019-09-20 13:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(blank=True, max_length=200, unique=True)),
                ('url', models.URLField()),
                ('category', models.CharField(blank=True, choices=[('js', 'js'), ('css', 'css'), ('html', 'html'), ('static', 'static')], default='html', max_length=10)),
                ('root', models.BooleanField(default=False)),
                ('content', models.TextField(blank=True)),
                ('crawled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('url', models.URLField()),
                ('email', models.EmailField(max_length=254)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('G', '✓ good'), ('E', '× error'), ('C', '~ running')], default='G', max_length=1)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='file',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='services.Item'),
        ),
    ]
