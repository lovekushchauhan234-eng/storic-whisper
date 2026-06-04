from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.CharField(
                max_length=20,
                choices=[
                    ('women', 'Women Psychology'),
                    ('dark', 'Dark Psychology'),
                    ('breakup', 'Breakup Recovery'),
                    ('stoic', 'Stoicism'),
                    ('dopamine', 'Dopamine & Modern Mind'),
                    ('human', 'Human Behavior'),
                    ('transform', 'Self-Transformation'),
                    ('aimind', 'AI + Human Mind'),
                ],
            ),
        ),
    ]
