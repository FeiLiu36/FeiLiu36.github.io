---
# Copy to _posts/YYYY-MM-DD-your-slug.md to publish.
title: "Essay title"
date: 2026-01-01
kind: essay            # essay | thought
lang: en               # en | zh
ref: your-slug         # same ref on the EN and ZH versions -> linked + shared comments
tags: [optimization, llm]
summary: "One or two sentences shown in the blog list."
math: false            # true to enable LaTeX ($...$, $$...$$)
comments: true
---

Opening paragraph.

## A section

Text, **bold**, [links](https://example.com), `code`.

```python
def f(x):
    return x ** 2
```

Inline math $f(x)=x^2$ and display math:

$$\min_{x \in \mathcal{X}} f(x)$$

![Alt text](/images/your-figure.png)
