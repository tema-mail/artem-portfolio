// Личный сайт-портфолио Артёма (закатный стиль по рилсу vavoytenko). Стенд: tema-mail.github.io/artem-portfolio/
import { defineConfig } from 'astro/config';
export default defineConfig({
  site: 'https://tema-mail.github.io',
  base: '/artem-portfolio',
  trailingSlash: 'always',
  build: { assets: '_a' },
});
