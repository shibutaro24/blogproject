# Generated by Django 3.1.3 on 2023-01-26 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('PUBLIC', '公開'), ('PRIVATE', '非公開')], default='PUBLIC', max_length=10),
        ),
    ]