from django.core.management.base import BaseCommand
from core.models import Article
from django.utils import timezone
from datetime import datetime


class Command(BaseCommand):
    help = 'Add legacy internal links to older articles pointing to newer relevant articles'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Legacy Internal Linking...'))
        
        # Define link updates for each article
        link_updates = [
            # Hindi Articles - Oldest First
            {
                'slug': 'dark-psychology',
                'updates': [
                    {
                        'old_text': 'Silence का मतलब हमेशा गुस्सा नहीं होता। कई बार यह emotional control होता है।',
                        'new_text': 'Silence का मतलब हमेशा गुस्सा नहीं होता। कई बार यह <a href="https://storicwhisper.com/articles/stoicism/">emotional control</a> होता है।',
                        'anchor': 'emotional control',
                        'destination': 'stoicism'
                    },
                    {
                        'old_text': '- Emotions को control करना जानता है',
                        'new_text': '- <a href="https://storicwhisper.com/articles/stoicism/">Emotions को control करना जानता है</a>',
                        'anchor': 'Emotions को control करना जानता है',
                        'destination': 'stoicism'
                    }
                ]
            },
            {
                'slug': 'the-dopamine-trap',
                'updates': [
                    {
                        'old_text': 'डोपामिन का खेल और \'Love Addiction\' का केमिकल आर्किटेक्चर',
                        'new_text': 'डोपामिन का खेल और <a href="https://storicwhisper.com/articles/the-male-validation-trap-validation/">\'Love Addiction\' का केमिकल आर्किटेक्चर</a>',
                        'anchor': '\'Love Addiction\' का केमिकल आर्किटेक्चर',
                        'destination': 'the-male-validation-trap-validation'
                    },
                    {
                        'old_text': 'Dark Psychology: चुप्पी कैसे लोगों को कंट्रोल करती है',
                        'new_text': '<a href="https://storicwhisper.com/articles/dark-psychology/">Dark Psychology: चुप्पी कैसे लोगों को कंट्रोल करती है</a>',
                        'anchor': 'Dark Psychology: चुप्पी कैसे लोगों को कंट्रोल करती है',
                        'destination': 'dark-psychology'
                    }
                ]
            },
            {
                'slug': 'the-male-validation-trap-validation',
                'updates': [
                    {
                        'old_text': 'इंसानी व्यवहार और निर्णय लेने की इस जटिल प्रक्रिया का पूरा वैज्ञानिक विश्लेषण आप हमारे Human Behavior सेक्शन में देख सकते हैं।',
                        'new_text': 'इंसानी व्यवहार और निर्णय लेने की इस जटिल प्रक्रिया का पूरा वैज्ञानिक विश्लेषण आप हमारे <a href="https://storicwhisper.com/articles/the-architecture-of-control-decoding-the-hidden-fo/">Human Behavior</a> सेक्शन में देख सकते हैं।',
                        'anchor': 'Human Behavior',
                        'destination': 'the-architecture-of-control-decoding-the-hidden-fo'
                    },
                    {
                        'old_text': 'attention और validation—के प्रति जन्मजात रूप से (neurobiologically) कहीं ज्यादा sensitive होता है।',
                        'new_text': 'attention और <a href="https://storicwhisper.com/articles/why-you-cant-move-on-after-a-breakup-the-truth-mig/">validation</a>—के प्रति जन्मजात रूप से (neurobiologically) कहीं ज्यादा sensitive होता है।',
                        'anchor': 'validation',
                        'destination': 'why-you-cant-move-on-after-a-breakup-the-truth-mig'
                    }
                ]
            },
            {
                'slug': 'why-you-cant-move-on-after-a-breakup-the-truth-mig',
                'updates': [
                    {
                        'old_text': 'हम किसी रिश्ते में कैसे व्यवहार करते हैं, ब्रेकअप के दर्द को कैसे संभालते हैं, और किसी के जाने के बाद हमारी प्रतिक्रिया क्या होती है—यह सब कुछ हमारी Attachment Theory से तय होता है।',
                        'new_text': 'हम किसी रिश्ते में कैसे व्यवहार करते हैं, ब्रेकअप के दर्द को कैसे संभालते हैं, और किसी के जाने के बाद हमारी प्रतिक्रिया क्या होती है—यह सब कुछ हमारी <a href="https://storicwhisper.com/articles/what-is-attachment-theory/">Attachment Theory</a> से तय होता है।',
                        'anchor': 'Attachment Theory',
                        'destination': 'what-is-attachment-theory'
                    },
                    {
                        'old_text': 'महिलाओं और पुरुषों में इसके थोड़े अलग रूप देखने को मिलते हैं, जिसे women psychology के संदर्भ में भी गहराई से समझा जा सकता है।',
                        'new_text': 'महिलाओं और पुरुषों में इसके थोड़े अलग रूप देखने को मिलते हैं, जिसे <a href="https://storicwhisper.com/articles/the-male-validation-trap-validation/">women psychology</a> के संदर्भ में भी गहराई से समझा जा सकता है।',
                        'anchor': 'women psychology',
                        'destination': 'the-male-validation-trap-validation'
                    }
                ]
            },
            {
                'slug': 'stoicism',
                'updates': [
                    {
                        'old_text': 'The Birkbeck Study: Quantifying the Power of Stoic Training',
                        'new_text': 'The Birkbeck Study: Quantifying the Power of <a href="https://storicwhisper.com/articles/self-transformation/">Stoic Training</a>',
                        'anchor': 'Stoic Training',
                        'destination': 'self-transformation'
                    },
                    {
                        'old_text': 'Domestication of Emotions vs. Suppression',
                        'new_text': '<a href="https://storicwhisper.com/articles/the-dopamine-trap/">Domestication of Emotions</a> vs. Suppression',
                        'anchor': 'Domestication of Emotions',
                        'destination': 'the-dopamine-trap'
                    }
                ]
            },
            # English Articles - Oldest First
            {
                'slug': 'why-is-stoicism-becoming-so-popular-in-the-modern',
                'updates': [
                    {
                        'old_text': 'The Hidden Blueprint of Cognitive Behavioral Therapy (CBT)',
                        'new_text': 'The Hidden Blueprint of <a href="https://storicwhisper.com/articles/the-architecture-of-control-decoding-the-hidden-fo/">Cognitive Behavioral Therapy (CBT)</a>',
                        'anchor': 'Cognitive Behavioral Therapy (CBT)',
                        'destination': 'the-architecture-of-control-decoding-the-hidden-fo'
                    },
                    {
                        'old_text': 'The Birkbeck Study: Quantifying the Power of Stoic Training',
                        'new_text': 'The Birkbeck Study: Quantifying the Power of <a href="https://storicwhisper.com/articles/what-is-self-transformation-the-science-of-persona/">Stoic Training</a>',
                        'anchor': 'Stoic Training',
                        'destination': 'what-is-self-transformation-the-science-of-persona'
                    }
                ]
            },
            {
                'slug': 'the-architecture-of-control-decoding-the-hidden-fo',
                'updates': [
                    {
                        'old_text': 'The Cult of the Crowd: When Majority Rewrites Reality',
                        'new_text': 'The Cult of the Crowd: When Majority <a href="https://storicwhisper.com/articles/why-is-stoicism-becoming-so-popular-in-the-modern/">Rewrites Reality</a>',
                        'anchor': 'Rewrites Reality',
                        'destination': 'why-is-stoicism-becoming-so-popular-in-the-modern'
                    },
                    {
                        'old_text': 'The Neurobiology of Exclusion: Why Being Left Out Feels Like Physical Violence',
                        'new_text': 'The Neurobiology of Exclusion: Why Being Left Out Feels Like <a href="https://storicwhisper.com/articles/what-is-attachment-theory/">Physical Violence</a>',
                        'anchor': 'Physical Violence',
                        'destination': 'what-is-attachment-theory'
                    }
                ]
            },
            {
                'slug': 'the-dopamine-trap-what-is-dopamine',
                'updates': [
                    {
                        'old_text': 'The Dopamine Myth',
                        'new_text': 'The <a href="https://storicwhisper.com/articles/why-is-stoicism-becoming-so-popular-in-the-modern/">Dopamine Myth</a>',
                        'anchor': 'Dopamine Myth',
                        'destination': 'why-is-stoicism-becoming-so-popular-in-the-modern'
                    },
                    {
                        'old_text': 'What Dopamine Really Does',
                        'new_text': 'What <a href="https://storicwhisper.com/articles/human-mind-Ai/">Dopamine Really Does</a>',
                        'anchor': 'Dopamine Really Does',
                        'destination': 'human-mind-Ai'
                    }
                ]
            },
            {
                'slug': 'what-is-self-transformation-the-science-of-persona',
                'updates': [
                    {
                        'old_text': 'The Critical Importance of Self Transformation',
                        'new_text': 'The Critical Importance of <a href="https://storicwhisper.com/articles/why-is-stoicism-becoming-so-popular-in-the-modern/">Self Transformation</a>',
                        'anchor': 'Self Transformation',
                        'destination': 'why-is-stoicism-becoming-so-popular-in-the-modern'
                    },
                    {
                        'old_text': 'What Does Science Say? (The Neurological Reality)',
                        'new_text': 'What Does Science Say? (The <a href="https://storicwhisper.com/articles/the-dopamine-trap-what-is-dopamine/">Neurological Reality</a>)',
                        'anchor': 'Neurological Reality',
                        'destination': 'the-dopamine-trap-what-is-dopamine'
                    }
                ]
            }
        ]
        
        total_links_added = 0
        articles_updated = []
        
        for update in link_updates:
            try:
                article = Article.objects.get(slug=update['slug'])
                original_content = article.content
                modified_content = original_content
                
                for link_update in update['updates']:
                    if link_update['old_text'] in modified_content:
                        modified_content = modified_content.replace(
                            link_update['old_text'],
                            link_update['new_text']
                        )
                        total_links_added += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"✓ Added link in '{article.title}': "
                                f"'{link_update['anchor']}' → '{link_update['destination']}'"
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"⚠ Text not found in '{article.title}': "
                                f"'{link_update['old_text'][:50]}...'"
                            )
                        )
                
                if modified_content != original_content:
                    article.content = modified_content
                    article.save()
                    articles_updated.append(article.title)
                    self.stdout.write(
                        self.style.SUCCESS(f"✓ Updated article: {article.title}")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"⚠ No changes needed for: {article.title}")
                    )
                    
            except Article.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"✗ Article not found: {update['slug']}")
                )
        
        self.stdout.write(self.style.SUCCESS('\n=== SUMMARY ==='))
        self.stdout.write(self.style.SUCCESS(f'Total links added: {total_links_added}'))
        self.stdout.write(self.style.SUCCESS(f'Articles updated: {len(articles_updated)}'))
        self.stdout.write(self.style.SUCCESS('\nUpdated articles:'))
        for title in articles_updated:
            self.stdout.write(f'  - {title}')
