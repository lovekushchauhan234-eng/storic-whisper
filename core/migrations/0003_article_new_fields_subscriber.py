from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_article_pillar_categories'),
    ]

    operations = [
        # Add thumbnail to Article
        migrations.AddField(
            model_name='article',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbs/'),
        ),
        # Add is_featured to Article
        migrations.AddField(
            model_name='article',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        # Make meta_description optional
        migrations.AlterField(
            model_name='article',
            name='meta_description',
            field=models.CharField(blank=True, max_length=160),
        ),
        # Create Subscriber model
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]