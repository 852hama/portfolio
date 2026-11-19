#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static site generator for "Silva HAMA | Portfolio".

    python3 _src/build.py        (requires: pip install jinja2)

Reads  _src/content.json (texts / page structure) and _src/assets.json (image manifest)
Writes docs/index.html, profile.html, works.html, works/<slug>.html, works/index.html (redirect),
       404.html and .nojekyll.   docs/ is the folder that is published with GitHub Pages.
CSS / JS live in docs/assets/ and are edited directly. Tag lettering in _src/svg/*.svg is inlined as an SVG sprite.
All links are relative, so the site works from any sub-path (https://<user>.github.io/<repo>/).
"""
import json, os, re
from jinja2 import Environment, DictLoader, select_autoescape

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(SRC), "docs")
C = json.load(open(os.path.join(SRC, "content.json"), encoding="utf-8"))
M = json.load(open(os.path.join(SRC, "assets.json"), encoding="utf-8"))

SITE = "Silva HAMA | Portfolio"
EMAIL = C["landing"]["email"]
INSTAGRAM = C["landing"]["instagram"]
INSTAGRAM_URL = C["landing"]["instagram_url"]
CAT_TAG = {"digital": "digital-contents", "web": "web-contents", "ai": "ai-contents", "other": "other-creative"}
SVG = os.path.join(SRC, "svg")
LABEL = {k: v["text"] for k, v in M["type"].items()}
BG = ["bg-to-white", "bg-to-green"]
_sym = {}
def sym(key):
    """Symbol metadata (viewBox / size / path markup) for _src/svg/<key>.svg."""
    if key not in _sym:
        s = open(os.path.join(SVG, key + ".svg"), encoding="utf-8").read()
        vb = re.search(r'viewBox="([^"]+)"', s).group(1); w, h = [float(v) for v in vb.split()[2:]]
        path = re.search(r"<path[^>]*/>", s, re.S).group(0).replace('"#000"', '"currentColor"').replace("<path", '<path id="s-%s"' % key, 1)
        _sym[key] = {"vb": vb, "w": round(w), "h": round(h), "path": path, "text": LABEL.get(key, "")}
    USED.add(key)
    return _sym[key]
USED = set()


from markupsafe import Markup, escape

def ink(key, cls="", label=None, stretch=False):
    """Inline <svg><use> for a tag-lettering symbol; colour comes from CSS `color`."""
    s = sym(key)
    a = ' role="img" aria-label="%s"' % escape(label) if label else ' aria-hidden="true"'
    par = ' preserveAspectRatio="none"' if stretch else ""
    return Markup('<svg class="ink%s" viewBox="%s" width="%d" height="%d"%s%s focusable="false"><use href="#s-%s"/></svg>'
                  % (" " + cls if cls else "", s["vb"], s["w"], s["h"], par, a, key))

def sprite():
    return ('<svg class="sprite" width="0" height="0" aria-hidden="true" focusable="false"><defs>'
            + "".join(_sym[k]["path"] for k in sorted(USED)) + "</defs></svg>")

T = {}
T["base"] = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ page_title }}</title>
<meta name="description" content="{{ page_desc }}">
<meta name="format-detection" content="telephone=no">
<meta name="theme-color" content="#07070a">
<meta name="color-scheme" content="dark">
<meta property="og:type" content="{{ og_type|default('website') }}">
<meta property="og:site_name" content="{{ site }}">
<meta property="og:title" content="{{ page_title }}">
<meta property="og:description" content="{{ page_desc }}">
<link rel="icon" href="{{ root }}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Inter:wght@400;500;600;700&amp;family=Noto+Sans+JP:wght@400;500;700&amp;display=swap">
<link rel="stylesheet" href="{{ root }}assets/css/site.css">
<script>(function(d){var c=" js";try{if(!matchMedia("(prefers-reduced-motion: reduce)").matches){c+=sessionStorage.getItem("sh-visited")?" is-return":" is-first";sessionStorage.setItem("sh-visited","1")}}catch(e){}d.className+=c})(document.documentElement)</script>
</head>
<body class="page-{{ page }}">
<!--SPRITE-->
<div class="loader" aria-hidden="true">
  <div class="loader__in">
    {{ ink('signature', 'loader__sign') }}
    <p class="loader__txt">LOADING <span class="loader__num">0</span>%</p>
    <span class="loader__bar"></span>
  </div>
</div>
<div class="wipe" aria-hidden="true"></div>
<div class="fx" aria-hidden="true">
  <svg class="fx__curve" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid slice" focusable="false">
    <path class="fx__glow fx__a" pathLength="1" d="M-60 150C380 40 760 230 990 520S1190 990 1560 760"/>
    <path class="fx__line fx__a" pathLength="1" d="M-60 150C380 40 760 230 990 520S1190 990 1560 760"/>
    <path class="fx__glow fx__b" pathLength="1" d="M1520 60C1180 170 1050 420 760 560S250 610-80 890"/>
    <path class="fx__line fx__b" pathLength="1" d="M1520 60C1180 170 1050 420 760 560S250 610-80 890"/>
  </svg>
</div>
<a class="skip-link" href="#main">本文へスキップ</a>
<header class="site-header" id="top">
  <div class="container site-header__inner">
    <a class="brand" href="{{ root }}index.html" aria-label="Silva HAMA | Portfolio — トップページ">{{ ink('signature', 'brand__sign') }}<span class="brand__name">Silva HAMA <span class="brand__sub">| Portfolio</span></span></a>
    <nav class="gnav" aria-label="メインナビゲーション">
      <ul>
        <li><a href="{{ nav.profile }}"{% if page == 'profile' %} aria-current="page"{% endif %}>Profile</a></li>
        <li><a href="{{ nav.works }}"{% if page in ('works', 'work') %} aria-current="{{ 'page' if page == 'works' else 'true' }}"{% endif %}>Works</a></li>
        <li><a href="{{ nav.contact }}">Contact</a></li>
      </ul>
    </nav>
  </div>
</header>
<main id="main">
{% block main %}{% endblock %}
</main>
<footer class="site-footer">
  <div class="container site-footer__inner">
    <a class="brand" href="{{ root }}index.html">{{ ink('signature', 'brand__sign') }}<span class="brand__name">Silva HAMA | Portfolio</span></a>
    <nav class="fnav" aria-label="フッターナビゲーション">
      <div class="fnav__col">
        <a href="{{ root }}profile.html">Profile</a>
      </div>
      <div class="fnav__col">
        <a href="{{ root }}works.html">WORKS</a>
        <ul class="fnav__sub">
{%- for c in cats %}
          <li><a href="{{ root }}works.html#{{ c.key }}">{{ c.name }}</a></li>
{%- endfor %}
        </ul>
      </div>
      <div class="fnav__col">
        <a href="{{ root }}index.html#contact">Contact</a>
        <ul class="fnav__sub">
          <li><a href="mailto:{{ email }}">E-mail</a></li>
          <li><a href="{{ instagram_url }}" target="_blank" rel="noopener noreferrer">Instagram<img class="fnav__ext" src="{{ root }}{{ D.link_white.src }}" alt="" width="{{ D.link_white.w }}" height="{{ D.link_white.h }}"><span class="visually-hidden">（新しいタブで開く）</span></a></li>
        </ul>
      </div>
    </nav>
    <a class="totop" href="#top" aria-label="ページの先頭へ戻る"><span aria-hidden="true">TOP</span></a>
  </div>
</footer>
<script src="{{ root }}assets/js/main.js" defer></script>
</body>
</html>
"""
T["macros"] = """
{%- macro wh(a) -%}width="{{ a.w|round|int }}" height="{{ a.h|round|int }}"{%- endmacro -%}
{%- macro tagbtn(href, key, cls='', label=None, rel=None) -%}
<a class="tagbtn{{ ' ' ~ cls if cls }}" href="{{ href }}"{% if rel %} rel="{{ rel }}"{% endif %} aria-label="{{ label or LABEL[key] }}">
  <span class="tagbtn__label">{{ ink(key) }}</span>
  {{ ink('arrow', 'tagbtn__arrow', stretch=True) }}
</a>
{%- endmacro -%}
{%- macro heading(key, tag='h2', flip=False) -%}
<{{ tag }} class="heading reveal">
  {{ ink(key, 'heading__tag', LABEL[key]) }}
  {{ ink('arrow', 'heading__arrow' ~ (' is-flip' if flip else ''), stretch=True) }}
</{{ tag }}>
{%- endmacro -%}
{%- macro ghost(text, drift='-0.10') -%}
<span class="ghost" aria-hidden="true" data-drift="{{ drift }}">{{ text }}</span>
{%- endmacro -%}
{%- macro paras(ps) -%}
{%- for p in ps %}
<p>{% for l in p %}{{ l }}{% if not loop.last %}<br>{% endif %}{% endfor %}</p>
{%- endfor %}
{%- endmacro -%}
"""
T["index"] = """{% extends "base" %}{% from "macros" import wh, tagbtn, heading, ghost with context %}
{% block main %}
<section class="hero" aria-label="メインビジュアル">
  <div class="hero__media"><img class="hero__img" src="{{ root }}{{ A.hero.src }}" srcset="{{ root }}{{ A.hero_sm.src }} {{ A.hero_sm.w }}w, {{ root }}{{ A.hero.src }} {{ A.hero.w }}w" sizes="100vw" alt="東京の街並みを上空から撮影した写真" {{ wh(A.hero) }} fetchpriority="high" data-parallax="0.16"></div>
  <div class="container hero__inner">
    <h1 class="hero__title">
      <span class="visually-hidden">Silva HAMA | PORTFOLIO</span>
      <span class="hero__line hero__line--outline" aria-hidden="true"><span>Silva HAMA</span></span>
      <span class="hero__line" aria-hidden="true"><span>Portfolio<i>.</i></span></span>
    </h1>
    {{ ink('signature', 'hero__sign') }}
    <p class="hero__roles">{{ about.roles|roles }}</p>
  </div>
  <a class="scrollcue" href="#profile" aria-label="プロフィールへスクロール"><span aria-hidden="true">Scroll</span></a>
</section>

<section id="profile" class="section bg-to-green">
  {{ ghost('PROFILE', '-0.10') }}
  <div class="container">
    {{ heading('profile', flip=True) }}
    <div class="profile reveal">
      <a class="profile__photo" href="{{ root }}profile.html" aria-label="プロフィール詳細へ"><img src="{{ root }}{{ A.profile.src }}" alt="プロフィール写真（ノートPCで顔を隠したポートレート）" {{ wh(A.profile) }} loading="lazy" decoding="async"></a>
      <div class="profile__info">
        {{ ink('signature', 'profile__sign') }}
        <p class="profile__name">{{ about.name_ja }}<span aria-hidden="true">|</span>{{ about.name_kana }}</p>
        <p class="profile__meta">{{ about.birth }}<br>{{ about.roles|roles }}</p>
      </div>
      <p class="profile__intro">{{ about.intro }}</p>
      <div class="profile__more">{{ tagbtn(root ~ 'profile.html', 'more', label='More — プロフィール詳細へ') }}</div>
    </div>
  </div>
</section>

<section id="works" class="section bg-to-white">
  {{ ghost('WORKS', '0.10') }}
  <div class="container">
    {{ heading('works') }}
    <ul class="cats">
{%- for c in cats %}
      <li class="cat reveal" style="--rot:{{ c.frame_rot }}deg;--tilt:{{ c.title_rot }}deg">
        <a class="cat__thumb" href="{{ root }}works.html#{{ c.key }}" aria-label="{{ c.name }} の作品一覧へ">
          <img class="cat__photo" src="{{ root }}{{ A.cats[c.key].src }}" alt="" {{ wh(A.cats[c.key]) }} loading="lazy" decoding="async">
          {{ ink('frame', 'cat__frame') }}
        </a>
        <div class="cat__body">
          <p class="cat__no" aria-hidden="true">{{ '%02d'|format(loop.index) }}<span>/ {{ '%02d'|format(c.cards|length) }} works</span></p>
          <h3 class="cat__title">{{ ink(cat_tag[c.key], '', c.name) }}</h3>
          <ul class="chips chips--lg">
{%- for b in c.bullets %}
            <li>{{ b }}</li>
{%- endfor %}
          </ul>
        </div>
        <div class="cat__more">{{ tagbtn(root ~ 'works.html#' ~ c.key, 'more', label='More — ' ~ c.name ~ ' の作品一覧へ') }}</div>
        {{ ink('arrow', 'cat__line', stretch=True) }}
      </li>
{%- endfor %}
    </ul>
  </div>
</section>

<div class="marquee-wrap" aria-hidden="true"><div class="marquee">
  <div class="marquee__track">
{%- for i in range(2) %}{% for c in cats %}
    <span{% if loop.index is even %} class="is-solid"{% endif %}>{{ c.name }}</span><i></i>
{%- endfor %}{% endfor %}
  </div>
</div></div>

<section id="contact" class="section bg-to-green">
  {{ ghost('CONTACT', '-0.10') }}
  <div class="container">
    {{ heading('contact', flip=True) }}
    <div class="contact__sign reveal">{{ ink('signature', '', 'Silva HAMA のサイン') }}</div>
    <ul class="contact__list">
      <li class="reveal"><a class="contact__link" href="mailto:{{ email }}">
        <img class="contact__icon" src="{{ root }}{{ D.mail.src }}" alt="" {{ wh(D.mail) }} loading="lazy">
        <span class="contact__text"><span class="visually-hidden">E-mail：</span>{{ email }}</span>
      </a></li>
      <li class="reveal"><a class="contact__link" href="{{ instagram_url }}" target="_blank" rel="noopener noreferrer">
        <img class="contact__icon" src="{{ root }}{{ D.instagram.src }}" alt="" {{ wh(D.instagram) }} loading="lazy">
        <span class="contact__text"><span class="visually-hidden">Instagram：</span>{{ instagram }}<img class="contact__ext" src="{{ root }}{{ D.link_white.src }}" alt="" {{ wh(D.link_white) }}><span class="visually-hidden">（新しいタブで開く）</span></span>
      </a></li>
    </ul>
  </div>
</section>
{% endblock %}
"""
T["works"] = """{% extends "base" %}{% from "macros" import wh, ghost with context %}
{% block main %}
<section class="works-hero">
  <div class="works-hero__strips" aria-hidden="true">
{%- for s in A.strips %}
    <img src="{{ root }}{{ s.src }}" alt="" {{ wh(s) }} style="--i:{{ loop.index0 }}">
{%- endfor %}
  </div>
  <div class="container works-hero__inner">
    <h1 class="works-hero__title"><span class="hero__line"><span>Works</span></span></h1>
    <p class="works-hero__meta">{{ works|length }} Projects <span aria-hidden="true">/</span> {{ cats|length }} Categories</p>
    <ul class="catnav" aria-label="カテゴリーへ移動">
{%- for c in cats %}
      <li><a href="#{{ c.key }}"><span aria-hidden="true">{{ '%02d'|format(loop.index) }}</span>{{ c.name }}</a></li>
{%- endfor %}
    </ul>
  </div>
</section>
{% for c in cats %}
<section id="{{ c.key }}" class="section {{ bg[loop.index0 % 2] }}">
  {{ ghost(c.name|upper, '-0.10' if loop.index is odd else '0.10') }}
  <div class="container">
    <header class="cat-head reveal">
      <h2 class="cat-head__title">{{ ink(cat_tag[c.key], 'cat-head__tag', c.name) }}</h2>
      {{ ink('arrow', 'cat-head__arrow', stretch=True) }}
      <ul class="chips chips--lg">
{%- for b in c.works_bullets %}
        <li>{{ b }}</li>
{%- endfor %}
      </ul>
    </header>
    <ul class="cards">
{%- for slug in c.cards %}{% set w = works[slug] %}
      <li class="reveal"><a class="card" href="{{ root }}works/{{ slug }}.html">
        <span class="card__media">
          <span class="card__clip"><img class="card__img" src="{{ root }}{{ A.works[slug].thumb.src }}" alt="" {{ wh(A.works[slug].thumb) }} loading="lazy" decoding="async"></span>
          <img class="card__frame" src="{{ root }}{{ D.paper_frame.src }}" alt="" {{ wh(D.paper_frame) }}>
          <span class="card__no" aria-hidden="true">{{ '%02d'|format(loop.index) }}</span>
        </span>
        <span class="card__client">{{ w.card.client }}</span>
        <span class="card__title"><span>{{ w.card.project }}</span></span>
        <span class="chips">
{%- for t in w.card.tags %}
          <span class="chip">{{ t }}</span>
{%- endfor %}
        </span>
      </a></li>
{%- endfor %}
    </ul>
  </div>
</section>
{% endfor %}
{% endblock %}
"""
T["work"] = """{% extends "base" %}{% from "macros" import wh, tagbtn, paras, ghost with context %}
{% block main %}
<article class="work">
  <div class="section work__top bg-to-white">
    {{ ghost(cat.name|upper, '-0.08') }}
    <div class="container">
      <p class="work__cat"><a class="chip chip--link" href="{{ root }}works.html#{{ cat.key }}">{{ cat.name }}</a><span class="work__no" aria-hidden="true">{{ '%02d'|format(pos) }} / {{ '%02d'|format(cat.cards|length) }}</span></p>
      <h1 class="work__title">{{ w.title }}</h1>
      <p class="work__client">{{ w.client }}</p>
      <div class="work__lead">{{ paras(w.lead) }}</div>
      <div class="work__hero reveal reveal--wipe">
        <div class="work__hero-main"{% if a.hero.side %} style="--ar:{{ a.hero.main.ar }}"{% endif %}>
          <a class="zoom" href="{{ root }}{{ a.hero.main.full }}" data-zoom><img src="{{ root }}{{ a.hero.main.src }}"{% if a.hero.main.w > 1000 %} srcset="{{ root }}{{ a.hero.main.sm }} 1000w, {{ root }}{{ a.hero.main.src }} {{ a.hero.main.w }}w" sizes="(min-width: 1400px) 1240px, 92vw"{% endif %} alt="{{ w.title }} のメインビジュアル" {{ wh(a.hero.main) }} fetchpriority="high"></a>
        </div>
{%- if a.hero.side %}
        <div class="work__hero-side" style="--ar:{{ a.hero.side_ar }}">
{%- for s in a.hero.side %}
          <a class="zoom" href="{{ root }}{{ s.full }}" data-zoom style="--ar:{{ s.ar }}"><img src="{{ root }}{{ s.src }}" alt="{{ w.title }} の制作物 {{ loop.index + 1 }}" {{ wh(s) }} decoding="async"></a>
{%- endfor %}
        </div>
{%- endif %}
      </div>
      <section class="spec reveal">
        <h2 class="spec__label">Overview</h2>
        <div class="spec__body prose">{{ paras(w.overview) }}</div>
      </section>
{%- if w.award %}
      <section class="spec reveal">
        <h2 class="spec__label">Award</h2>
        <div class="spec__body"><p class="spec__award">{{ w.award }}</p></div>
      </section>
{%- endif %}
    </div>
  </div>
  <div class="section work__bottom bg-to-green">
    <div class="container">
      <div class="gallery reveal">
{%- set ns = namespace(n=a.hero.side|length + 1) %}
{%- for row in a.gallery %}
        <div class="gallery__row">
{%- for cell in row %}
          <div class="gallery__cell" style="--ar:{{ cell.ar }}">
{%- for g in cell.imgs %}{% set ns.n = ns.n + 1 %}
            <a class="zoom" href="{{ root }}{{ g.full }}" data-zoom style="--ar:{{ g.ar }}"><img src="{{ root }}{{ g.src }}" alt="{{ w.title }} の制作物 {{ ns.n }}" {{ wh(g) }} loading="lazy" decoding="async"></a>
{%- endfor %}
          </div>
{%- endfor %}
        </div>
{%- endfor %}
{%- if w.credit %}
        <p class="gallery__credit">{{ w.credit }}</p>
{%- endif %}
      </div>
      <section class="spec reveal">
        <h2 class="spec__label">URL</h2>
        <div class="spec__body">
{%- if w.url %}
          <ul class="spec__urls">
            <li><a class="spec__url" href="{{ w.url }}" target="_blank" rel="noopener noreferrer"><span>{{ w.url_text }}</span><img src="{{ root }}{{ D.link_white.src }}" alt="" {{ wh(D.link_white) }}><span class="visually-hidden">（新しいタブで開く）</span></a></li>
{%- for r in w.refs or [] %}
            <li><a class="spec__url" href="{{ r.url }}" target="_blank" rel="noopener noreferrer"><span>{{ r.url }}</span><img src="{{ root }}{{ D.link_white.src }}" alt="" {{ wh(D.link_white) }}><span class="visually-hidden">（新しいタブで開く）</span></a></li>
{%- endfor %}
          </ul>
{%- else %}
          <p>{{ w.url_note }}</p>
{%- endif %}
        </div>
      </section>
      <section class="spec reveal">
        <h2 class="spec__label">Position</h2>
        <div class="spec__body">
{%- if w.role %}
          <p class="spec__role">{{ w.role|roles }}</p>
{%- endif %}
          <div class="prose">{{ paras(w.body) }}</div>
        </div>
      </section>
      <nav class="pager reveal" aria-label="作品ナビゲーション">
        {{ tagbtn(root ~ 'works/' ~ w.prev ~ '.html', 'back', 'tagbtn--back', label='BACK — 前の作品：' ~ works[w.prev].title, rel='prev') }}
        {{ tagbtn(root ~ 'works/' ~ w.next ~ '.html', 'next', 'tagbtn--next', label='NEXT — 次の作品：' ~ works[w.next].title, rel='next') }}
        {{ tagbtn(root ~ 'works.html#' ~ cat.key, 'back-to-works', 'tagbtn--up', label='BACK to WORKS — 作品一覧へ戻る') }}
      </nav>
    </div>
  </div>
</article>
{% endblock %}
"""
T["profile"] = """{% extends "base" %}{% from "macros" import wh, heading, ghost with context %}
{% block main %}
<div class="section section--first bg-to-mint">
  {{ ghost('PROFILE', '-0.08') }}
  <div class="container">
    {{ heading('profile', tag='h1', flip=True) }}
    <div class="about reveal">
      <button class="flip" type="button" aria-pressed="false" aria-label="プロフィール写真を切り替える">
        <img src="{{ root }}{{ A.profile.src }}" alt="プロフィール写真（ノートPCで顔を隠したポートレート）" {{ wh(A.profile) }}>
        <img class="flip__alt" src="{{ root }}{{ A.profile_alt.src }}" alt="" {{ wh(A.profile_alt) }}>
      </button>
      <div class="about__info">
        {{ ink('signature', 'about__sign') }}
        <p class="about__name">{{ about.name_ja }}<span aria-hidden="true">|</span>{{ about.name_kana }}</p>
        <p class="about__meta">{{ about.birth }}<br>{{ about.roles|roles }}</p>
      </div>
      <p class="about__intro">{{ about.intro }}</p>
    </div>

    <section class="spec reveal">
      <h2 class="spec__label spec__label--ja">学歴</h2>
      <div class="spec__body">
        <ol class="timeline">
{%- for g in about.history.edu %}{% for e in g %}
          <li class="timeline__item">{% if e.year %}<span class="timeline__year">{{ e.year }}年</span>{% endif %}<span class="timeline__main">{{ e.text }}</span>{% if e.detail %}<span class="timeline__detail">{{ e.detail|phrases }}</span>{% endif %}</li>
{%- endfor %}{% endfor %}
        </ol>
      </div>
    </section>
    <section class="spec reveal">
      <h2 class="spec__label spec__label--ja">職歴</h2>
      <div class="spec__body">
        <ol class="timeline">
{%- for g in about.history.career %}
{%- if not loop.first %}
          <li class="timeline__arrow" aria-hidden="true">{{ ink('arrow', '', stretch=True) }}</li>
{%- endif %}
{%- for e in g %}
          <li class="timeline__item">{% if e.year %}<span class="timeline__year">{{ e.year }}年</span>{% endif %}<span class="timeline__main">{{ e.text }}</span>{% if e.detail %}<span class="timeline__detail">{{ e.detail|phrases }}</span>{% endif %}</li>
{%- endfor %}
{%- endfor %}
        </ol>
      </div>
    </section>

    <h2 class="heading-line reveal">
      {{ ink('skill-set', 'heading-line__tag', 'SKILL SET') }}
      {{ ink('arrow', 'heading-line__arrow is-flip', stretch=True) }}
    </h2>
    <section class="spec reveal">
      <h3 class="spec__label spec__label--ja">職務経歴</h3>
      <div class="spec__body">
        <ul class="bars">
{%- for e in about.exp %}
          <li class="bars__item"><span class="bars__label">{{ e.label }}</span><span class="bars__track" aria-hidden="true"><span class="bars__fill" style="--v:{{ '%.1f'|format(e.years / exp_max * 100) }}%"></span></span><span class="bars__val">{{ e.value }}</span></li>
{%- endfor %}
        </ul>
      </div>
    </section>
    <section class="spec reveal">
      <h3 class="spec__label spec__label--ja">技術スキルセット<small>ソフトウェア</small></h3>
      <div class="spec__body skills">
{%- for g in about.software %}
        <div class="skills__group">
          <h4 class="skills__title">{{ g.group }}</h4>
          <dl class="deflist">
{%- for i in g['items'] %}
            <div><dt>{{ i.name }}</dt><dd>{{ i.desc }}</dd></div>
{%- endfor %}
          </dl>
        </div>
{%- endfor %}
      </div>
    </section>
    <section class="spec reveal">
      <h3 class="spec__label spec__label--ja">技術スキルセット<small>デジタルファブリケーション機材</small></h3>
      <div class="spec__body">
        <ul class="deflist deflist--cols">
{%- for f in about.fab %}
          <li><strong class="deflist__name">{{ f.name }}</strong>{% for d in f.desc %}<span class="deflist__desc">{{ d }}</span>{% endfor %}</li>
{%- endfor %}
        </ul>
      </div>
    </section>

    <h2 class="heading-line reveal">
      {{ ink('hobby', 'heading-line__tag', 'HOBBY') }}
      {{ ink('arrow', 'heading-line__arrow is-flip', stretch=True) }}
    </h2>
    <div class="hobby">
{%- for row in hobby_rows %}
      <div class="hobby__row reveal">
{%- for g in row %}
        <figure class="hobby__group" style="--ar:{{ g.ar }}">
          <div class="hobby__imgs">
{%- for i in g.imgs %}
            <img src="{{ root }}{{ i.src }}" alt="{{ g.label }} の写真{% if g.imgs|length > 1 %} {{ loop.index }}{% endif %}" {{ wh(i) }} style="--ar:{{ i.ar }}" loading="lazy" decoding="async">
{%- endfor %}
          </div>
          <figcaption class="hobby__label">{{ g.label }}</figcaption>
        </figure>
{%- endfor %}
      </div>
{%- endfor %}
    </div>
  </div>
</div>
{% endblock %}
"""

# --- GitHub Pages extras ---------------------------------------------------------------------
# 404.html is served for ANY missing URL below the site root, so it cannot use relative paths:
# everything is inlined and the links are pointed at the site root by a tiny script that finds
# the root by probing for favicon.svg ("/<repo>/" for project sites, "/" for user sites / custom domains).
T["notfound"] = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>404 Not Found | {{ site }}</title>
<meta name="robots" content="noindex">
<meta name="theme-color" content="#07070a">
<meta name="color-scheme" content="dark">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&amp;family=Inter:wght@400;500;600;700&amp;family=Noto+Sans+JP:wght@400;500;700&amp;display=swap">
<style>
:root{--bg:#07070a;--ink:#ecebe6;--muted:rgba(236,235,230,.66);--green:#1fe86a}
*,*::before,*::after{box-sizing:border-box}
html{background:var(--bg);color-scheme:dark;-webkit-text-size-adjust:100%;text-size-adjust:100%}
body{margin:0;min-height:100vh;min-height:100svh;display:grid;place-items:center;padding:clamp(24px,6vw,80px);overflow-x:hidden;color:var(--muted);font:400 1rem/1.8 "Inter","Noto Sans JP","Hiragino Kaku Gothic ProN","Hiragino Sans","Yu Gothic UI","Yu Gothic",Meiryo,system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-font-smoothing:antialiased;background-color:var(--bg);background-image:radial-gradient(70% 55% at 10% 78%,rgba(31,232,106,.12),rgba(31,232,106,0) 72%),radial-gradient(70% 55% at 92% 16%,rgba(123,92,255,.15),rgba(123,92,255,0) 72%),radial-gradient(rgba(236,235,230,.075) 1px,transparent 1.6px);background-size:auto,auto,56px 56px}
.sprite{position:absolute;width:0;height:0;overflow:hidden}
.nf{position:relative;width:min(100%,900px)}
.nf__sign{display:block;width:clamp(130px,24vw,240px);height:auto;margin:0 0 clamp(4px,1.4vw,14px) -4px;color:var(--green);fill:currentColor;overflow:visible;transform:rotate(-6deg)}
.nf__code{margin:0;color:transparent;font:400 clamp(120px,33vw,340px)/.9 "Anton","Impact","Haettenschweiler","Arial Narrow Bold",sans-serif;letter-spacing:.01em;-webkit-text-stroke:2px var(--ink)}
.nf__code i{color:var(--green);font-style:normal;-webkit-text-stroke:0}
@supports not (-webkit-text-stroke:1px #000){.nf__code{color:var(--ink)}}
.nf__title{margin:clamp(14px,2.2vw,26px) 0 0;padding-left:58px;background-image:linear-gradient(var(--green),var(--green));background-position:0 50%;background-size:44px 2px;background-repeat:no-repeat;color:var(--ink);font:400 clamp(1.25rem,1rem + 1.6vw,2rem)/1.3 "Anton","Impact","Arial Narrow Bold",sans-serif;letter-spacing:.14em;text-transform:uppercase}
.nf__text{max-width:36em;margin:clamp(12px,2vw,20px) 0 0;color:var(--ink);font-weight:500}
.nf__nav{display:flex;flex-wrap:wrap;gap:10px;margin:clamp(24px,4vw,40px) 0 0;padding:0;list-style:none}
.nf__nav a{display:inline-block;padding:.62em 1.5em;border:1px solid rgba(236,235,230,.36);color:var(--ink);font:400 1rem/1.5 "Anton","Impact","Arial Narrow Bold",sans-serif;letter-spacing:.16em;text-indent:.16em;text-decoration:none;text-transform:uppercase;transition:background-color .25s,color .25s,border-color .25s}
.nf__nav li:first-child a,.nf__nav a:hover,.nf__nav a:focus-visible{background:var(--green);border-color:var(--green);color:#000}
.nf__nav li:first-child a:hover,.nf__nav li:first-child a:focus-visible{background:transparent;color:var(--green)}
:focus-visible{outline:2px solid var(--green);outline-offset:4px}
</style>
</head>
<body>
<!--SPRITE-->
<main class="nf">
  {{ ink('signature', 'nf__sign') }}
  <p class="nf__code" aria-hidden="true">404<i>.</i></p>
  <h1 class="nf__title">Page not found</h1>
  <p class="nf__text">お探しのページは見つかりませんでした。移動または削除されたか、URL が間違っている可能性があります。</p>
  <ul class="nf__nav">
    <li><a href="./" data-href="index.html">Top</a></li>
    <li hidden><a href="./" data-href="works.html">Works</a></li>
    <li hidden><a href="./" data-href="profile.html">Profile</a></li>
  </ul>
</main>
<script>
(function (d) {
  var p = location.pathname, seg = p.split("/")[1] || "", c = [], i = 0;
  if (/\\/404(\\.html)?$/.test(p)) c.push("./");          // the file itself was opened
  if (seg) c.push("/" + seg + "/");                       // project site: https://<user>.github.io/<repo>/
  c.push("/");                                            // user site or custom domain
  function use(base) {
    [].forEach.call(d.querySelectorAll("[data-href]"), function (a) {
      a.href = base + a.getAttribute("data-href");
      a.parentNode.hidden = false;
    });
    var l = d.createElement("link");
    l.rel = "icon"; l.type = "image/svg+xml"; l.href = base + "favicon.svg";
    d.head.appendChild(l);
  }
  (function next() {
    if (i >= c.length) return;                            // nothing found: keep the plain "./" link
    var base = c[i++], im = new Image();
    im.onload = function () { use(base); };
    im.onerror = next;
    im.src = base + "favicon.svg";
  })();
})(document);
</script>
</body>
</html>
"""
# works/ has no page of its own (the list is works.html); send /works/ there instead of a 404.
T["redirect"] = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ page_title }}</title>
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={{ to }}">
<script>location.replace("{{ to }}" + location.hash);</script>
</head>
<body>
<p><a href="{{ to }}">{{ label }}</a></p>
</body>
</html>
"""

env = Environment(loader=DictLoader(T), autoescape=select_autoescape(default=True, default_for_string=True), trim_blocks=False, lstrip_blocks=False)

env.globals.update(ink=ink, LABEL=LABEL)

_ROLE_NOUN = re.compile(r"^(.{3,}?)(プロデューサー|ディレクター|プランナー|デザイナー|エディター|マネージャー|リーダー)$")
def roles(s):
    """'A・B・C' -> one unbreakable chunk per title, so a list of titles only wraps between titles.
    A title that is wider than the line on its own (narrow phones) breaks before its last word
    ('デジタルアクティベーション' / 'プロデューサー') instead of in the middle of a word."""
    parts = [p for p in str(s).split("・") if p]
    out = []
    for i, p in enumerate(parts):
        sep = "・" if i < len(parts) - 1 else ""
        m = _ROLE_NOUN.match(p)
        inner = ('<span class="nb">%s</span><span class="nb">%s%s</span>' % (escape(m.group(1)), escape(m.group(2)), sep)) if m else "%s%s" % (escape(p), sep)
        out.append('<span class="nb">%s</span>' % inner)
    return Markup("".join(out))
env.filters["roles"] = roles

def phrases(v):
    """Text that should wrap only at chosen places: a list of parts -> one chunk (.nb) per part, so the line
    wraps between parts and not inside them. A part may itself be a list of parts (used when it is wider than
    a narrow phone line). A plain string is output as it is."""
    if isinstance(v, (list, tuple)):
        return Markup("".join('<span class="nb">%s</span>' % phrases(p) for p in v))
    return escape(v)
env.filters["phrases"] = phrases

def oneline(s, n=118):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[: n - 1] + "…"

about = dict(C["about"])
about["name_ja"], about["name_kana"] = [s.strip() for s in about["name"].split("|", 1)]
hob = M["hobby"]
HOBBY_ROWS = [hob[0:3], hob[3:5], hob[5:8]]        # same grouping as the Figma layout
cat_by_key = {c["key"]: c for c in C["cats"]}

def render(name, path, root, page, **ctx):
    nav = ({"profile": "#profile", "works": "#works", "contact": "#contact"} if page == "home" else
           {"profile": root + "profile.html", "works": root + "works.html", "contact": root + "index.html#contact"})
    USED.clear()
    html = env.get_template(name).render(root=root, page=page, nav=nav, site=SITE, cats=C["cats"], works=C["works"], A=M, D=M["deco"], TY=M["type"],
                                         about=about, email=EMAIL, instagram=INSTAGRAM, instagram_url=INSTAGRAM_URL, cat_tag=CAT_TAG, bg=BG, **ctx)
    html = html.replace("<!--SPRITE-->", sprite())
    html = "\n".join(l.rstrip() for l in html.split("\n") if l.strip()) + "\n"
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    return path

intro = about["intro"]
pages = []
pages.append(render("index", "index.html", "", "home", page_title=SITE,
                    page_desc=oneline(f'{about["roles"]} {about["name_ja"]}（Silva HAMA）のポートフォリオサイト。{intro}', 140)))
pages.append(render("profile", "profile.html", "", "profile", page_title=f"Profile | {SITE}", og_type="profile",
                    page_desc=oneline(f'{about["name_ja"]}（{about["name_kana"]}）のプロフィール。{intro}', 140),
                    hobby_rows=HOBBY_ROWS, exp_max=max(e["years"] for e in about["exp"])))
pages.append(render("works", "works.html", "", "works", page_title=f"Works | {SITE}",
                    page_desc="Silva HAMA の制作実績一覧。" + " / ".join(c["name"] for c in C["cats"]) + " の各カテゴリーの仕事を掲載しています。"))
for slug, w in C["works"].items():
    lead = " ".join(" ".join(p) for p in w["lead"])
    pages.append(render("work", f"works/{slug}.html", "../", "work", w=w, a=M["works"][slug], cat=cat_by_key[w["cat"]], pos=cat_by_key[w["cat"]]["cards"].index(slug) + 1, og_type="article",
                        page_title=f'{w["title"]} | Works | {SITE}', page_desc=oneline(f'{w["client"]}｜{lead}', 140)))

# --- GitHub Pages extras -----------------------------------------------------------------------
def write(path, text):
    with open(os.path.join(OUT, path), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

USED.clear()
nf = env.get_template("notfound").render(site=SITE).replace("<!--SPRITE-->", sprite())
write("404.html", "\n".join(l.rstrip() for l in nf.split("\n") if l.strip()) + "\n")
write("works/index.html", env.get_template("redirect").render(to="../works.html", label="Works", page_title=f"Works | {SITE}").rstrip("\n") + "\n")
write(".nojekyll", "")          # tells GitHub Pages to publish the files as they are (no Jekyll build)
print(f"built {len(pages)} pages + 404.html + works/index.html (redirect) -> {OUT}")

# GitHub's browser upload takes at most 100 files per upload and 25 MiB per file:
# keep every top-level folder (and the first batch: loose files + assets + works) within that.
LIMIT, MAXSIZE = 100, 25 * 1024 * 1024
count = {}
for d, _, fs in os.walk(OUT):
    rel = os.path.relpath(d, OUT)
    top = "(files)" if rel == "." else rel.split(os.sep)[0]
    count[top] = count.get(top, 0) + len(fs)
    for f in fs:
        if os.path.getsize(os.path.join(d, f)) > MAXSIZE:
            print(f"WARNING: {os.path.join(rel, f)} is larger than 25 MiB (cannot be uploaded in the browser)")
first = ["(files)", "assets", "works"]
batches = [("+".join(first), sum(count.get(k, 0) for k in first))] + sorted((k, v) for k, v in count.items() if k not in first)
print("upload batches: " + " / ".join(f"{k} {v}" for k, v in batches) + f" / total {sum(count.values())} files")
for k, v in batches:
    if v > LIMIT:
        print(f"WARNING: {k} has {v} files (> {LIMIT}); upload its sub-folders in two or more batches")
