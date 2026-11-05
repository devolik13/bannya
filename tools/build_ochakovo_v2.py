"""Пересобирает из tilda-snippets/ochakovo-intro-faq.md (единый источник текстов):
- tilda-snippets/ochakovo-jsonld.html (Organization, LocalBusiness+Offer, FAQPage, BreadcrumbList)
- вводный абзац, сетку фактов и приложение FAQ в tilda-snippets/ochakovo-volna2-tz.md
- макет (блоки rec-mock-intro / rec-mock-faq и JSON-LD) в page30467207.html — только полигон.
Запуск из корня репозитория: python3 tools/build_ochakovo_v2.py"""
import re, json, html

MD = 'tilda-snippets/ochakovo-intro-faq.md'
md = open(MD, encoding='utf-8').read()
intro = ' '.join(l[2:] for l in re.search(r'## 2\.[\s\S]*?\n((?:> .*\n)+)', md).group(1).splitlines())
faq = re.findall(r'\*\*(.+?\?)\*\*\n(.+)', re.search(r'## 3\.[\s\S]*?(?=\n---)', md).group(0))
faq = [(q, a) for q, a in faq if 'ПОДСТАВИТЬ' not in a and 'ПРОВЕРИТЬ' not in a]

# Срубы: название, ₽/час, вместимость, число парных, бассейн
SRUBS = [("Княжеский", 13000, 15, 2, True), ("Мужские забавы", 11000, 12, 2, True),
         ("Форт", 9000, 8, 1, True), ("Африка", 9000, 8, 1, True), ("Русская изба", 9000, 8, 1, True),
         ("Садко", 9000, 8, 1, True), ("Сибирский", 9000, 8, 1, True),
         ("Осенний", 6000, 6, 1, False), ("Летний", 6000, 6, 1, False),
         ("Зимняя сказка", 6000, 6, 1, False), ("Весенний", 6000, 6, 1, False)]

def offer(n, p, c, steam, pool):
    parts = ["2 парные на дровах" if steam == 2 else "парная на дровах", "купель"]
    if pool: parts.append("подогреваемый бассейн на улице")
    return {"@type": "Offer", "name": f"Аренда сруба «{n}»",
            "description": f"Отдельный сруб до {c} человек: {', '.join(parts)}. Минимальная аренда 3 часа",
            "itemOffered": {"@type": "Service", "name": f"Сруб «{n}»"},
            "priceSpecification": {"@type": "UnitPriceSpecification", "price": p, "priceCurrency": "RUB", "unitText": "час"}}

feat = lambda name: {"@type": "LocationFeatureSpecification", "name": name, "value": True}
graph = [
    {"@type": "Organization", "@id": "https://banniy-dvor.ru/#organization", "name": "Банный двор", "url": "https://banniy-dvor.ru/"},
    {"@type": "LocalBusiness", "@id": "https://banniy-dvor.ru/ochakovo#business",
     "name": "Банный двор Очаково", "alternateName": "Банный двор на Очаковском шоссе",
     "description": "Банный комплекс из 11 отдельных срубов. В каждом срубе своя парная на дровах и купель, в 7 срубах — подогреваемый бассейн на улице. Вместимость от 6 до 15 человек, от 6 000 до 13 000 ₽ в час, минимальная аренда 3 часа, круглосуточно.",
     "url": "https://banniy-dvor.ru/ochakovo",
     "image": "https://banniy-dvor.ru/images/tild6163-6234-4563-b964-366332633038__banniy_dvor_preview_.webp",
     "parentOrganization": {"@id": "https://banniy-dvor.ru/#organization"},
     "telephone": "+7-495-795-00-01", "priceRange": "6 000–13 000 ₽/час", "currenciesAccepted": "RUB",
     "address": {"@type": "PostalAddress", "streetAddress": "Очаковское шоссе, 40", "addressLocality": "Москва", "addressCountry": "RU"},
     "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"},
     "amenityFeature": [feat("Парная на дровах в каждом срубе"), feat("Купель в каждом срубе"),
                        feat("Подогреваемый бассейн на улице (7 срубов из 11)"), feat("Своя закрытая охраняемая парковка"),
                        feat("Можно с детьми")],
     "sameAs": ["https://yandex.ru/maps/org/15888089120", "https://2gis.ru/moscow/firm/4504127919528297"],
     "makesOffer": [offer(*x) for x in SRUBS]},
    {"@type": "FAQPage", "@id": "https://banniy-dvor.ru/ochakovo#faq",
     "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Главная", "item": "https://banniy-dvor.ru/"},
        {"@type": "ListItem", "position": 2, "name": "Банный двор Очаково", "item": "https://banniy-dvor.ru/ochakovo"}]},
]
js = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)
open('tilda-snippets/ochakovo-jsonld.html', 'w', encoding='utf-8').write('<script type="application/ld+json">\n' + js + '\n</script>\n')

# ТЗ дизайнеру
TZ = 'tilda-snippets/ochakovo-volna2-tz.md'
tz = open(TZ, encoding='utf-8').read()
tz = re.sub(r'(Текст \(абзац\):\n)> .*\n', lambda m: m.group(1) + '> ' + intro + '\n', tz)
grid = """Те же факты для варианта «сетка с иконками»:
- Очаковское шоссе, 40 · 8 минут пешком от МЦД «Очаково»
- 11 отдельных срубов, только ваша компания
- от 6 до 15 человек
- от 6 000 до 13 000 ₽/час, минимум 3 часа
- в каждом срубе парная на дровах и купель
- в 7 срубах — подогреваемый бассейн на улице
- круглосуточно, без выходных
- своя закрытая охраняемая парковка
- банщики, кухня, повар и официант в срубе
- +7 (495) 795-00-01
"""
tz = re.sub(r'Те же факты для варианта «сетка с иконками»:\n(?:- .*\n)+', grid, tz)
tz = re.sub(r'(## Приложение\. Тексты блока «Частые вопросы» )\(\d+ вопрос\w*\)[\s\S]*$',
            lambda m: m.group(1) + f'({len(faq)} вопросов)\n\n' + '\n\n'.join(f'**{q}**\n{a}' for q, a in faq) + '\n', tz)
tz = re.sub(r'H2\. \d+ вопрос\w*,', f'H2. {len(faq)} вопросов,', tz)
open(TZ, 'w', encoding='utf-8').write(tz)

# Макет в копии (полигон)
P = 'page30467207.html'
s = open(P, encoding='utf-8').read()
CSS = "font-family:'Ubuntu',Arial,sans-serif;color:#1f1f1f;"
intro_html = (f'<div id="rec-mock-intro" class="r t-rec" style="background:#f7f3ee;padding:48px 20px;">\n'
              f'<div style="max-width:960px;margin:0 auto;{CSS}"><p style="font-size:20px;line-height:1.55;margin:0;">{html.escape(intro)}</p></div></div>')
items = ''.join(f'<div style="border-top:1px solid #ddd;padding:18px 0;"><h3 style="font-size:19px;font-weight:600;margin:0 0 8px;">{html.escape(q)}</h3>'
                f'<p style="font-size:17px;line-height:1.55;margin:0;">{html.escape(a)}</p></div>' for q, a in faq)
faq_html = (f'<div id="rec-mock-faq" class="r t-rec" style="background:#fff;padding:56px 20px;">\n'
            f'<div style="max-width:960px;margin:0 auto;{CSS}"><h2 style="font-size:32px;font-weight:600;margin:0 0 24px;">Частые вопросы о Банном дворе в Очаково</h2>{items}</div></div>')
s, n1 = re.subn(r'<div id="rec-mock-intro"[\s\S]*?</p></div></div>', lambda m: intro_html, s, count=1)
s, n2 = re.subn(r'<div id="rec-mock-faq"[\s\S]*?</p></div></div></div>', lambda m: faq_html, s, count=1)
s, n3 = re.subn(r'<script type="application/ld\+json">[\s\S]*?</script>', lambda m: '<script type="application/ld+json">\n' + js + '\n</script>', s, count=1)
assert (n1, n2, n3) == (1, 1, 1), (n1, n2, n3)
open(P, 'w', encoding='utf-8').write(s)
print(f'intro {len(intro)} симв., FAQ {len(faq)} вопросов, офферов {len(SRUBS)}')
