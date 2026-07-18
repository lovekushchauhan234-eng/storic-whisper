from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_articlecontentbackup_articlelink'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='author_name',
            field=models.CharField(
                default='Lovekush Chauhan',
                max_length=100,
                help_text='Byline shown on the article, e.g. "Lovekush Chauhan"',
            ),
        ),
        migrations.AddField(
            model_name='article',
            name='author_bio',
            field=models.CharField(
                default='Founder, Storic Whisper',
                max_length=200,
                blank=True,
                help_text='Short credential line shown under the author name, e.g. "Founder, Storic Whisper"',
            ),
        ),
    ]
    