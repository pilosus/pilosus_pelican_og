Pilosus Open Graph Pluging
==========================

Expand Article and Page entities with Open Graph Protocol tags.


Installation
------------

1. Place plugin in a directory, e.g ``plugins/pilosus_pelican_og``

2. Add plugins configurations in a settings file:

.. code-block:: python

  PLUGIN_PATHS = ['plugins']
  PLUGINS = ['pilosus_pelican_og',]


Usage
-----

1. Use the following tags in your content's `metadata`_ section:

.. code-block:: python

  og_title (article title used by default)
  og_type (article by default)
  og_image (abolute or relative path to an image, DEFAULT_OG_IMAGE config used by default)
  og_url
  og_description (summary used by default)
  og_locale (LOCALE config used by default)
  og_site_name
  og_see_also
  article_author 
  article_published_time
  article_modified_time
  article_section
  article_tag

  
2.  Place this snippet in your ``base.html`` template inside of the ``head`` tag:

.. code-block:: jinja2

  {% if article and article.og %}
  {% for tag in article.og %}
  <meta property="{{tag[0]}}" content="{{tag[1]|striptags|e}}" />
  {% endfor %}
  {% endif %}

  {% if page and page.og %}
  {% for tag in page.og %}
  <meta property="{{tag[0]}}" content="{{tag[1]|striptags|e}}" />
  {% endfor %}
  {% endif %}


License
-------

This work is based upon an original work of ``whiskyechobravo`` that
can be found under: https://github.com//pelican-open_graph

This work is licensed under GNU AFFERO GENERAL PUBLIC LICENSE Version 3

.. _metadata: https://docs.getpelican.com/en/stable/content.html#file-metadata
