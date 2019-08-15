# Generated by Django 2.2.4 on 2019-08-14 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='interest',
            field=models.CharField(blank=True, choices=[('음식', '음식'), ('스포츠', '스포츠'), ('코딩', '코딩'), ('여행', '여행'), ('컴퓨터', '컴퓨터'), ('게임', '게임'), ('영화', '영화'), ('언어', '언어'), ('예술', '예술'), ('음악', '음악'), ('경훈', '경훈')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='region',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]