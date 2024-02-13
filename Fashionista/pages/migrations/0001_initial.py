# Generated by Django 5.0.2 on 2024-02-12 15:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pages', to=settings.AUTH_USER_MODEL, verbose_name='page')),
            ],
            options={
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
            },
        ),
        migrations.CreateModel(
            name='Wardrobe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wardrobe', to=settings.AUTH_USER_MODEL, verbose_name='wardrobe')),
            ],
            options={
                'verbose_name': 'wardrobe',
                'verbose_name_plural': 'wardrobes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='name')),
                ('description', models.TextField(blank=True, max_length=100000, verbose_name='description')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='updated at')),
                ('is_available', models.BooleanField(db_index=True, default=False, verbose_name='is available')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing', to=settings.AUTH_USER_MODEL, verbose_name='owner')),
                ('wardrobe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listing', to='pages.wardrobe', verbose_name='project')),
            ],
            options={
                'verbose_name': 'listing',
                'verbose_name_plural': 'listings',
                'ordering': ['is_available', 'created_at'],
            },
        ),
    ]
