// Портфолио: 6 лучших живых сайтов (Артём 18.11: «не все кейсы, только 4–6»). Всего в бою – liveCount.
// Скрины – assets/raw/works (сняты 18.11.2026, там же запасные: avtoball, starline, tehnics, kitaccess, milovini, rozalii), WebP – scripts/webp.py.
export type Work = { id: string; type: string; name: string; place: string; url: string; note?: string };

export const liveCount = 12;

export const works: Work[] = [
  { id: 'ev', type: 'Сайт сервиса', name: 'EV Service', place: 'Новосибирск', url: 'https://evolutioncarservice.ru/', note: 'свой бизнес' },
  { id: 'teyes', type: 'Сайт и каталог', name: 'TEYES Sibir', place: 'Новосибирск', url: 'https://teyes-sibir.ru/', note: 'свой бизнес' },
  { id: 'evocar', type: 'Каталог авто', name: 'Evolution Car', place: 'Минск', url: 'https://evolutioncar.by/' },
  { id: 'gazmag', type: 'Интернет-магазин', name: 'Газ-маг', place: 'Болотное', url: 'https://gaz-mag.ru/' },
  { id: 'angela', type: 'Лендинг мастера', name: 'Анжела Богатырёва', place: 'Краснодар', url: 'https://permanentbogatyryova.ru/' },
  { id: 'balance', type: 'Сеть клубов', name: 'Balance', place: 'Краснодар', url: 'https://balance-fit.ru/' },
];
