---
layout: page
permalink: /publications/
title: publications
description: available soon
years: [2019, 2020, 2021, 2022, 2023]
nav: true
nav_order: 3
---
<!-- _pages/publications.md -->
<div class="publications">

{%- for y in page.years %}
  <h2 class="year">{{y}}</h2>
  {% bibliography -f papers -q @*[year={{y}}]* %}
{% endfor %}

</div>
