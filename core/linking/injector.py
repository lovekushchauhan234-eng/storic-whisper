from bs4 import BeautifulSoup
from django.urls import reverse


def inject_link(content_html: str, anchor_text: str, target_article) -> str:
    """
    Find anchor_text in content_html paragraphs and wrap it with <a> tag.
    Rules:
    - Only inject into <p> tags (not headings, not existing <a> tags)
    - Only inject the FIRST occurrence
    - Never inject into a paragraph that already contains a link to this target
    - Never inject into the first <p> of the article (intro paragraph — keep clean)
    Returns modified HTML string or original HTML if injection not possible.
    """
    soup = BeautifulSoup(content_html, 'html.parser')
    target_url = reverse('article_detail', args=[target_article.slug])
    
    paragraphs = soup.find_all('p')
    if len(paragraphs) < 2:
        return content_html   # Not enough paragraphs — skip
    
    for para in paragraphs[1:]:   # Skip first paragraph
        # Skip if already contains link to this target
        existing = para.find('a', href=lambda h: h and target_article.slug in h)
        if existing:
            continue
        
        text = para.get_text()
        if anchor_text.lower() in text.lower():
            # Find the exact case in the paragraph text
            idx = text.lower().index(anchor_text.lower())
            exact = text[idx:idx+len(anchor_text)]
            # Replace only the first occurrence via string replacement on para's HTML
            para_html = str(para)
            linked = para_html.replace(
                exact,
                f'<a href="{target_url}">{exact}</a>',
                1
            )
            para.replace_with(BeautifulSoup(linked, 'html.parser').find('p'))
            return str(soup)
    
    return content_html   # anchor_text not found — return unchanged
