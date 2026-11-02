# Helei Yang · 杨贺磊

[Personal website / 个人主页](https://mechabear7.github.io/) · [中文](https://mechabear7.github.io/zh/index.html)

Projects, experience, publications, competitions, patents, and academic service. English is the default; every page has a matching Chinese version.

## Maintain both languages

- Chinese templates: `content/zh/`
- English translations: `content/en.json`
- Media metadata: `content/media.zh.json`
- Shared presentation: `styles.css`, `app.js`, and `assets/`

After editing, regenerate both languages:

```sh
python3 build_bilingual.py --output .
```

The build stops if an English translation is missing. Do not edit generated HTML or media catalogs directly. Preview locally before publishing; push only when publication is requested. GitHub Pages publishes the `main` branch root, with `.nojekyll` and no framework dependencies.
