from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_article_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='language',
            field=models.CharField(
                choices=[('HI', 'Hindi'), ('EN', 'English')],
                default='HI',
                max_length=2,
            ),
        ),
        migrations.AddField(
            model_name='article',
            name='topic_section',
            field=models.CharField(
                blank=True,
                choices=[
                    ('attachment', 'Attachment Theory'),
                    ('validation', 'Validation Psychology'),
                    ('dependency', 'Emotional Dependency'),
                    ('relationship', 'Relationship Psychology'),
                    ('behavior', 'Human Behavior'),
                    ('dark', 'Dark Psychology'),
                    ('stoicism', 'Stoicism'),
                    ('dopamine', 'Dopamine & Modern Mind'),
                    ('transformation', 'Self Transformation'),
                    ('ai_mind', 'AI & Human Mind'),
                ],
                max_length=50,
                null=True,
            ),
        ),
    ]
