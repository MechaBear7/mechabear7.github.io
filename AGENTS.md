# Personal website maintenance

- Maintain English and Chinese together for all content, layout, navigation, captions, and accessibility changes. English is the default at the root; Chinese lives under `zh/`. Language switches retain the matching page and section.
- Author Chinese HTML in `content/zh/`, English translations in `content/en.json`, and media metadata in `content/media.zh.json`. Run `python3 build_bilingual.py --output .`; missing translations must block generation. Do not edit generated HTML/media catalogs directly.
- CSS, JavaScript, and authentic media are shared. Keep the minimal layout and factual project claims. Preserve source images and videos; keep web videos silent and use short excerpts for GIFs.
- Use the original supplied portrait with a circular CSS crop, 180px desktop and 108px mobile. Do not alter facial appearance or replace it with a generated portrait.
- Preview changes locally first. Do not push or deploy subsequent updates unless the user requests publication.
