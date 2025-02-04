# Generated by Django 5.1.5 on 2025-02-04 02:17

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
            name='Pattern',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('difficulty_level', models.IntegerField(choices=[(0, 'Easy'), (1, 'Medium'), (2, 'Hard')])),
                ('craft', models.IntegerField(choices=[(0, 'Crochet'), (1, 'Knitting')])),
                ('yarn_weight', models.IntegerField(choices=[(0, 'Lace/2 ply'), (1, 'Light Fingering/3 ply'), (2, 'Fingering/4 ply (14 wpi)'), (3, 'Sport/5 ply (12 wpi)'), (4, 'DK/8 ply (11 wpi)'), (5, 'Aran/10 ply (8 wpi)'), (6, 'Chunky/12 ply (7 wpi)'), (7, 'Super Chunky/16 ply (5-6 wpi)')])),
                ('size', models.IntegerField(blank=True, choices=[(0, 'One Size'), (1, 'XS'), (2, 'S'), (3, 'M'), (4, 'L'), (5, 'XL')], null=True)),
                ('category', models.IntegerField(blank=True, choices=[(0, 'Clothing'), (1, 'Accessories'), (2, 'Toys and Hobbies'), (3, 'Pet'), (4, 'Home')], null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patterns', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Library',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='libraries', to=settings.AUTH_USER_MODEL)),
                ('pattern', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patterns.pattern')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('pattern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patterns.pattern')),
            ],
        ),
        migrations.CreateModel(
            name='PatternHooksNeedle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(0, 'Hook'), (1, 'Needle')])),
                ('hook_size', models.IntegerField(blank=True, choices=[(0, '2.0 mm'), (1, '2.25 mm'), (2, '2.5 mm'), (3, '2.75 mm'), (4, '3.0 mm'), (5, '3.25 mm'), (6, '3.5 mm'), (7, '3.75 mm'), (8, '4.0 mm'), (9, '4.5 mm'), (10, '5.0 mm'), (11, '5.5 mm'), (12, '6.0 mm'), (13, '6.5 mm'), (14, '7.0 mm'), (15, '8.0 mm'), (16, '9.0 mm'), (17, '10.0 mm'), (18, '12.0 mm'), (19, '15.0 mm'), (20, '20.0 mm')], null=True)),
                ('needle_size', models.IntegerField(blank=True, choices=[(0, '2.0 mm / US 0'), (1, '2.25 mm / US 1'), (2, '2.5 mm / US 1.5'), (3, '2.75 mm / US 2'), (4, '3.0 mm / US 2.5'), (5, '3.25 mm / US 3'), (6, '3.5 mm / US 4'), (7, '3.75 mm / US 5'), (8, '4.0 mm / US 6'), (9, '4.5 mm / US 7'), (10, '5.0 mm / US 8'), (11, '5.5 mm / US 9'), (12, '6.0 mm / US 10'), (13, '6.5 mm / US 10.5'), (14, '7.0 mm / US 10.75'), (15, '8.0 mm / US 11'), (16, '9.0 mm / US 13'), (17, '10.0 mm / US 15'), (18, '12.0 mm / US 17'), (19, '15.0 mm / US 19'), (20, '20.0 mm / US 36')], null=True)),
                ('pattern', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pattern_hooks_needles', to='patterns.pattern')),
            ],
        ),
    ]
