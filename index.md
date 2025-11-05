---
layout: default
title: Home
---

<div class="post-grid">
  {% assign featured = site.posts | where: "featured", true | first %}
  {% if featured %}
    <section class="featured-post">
      <article class="post-featured">
        <a href="{{ featured.url | relative_url }}">
          {% if featured.image %}
            <img src="{{ featured.image | relative_url }}" alt="{{ featured.title }}" style="width:100%; height:auto; border-radius:8px;">
          {% endif %}
          <h1>{{ featured.title }}</h1>
          {% if featured.summary %}<p>{{ featured.summary }}</p>{% endif %}
          <p class="post-meta">Published {% include ordinal_date.html date=featured.date %} {% if featured.author %}— By {{ featured.author }}{% endif %}</p>
        </a>
      </article>
    </section>
  {% endif %}

  {% assign others = site.posts %}
  {% if featured %}
    {% assign others = site.posts | where_exp: "p", "p.url != featured.url" %}
  {% endif %}
  {% for post in others %}
    <article class="post-card">
      <a href="{{ post.url | relative_url }}" class="post-card-link">
        {% if post.preview_image %}
          <img src="{{ post.preview_image | relative_url }}" alt="{{ post.title }}" class="post-card-image">
        {% endif %}
        <div class="post-card-content">
          <h2>{{ post.title }}</h2>
          {% if post.summary %}
            <p class="post-card-summary">{{ post.summary }}</p>
          {% endif %}
          <span class="post-card-date">{% include ordinal_date.html date=post.date %}</span>
        </div>
      </a>
    </article>
  {% endfor %}
</div>
