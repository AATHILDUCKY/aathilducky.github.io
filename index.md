---
layout: default
---

<h2>Filter by Tags</h2>
<input type="text" id="keyword-input" placeholder="Enter comma-separated tags">
<div id="selected-tags"></div>
<hr>

<div id="notes">
  {% for note in site.notes %}
    <div class="note" 
         data-tags="{{ note.tags | join: ',' | downcase }}" 
         data-title="{{ note.title }}">
      <h3>{{ note.title }}</h3>
      <p><strong>Tags:</strong> {{ note.tags | join: ', ' }}</p>
      {{ note.content }}
    </div>
  {% endfor %}
</div>

<script src="/assets/js/filter.js"></script>
