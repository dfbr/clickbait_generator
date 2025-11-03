---
layout: default
title: Home
---

# Latest Stories

<div class="post-grid">
  {% for post in site.posts %}
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
          <span class="post-card-date">{{ post.date | date: "%B %d, %Y" }}</span>
        </div>
      </a>
    </article>
  {% endfor %}
</div>
