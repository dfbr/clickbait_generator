---
layout: default
title: Home
---

<div class="post-grid">
  {% for post in paginator.posts %}
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

{% if paginator.total_pages > 1 %}
  <nav class="pagination">
    {% if paginator.previous_page %}
      <a href="{{ paginator.previous_page_path | relative_url }}" class="pagination-link">← Newer</a>
    {% endif %}

    {% for page_number in (1..paginator.total_pages) %}
      {% if page_number == paginator.page %}
        <span class="pagination-link pagination-link-current">{{ page_number }}</span>
      {% elsif page_number == 1 %}
        <a href="{{ '/' | relative_url }}" class="pagination-link">{{ page_number }}</a>
      {% else %}
        <a href="{{ site.paginate_path | replace: ':num', page_number | relative_url }}" class="pagination-link">{{ page_number }}</a>
      {% endif %}
    {% endfor %}

    {% if paginator.next_page %}
      <a href="{{ paginator.next_page_path | relative_url }}" class="pagination-link">Older →</a>
    {% endif %}
  </nav>
{% endif %}
