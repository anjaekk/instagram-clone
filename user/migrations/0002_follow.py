# Generated by Django 3.2.4 on 2021-07-02 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='user.user')),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='user.user')),
            ],
            options={
                'db_table': 'follows',
            },
        ),
    ]
