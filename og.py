# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

from urllib.parse import urlparse
import os.path

from pelican import generators, signals
from pelican.utils import strftime


def process_generators(content_generators):
    """
    Process Article and Page generators
    """
    for generator in content_generators:
        if isinstance(generator, generators.ArticlesGenerator):
            for article in (
                    generator.articles +
                    generator.translations +
                    generator.drafts):
                open_graph_tag(article)
        elif isinstance(generator, generators.PagesGenerator):
            for page in generator.pages:
                open_graph_tag(page)

    return True


def open_graph_tag(item):
    """
    Process single item (article or page)

    Access the following meta tags:
    og:title
    og:type
    og:image
    og:url
    og:description
    og:locale
    og:site_name
    og:see_also
    article:author
    article:published_time
    article:modified_time
    article:section
    article:tag
    """
    # Predefined tags
    og_tags = [('og:title', item.title),
              ('og:type', 'article')]

    # og:image explicitly or via DEFAULT_OG_IMAGE variable in settings
    default_image = item.settings.get('DEFAULT_OG_IMAGE')
    
    image = item.metadata.get('og_image', '')
    if image:
        og_tags.append(('og:image', image))
    else:
        if default_image:
            image_url = urlparse(default_image)
            if not image_url.scheme:
                if item.settings.get('SITEURL', ''):
                    default_image = "{0}/{1}".format(
                        item.settings.get('SITEURL', ''),
                        default_image)
            og_tags.append(('og:image', default_image))

    # og:url
    url = os.path.join(item.settings.get('SITEURL', ''), item.url)
    og_tags.append(('og:url', url))

    # og:description
    default_summary = item.summary
    description = item.metadata.get('og_description', default_summary)
    og_tags.append(('og:description', description))

    # og:locale
    default_locale = item.settings.get('LOCALE', [])
    if default_locale:
        default_locale = default_locale[0]
    else:
        default_locale = ''
    og_tags.append(
        ('og:locale', item.metadata.get('og_locale', default_locale)))

    # og:site_name
    og_tags.append(('og:site_name', item.settings.get('SITENAME', '')))

    # article:published_time
    if hasattr(item, 'date'):
        og_tags.append(('article:published_time',
            strftime(item.date, "%Y-%m-%d")))

    # article:modified_time
    if hasattr(item, 'modified'):
        og_tags.append(('article:modified_time', strftime(
            item.modified, "%Y-%m-%d")))

    # og:see_also
    if hasattr(item, 'related_posts'):
        for related_post in item.related_posts:
            url = os.path.join(item.settings.get('SITEURL', ''), related_post.url)
            og_tags.append(('og:see_also', url))

    # article:author, link author Facebook account vie AUTHOR_FB_ID variable in settings
    author_fb_profiles = item.settings.get('AUTHOR_FB_ID', {})
    if len(author_fb_profiles) > 0:
        for author in item.authors:
            if author.name in author_fb_profiles:
                og_tags.append(
                    ('article:author', author_fb_profiles[author.name]))

    # article:section
    og_tags.append(('article:section', item.category.name))

    # article:tag    
    try:
        for tag in item.tags:
            og_tags.append(('article:tag', tag.name))
    except AttributeError:
        pass

    item.og = og_tags


def register():
    """
    Pelican plugin entrypoint
    """
    signals.all_generators_finalized.connect(process_generators)
