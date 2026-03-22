/**
 * tools/adb_playwright_scraper.js
 * Scrapes Astro-Databank birth data using Playwright (bypasses Cloudflare JS check).
 *
 * Usage (from ~/LagnaMaster/my-playwright-project):
 *   node ../tools/adb_playwright_scraper.js
 *   node ../tools/adb_playwright_scraper.js --limit 50
 *   node ../tools/adb_playwright_scraper.js --slug "Einstein,_Albert"
 *
 * Output: writes JSON files to ../tests/fixtures/adb_charts/
 */

const { chromium } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

const ADB_BASE = 'https://www.astro.com/astro-databank/';
const FIXTURES_DIR = path.join(__dirname, '../tests/fixtures/adb_charts');
const DELAY_MS = 2000; // polite delay between requests

// ── Full list of 200 persons to scrape ───────────────────────────────────────
const PERSONS = [
  // [slug, name, country, year]
  ["Goethe,_Johann_Wolfgang","Johann Wolfgang Goethe","Germany",1749],
  ["Bach,_Johann_Sebastian","Johann Sebastian Bach","Germany",1685],
  ["Schiller,_Friedrich","Friedrich Schiller","Germany",1759],
  ["Kant,_Immanuel","Immanuel Kant","Germany",1724],
  ["Hegel,_Georg_Wilhelm","Georg Wilhelm Hegel","Germany",1770],
  ["Schopenhauer,_Arthur","Arthur Schopenhauer","Germany",1788],
  ["Wagner,_Richard","Richard Wagner","Germany",1813],
  ["Brahms,_Johannes","Johannes Brahms","Germany",1833],
  ["Kepler,_Johannes","Johannes Kepler","Germany",1571],
  ["Leibniz,_Gottfried","Gottfried Leibniz","Germany",1646],
  ["Bismarck,_Otto_von","Otto von Bismarck","Germany",1815],
  ["Kaiser_Wilhelm_II","Kaiser Wilhelm II","Germany",1859],
  ["Napoleon_III","Napoleon III","France",1808],
  ["de_Gaulle,_Charles","Charles de Gaulle","France",1890],
  ["Hugo,_Victor","Victor Hugo","France",1802],
  ["Descartes,_René","René Descartes","France",1596],
  ["Voltaire","Voltaire","France",1694],
  ["Rousseau,_Jean-Jacques","Jean-Jacques Rousseau","France",1712],
  ["Pascal,_Blaise","Blaise Pascal","France",1623],
  ["Balzac,_Honoré_de","Honoré de Balzac","France",1799],
  ["Flaubert,_Gustave","Gustave Flaubert","France",1821],
  ["Zola,_Émile","Émile Zola","France",1840],
  ["Proust,_Marcel","Marcel Proust","France",1871],
  ["Sartre,_Jean-Paul","Jean-Paul Sartre","France",1905],
  ["Camus,_Albert","Albert Camus","France",1913],
  ["Newton,_Isaac","Isaac Newton","UK",1643],
  ["Dickens,_Charles","Charles Dickens","UK",1812],
  ["Byron,_Lord","Lord Byron","UK",1788],
  ["Shelley,_Percy_Bysshe","Percy Bysshe Shelley","UK",1792],
  ["Keats,_John","John Keats","UK",1795],
  ["Wordsworth,_William","William Wordsworth","UK",1770],
  ["Tennyson,_Alfred","Alfred Tennyson","UK",1809],
  ["Wilde,_Oscar","Oscar Wilde","UK",1854],
  ["Kipling,_Rudyard","Rudyard Kipling","UK",1865],
  ["Shaw,_George_Bernard","George Bernard Shaw","UK",1856],
  ["Wells,_H.G.","H.G. Wells","UK",1866],
  ["Huxley,_Aldous","Aldous Huxley","UK",1894],
  ["Orwell,_George","George Orwell","UK",1903],
  ["Thatcher,_Margaret","Margaret Thatcher","UK",1925],
  ["Charles_III","King Charles III","UK",1948],
  ["Jefferson,_Thomas","Thomas Jefferson","USA",1743],
  ["Roosevelt,_Theodore","Theodore Roosevelt","USA",1858],
  ["Nixon,_Richard","Richard Nixon","USA",1913],
  ["Reagan,_Ronald","Ronald Reagan","USA",1911],
  ["Clinton,_Bill","Bill Clinton","USA",1946],
  ["Bush,_George_W.","George W. Bush","USA",1946],
  ["Trump,_Donald","Donald Trump","USA",1946],
  ["Edison,_Thomas","Thomas Edison","USA",1847],
  ["Ford,_Henry","Henry Ford","USA",1863],
  ["Rockefeller,_John_D.","John D. Rockefeller","USA",1839],
  ["Carnegie,_Andrew","Andrew Carnegie","USA",1835],
  ["Twain,_Mark","Mark Twain","USA",1835],
  ["Hemingway,_Ernest","Ernest Hemingway","USA",1899],
  ["Faulkner,_William","William Faulkner","USA",1897],
  ["Whitman,_Walt","Walt Whitman","USA",1819],
  ["Poe,_Edgar_Allan","Edgar Allan Poe","USA",1809],
  ["King,_Martin_Luther","Martin Luther King","USA",1929],
  ["Malcolm_X","Malcolm X","USA",1925],
  ["Armstrong,_Neil","Neil Armstrong","USA",1930],
  ["Hawking,_Stephen","Stephen Hawking","USA",1942],
  ["Lenin,_Vladimir","Vladimir Lenin","Russia",1870],
  ["Stalin,_Joseph","Joseph Stalin","Russia",1878],
  ["Trotsky,_Leon","Leon Trotsky","Russia",1879],
  ["Tolstoy,_Leo","Leo Tolstoy","Russia",1828],
  ["Dostoevsky,_Fyodor","Fyodor Dostoevsky","Russia",1821],
  ["Chekhov,_Anton","Anton Chekhov","Russia",1860],
  ["Pushkin,_Alexander","Alexander Pushkin","Russia",1799],
  ["Tchaikovsky,_Pyotr","Pyotr Tchaikovsky","Russia",1840],
  ["Gorbachev,_Mikhail","Mikhail Gorbachev","Russia",1931],
  ["Yeltsin,_Boris","Boris Yeltsin","Russia",1931],
  ["Khrushchev,_Nikita","Nikita Khrushchev","Russia",1894],
  ["Mussolini,_Benito","Benito Mussolini","Italy",1883],
  ["Leonardo_da_Vinci","Leonardo da Vinci","Italy",1452],
  ["Michelangelo","Michelangelo","Italy",1475],
  ["Dante","Dante Alighieri","Italy",1265],
  ["Verdi,_Giuseppe","Giuseppe Verdi","Italy",1813],
  ["Puccini,_Giacomo","Giacomo Puccini","Italy",1858],
  ["Fellini,_Federico","Federico Fellini","Italy",1920],
  ["Dali,_Salvador","Salvador Dalí","Spain",1904],
  ["Lorca,_Federico_Garcia","Federico García Lorca","Spain",1898],
  ["Cervantes,_Miguel_de","Miguel de Cervantes","Spain",1547],
  ["Bolivar,_Simon","Simón Bolívar","Venezuela",1783],
  ["Castro,_Fidel","Fidel Castro","Cuba",1926],
  ["Guevara,_Che","Che Guevara","Argentina",1928],
  ["Borges,_Jorge_Luis","Jorge Luis Borges","Argentina",1899],
  ["Neruda,_Pablo","Pablo Neruda","Chile",1904],
  ["Marquez,_Gabriel_Garcia","Gabriel García Márquez","Colombia",1927],
  ["Nkrumah,_Kwame","Kwame Nkrumah","Ghana",1909],
  ["Lumumba,_Patrice","Patrice Lumumba","Congo",1925],
  ["Zhou_Enlai","Zhou Enlai","China",1898],
  ["Deng_Xiaoping","Deng Xiaoping","China",1904],
  ["Sun_Yat-sen","Sun Yat-sen","China",1866],
  ["Hirohito","Emperor Hirohito","Japan",1901],
  ["Khomeini,_Ruhollah","Ayatollah Khomeini","Iran",1902],
  ["Nasser,_Gamal_Abdel","Gamal Abdel Nasser","Egypt",1918],
  ["Sadat,_Anwar","Anwar Sadat","Egypt",1918],
  ["Ben_Gurion,_David","David Ben-Gurion","Israel",1886],
  ["Arafat,_Yasser","Yasser Arafat","Palestine",1929],
  ["Ataturk,_Mustafa_Kemal","Mustafa Kemal Atatürk","Turkey",1881],
  ["Lee_Kuan_Yew","Lee Kuan Yew","Singapore",1923],
  ["Copernicus,_Nicolaus","Nicolaus Copernicus","Poland",1473],
  ["Faraday,_Michael","Michael Faraday","UK",1791],
  ["Maxwell,_James_Clerk","James Clerk Maxwell","UK",1831],
  ["Planck,_Max","Max Planck","Germany",1858],
  ["Heisenberg,_Werner","Werner Heisenberg","Germany",1901],
  ["Schrodinger,_Erwin","Erwin Schrödinger","Austria",1887],
  ["Fermi,_Enrico","Enrico Fermi","Italy",1901],
  ["Oppenheimer,_Robert","Robert Oppenheimer","USA",1904],
  ["Von_Neumann,_John","John von Neumann","Hungary",1903],
  ["Lorentz,_Hendrik","Hendrik Lorentz","Netherlands",1853],
  ["Mendel,_Gregor","Gregor Mendel","Austria",1822],
  ["Rembrandt","Rembrandt van Rijn","Netherlands",1606],
  ["Chopin,_Frédéric","Frédéric Chopin","Poland",1810],
  ["Liszt,_Franz","Franz Liszt","Hungary",1811],
  ["Schubert,_Franz","Franz Schubert","Austria",1797],
  ["Handel,_George_Frideric","George Frideric Handel","Germany",1685],
  ["Haydn,_Joseph","Joseph Haydn","Austria",1732],
  ["Vivaldi,_Antonio","Antonio Vivaldi","Italy",1678],
  ["McCartney,_Paul","Paul McCartney","UK",1942],
  ["Mercury,_Freddie","Freddie Mercury","UK",1946],
  ["Dylan,_Bob","Bob Dylan","USA",1941],
  ["Hendrix,_Jimi","Jimi Hendrix","USA",1942],
  ["Morrison,_Jim","Jim Morrison","USA",1943],
  ["Cobain,_Kurt","Kurt Cobain","USA",1967],
  ["Brando,_Marlon","Marlon Brando","USA",1924],
  ["Dean,_James","James Dean","USA",1931],
  ["Tata,_J.R.D.","J.R.D. Tata","India",1904],
  ["Ambedkar,_B.R.","B.R. Ambedkar","India",1891],
  ["Bose,_Subhas_Chandra","Subhas Chandra Bose","India",1897],
  ["Ramakrishna","Sri Ramakrishna","India",1836],
];

// ── Parse birth data from ADB page HTML ──────────────────────────────────────
function parseBirthData(html, slug, name, country, year) {
  const months = {january:1,february:2,march:3,april:4,may:5,june:6,
                  july:7,august:8,september:9,october:10,november:11,december:12};

  // Date: "14 March 1879" or "March 14, 1879"
  let yr = year, mo = 1, dy = 1;
  let dm = html.match(/(\d{1,2})\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})/i);
  if (dm) { dy=parseInt(dm[1]); mo=months[dm[2].toLowerCase()]; yr=parseInt(dm[3]); }
  else {
    let md = html.match(/(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2}),?\s+(\d{4})/i);
    if (md) { mo=months[md[1].toLowerCase()]; dy=parseInt(md[2]); yr=parseInt(md[3]); }
  }

  // Time
  let hour = 12.0;
  let tm = html.match(/(\d{1,2}):(\d{2})(?::\d{2})?\s*(am|pm|h)?/i);
  if (tm) {
    hour = parseInt(tm[1]) + parseInt(tm[2])/60;
    if (tm[3] && tm[3].toLowerCase()==='pm' && parseInt(tm[1])<12) hour+=12;
    if (tm[3] && tm[3].toLowerCase()==='am' && parseInt(tm[1])===12) hour=parseInt(tm[2])/60;
  }

  // Coordinates
  let lat=0, lon=0;
  let latm = html.match(/(\d+)°(\d+)'([NS])/);
  let lonm = html.match(/(\d+)°(\d+)'([EW])/);
  if (latm) { lat=parseInt(latm[1])+parseInt(latm[2])/60; if(latm[3]==='S') lat=-lat; }
  if (lonm) { lon=parseInt(lonm[1])+parseInt(lonm[2])/60; if(lonm[3]==='W') lon=-lon; }

  // Rodden rating
  let rodden = 'Unknown';
  let rm = html.match(/Rodden[^<]{0,40}?(AA|A|B|C|DD)\b/i) ||
           html.match(/\b(AA)\b.*?[Rr]odden/);
  if (rm) rodden = rm[1].toUpperCase();

  // Timezone
  let tz = lon !== 0 ? Math.round(lon/15*4)/4 : 0;
  const cl = country.toLowerCase();
  if (cl.includes('india') || cl.includes('pakistan')) tz = 5.5;
  else if (cl.includes('germany') || cl.includes('france') || cl.includes('italy') ||
           cl.includes('austria') || cl.includes('switzerland')) tz = 1.0;
  else if (cl.includes('uk') || cl.includes('england')) tz = 0.0;
  else if (cl.includes('russia') && lon > 30) tz = 3.0;

  // Trust level
  const trust = (
    (cl.includes('germany') || cl.includes('france') || cl.includes('switzerland') ||
     cl.includes('denmark') || cl.includes('netherlands') || cl.includes('austria')) && yr >= 1876
  ) ? 'high' :
  (yr >= 1900 && (cl.includes('uk') || cl.includes('usa') || cl.includes('australia'))) ? 'medium' : 'low';

  return { yr, mo, dy, hour, lat, lon, tz, rodden, trust };
}

// ── Main scraper ─────────────────────────────────────────────────────────────
async function scrapeADB(limit = 200, singleSlug = null) {
  fs.mkdirSync(FIXTURES_DIR, { recursive: true });

  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  });
  const page = await context.newPage();

  const toProcess = singleSlug
    ? PERSONS.filter(([s]) => s === singleSlug)
    : PERSONS.slice(0, limit);

  let fetched = 0, skipped = 0, errors = 0;

  for (const [slug, name, country, year] of toProcess) {
    const key = slug.toLowerCase().replace(/[,. ]/g, '_').replace(/__+/g,'_');
    const outPath = path.join(FIXTURES_DIR, `${key}.json`);

    // Check if already has real data
    if (fs.existsSync(outPath)) {
      const existing = JSON.parse(fs.readFileSync(outPath, 'utf8'));
      if (existing.birth_data?.lat !== 0 && existing.fetch_status === 'ok') {
        console.log(`  SKIP (done) ${name}`);
        skipped++;
        continue;
      }
    }

    const url = ADB_BASE + encodeURIComponent(slug).replace(/%2C/g, ',').replace(/%27/g, "'");
    process.stdout.write(`  FETCH [${fetched+1}] ${name}... `);

    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 });

      // Wait for Cloudflare to pass (if triggered)
      await page.waitForFunction(() => !document.title.includes('Just a moment'), { timeout: 10000 }).catch(() => {});
      await page.waitForTimeout(1500);

      const html = await page.content();

      if (html.includes('Enable JavaScript') || html.includes('Just a moment')) {
        console.log(`BLOCKED`);
        errors++;
        continue;
      }

      const d = parseBirthData(html, slug, name, country, year);

      // Read existing fixture or create new
      let fixture = fs.existsSync(outPath) ? JSON.parse(fs.readFileSync(outPath, 'utf8')) : {
        adb_slug: slug, name, source: 'astro-databank',
        adb_url: ADB_BASE + slug,
        expected: {}, chart: null, scores: null,
      };

      fixture.rodden_rating = d.rodden;
      fixture.birth_data = {
        year: d.yr, month: d.mo, day: d.dy, hour: Math.round(d.hour * 100) / 100,
        lat: Math.round(d.lat * 10000) / 10000,
        lon: Math.round(d.lon * 10000) / 10000,
        tz_offset: d.tz, ayanamsha: 'lahiri',
      };
      fixture.birth_place = country;
      fixture.country = country;
      fixture.data_trust_level = d.trust;
      fixture.assert_lagna = (d.trust === 'high');
      fixture.trust_note = `${country} ${d.yr} — ${d.trust} trust`;
      fixture.fetch_status = 'ok';
      fixture.fetched_date = new Date().toISOString().slice(0, 10);

      fs.writeFileSync(outPath, JSON.stringify(fixture, null, 2));
      console.log(`OK (${d.rodden}, ${d.yr}, ${d.lat.toFixed(1)}°, ${d.lon.toFixed(1)}°)`);
      fetched++;

      await page.waitForTimeout(DELAY_MS);

    } catch (e) {
      console.log(`ERROR: ${e.message.slice(0, 60)}`);
      errors++;
    }
  }

  await browser.close();

  console.log(`\nDone: ${fetched} fetched, ${skipped} skipped, ${errors} errors`);
  console.log(`\nNext: cd ~/LagnaMaster && PYTHONPATH=. .venv/bin/python3 tools/scrape_200_aa.py --compute`);
}

// ── CLI ───────────────────────────────────────────────────────────────────────
const args = process.argv.slice(2);
const limitArg = args.find(a => a.startsWith('--limit='));
const slugArg  = args.find(a => a.startsWith('--slug='));
const limit = limitArg ? parseInt(limitArg.split('=')[1]) : 200;
const slug  = slugArg  ? slugArg.split('=').slice(1).join('=') : null;

scrapeADB(limit, slug).catch(e => { console.error(e); process.exit(1); });
