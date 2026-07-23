'use strict';

// --- Rate data -------------------------------------------------------------

const RATES_URL = 'https://open.er-api.com/v6/latest/USD';
const STORAGE_KEY = 'alter-rates-v1';
const PREFS_KEY = 'alter-prefs-v1';
const MAX_FRESH_AGE_MS = 60 * 60 * 1000; // refresh if older than 1 hour

// Bundled snapshot so the app works even if it has never been online.
const FALLBACK_RATES = {
  base: 'USD',
  timestamp: Date.parse('2026-01-15T00:00:00Z'),
  fallback: true,
  rates: {
    USD: 1, EUR: 0.92, GBP: 0.79, JPY: 155, CNY: 7.25, INR: 84, AUD: 1.52,
    CAD: 1.37, CHF: 0.88, HKD: 7.8, SGD: 1.34, KRW: 1380, MXN: 18.5,
    BRL: 5.5, ZAR: 18.2, SEK: 10.5, NOK: 10.8, DKK: 6.9, PLN: 4.0,
    TRY: 34, RUB: 95, IDR: 15800, MYR: 4.4, THB: 34.5, PHP: 57,
    VND: 25000, AED: 3.6725, SAR: 3.75, ILS: 3.7, EGP: 48, NGN: 1550,
    KES: 129, ARS: 1000, CLP: 950, COP: 4100, PKR: 278, BDT: 118,
    NZD: 1.65, TWD: 32, CZK: 23, HUF: 360, RON: 4.6, UAH: 41,
    QAR: 3.64, KWD: 0.31
  }
};

const CURRENCY_NAMES = {
  USD: 'US Dollar', EUR: 'Euro', GBP: 'British Pound', JPY: 'Japanese Yen',
  CNY: 'Chinese Yuan', INR: 'Indian Rupee', AUD: 'Australian Dollar',
  CAD: 'Canadian Dollar', CHF: 'Swiss Franc', HKD: 'Hong Kong Dollar',
  SGD: 'Singapore Dollar', KRW: 'South Korean Won', MXN: 'Mexican Peso',
  BRL: 'Brazilian Real', ZAR: 'South African Rand', SEK: 'Swedish Krona',
  NOK: 'Norwegian Krone', DKK: 'Danish Krone', PLN: 'Polish Zloty',
  TRY: 'Turkish Lira', RUB: 'Russian Ruble', IDR: 'Indonesian Rupiah',
  MYR: 'Malaysian Ringgit', THB: 'Thai Baht', PHP: 'Philippine Peso',
  VND: 'Vietnamese Dong', AED: 'UAE Dirham', SAR: 'Saudi Riyal',
  ILS: 'Israeli Shekel', EGP: 'Egyptian Pound', NGN: 'Nigerian Naira',
  KES: 'Kenyan Shilling', ARS: 'Argentine Peso', CLP: 'Chilean Peso',
  COP: 'Colombian Peso', PKR: 'Pakistani Rupee', BDT: 'Bangladeshi Taka',
  NZD: 'New Zealand Dollar', TWD: 'New Taiwan Dollar', CZK: 'Czech Koruna',
  HUF: 'Hungarian Forint', RON: 'Romanian Leu', UAH: 'Ukrainian Hryvnia',
  QAR: 'Qatari Riyal', KWD: 'Kuwaiti Dinar'
};

let current = loadStoredRates() || FALLBACK_RATES;

function loadStoredRates() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const data = JSON.parse(raw);
    if (data && data.rates && data.timestamp) return data;
  } catch (err) { /* corrupted storage — fall back */ }
  return null;
}

async function refreshRates() {
  if (!navigator.onLine) return false;
  try {
    const res = await fetch(RATES_URL, { cache: 'no-store' });
    if (!res.ok) return false;
    const body = await res.json();
    if (body.result !== 'success' || !body.rates) return false;
    current = {
      base: body.base_code || 'USD',
      timestamp: Date.now(),
      rates: body.rates
    };
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(current));
    } catch (err) { /* storage full — keep in-memory rates */ }
    populateCurrencies();
    render();
    return true;
  } catch (err) {
    return false;
  }
}

function convert(amount, from, to) {
  const r = current.rates;
  if (!(from in r) || !(to in r)) return null;
  return amount * (r[to] / r[from]);
}

// --- UI --------------------------------------------------------------------

const amountEl = document.getElementById('amount');
const fromEl = document.getElementById('from-currency');
const toEl = document.getElementById('to-currency');
const resultEl = document.getElementById('result');
const unitRateEl = document.getElementById('unit-rate');
const badgeEl = document.getElementById('connection-badge');
const ageEl = document.getElementById('rates-age');

function populateCurrencies() {
  const codes = Object.keys(current.rates).sort();
  const prefs = loadPrefs();
  const prevFrom = fromEl.value || prefs.from || 'USD';
  const prevTo = toEl.value || prefs.to || 'EUR';
  for (const sel of [fromEl, toEl]) {
    sel.innerHTML = '';
    for (const code of codes) {
      const opt = document.createElement('option');
      opt.value = code;
      const name = CURRENCY_NAMES[code];
      opt.textContent = name ? `${code} — ${name}` : code;
      sel.appendChild(opt);
    }
  }
  fromEl.value = codes.includes(prevFrom) ? prevFrom : 'USD';
  toEl.value = codes.includes(prevTo) ? prevTo : codes.find(c => c !== fromEl.value);
}

function loadPrefs() {
  try {
    return JSON.parse(localStorage.getItem(PREFS_KEY)) || {};
  } catch (err) {
    return {};
  }
}

function savePrefs() {
  try {
    localStorage.setItem(PREFS_KEY, JSON.stringify({ from: fromEl.value, to: toEl.value }));
  } catch (err) { /* non-essential */ }
}

function formatMoney(value, code) {
  try {
    return new Intl.NumberFormat(undefined, {
      style: 'currency',
      currency: code,
      maximumFractionDigits: value < 1 ? 6 : 2
    }).format(value);
  } catch (err) {
    return `${value.toFixed(2)} ${code}`;
  }
}

function render() {
  const amount = parseFloat(amountEl.value);
  const from = fromEl.value;
  const to = toEl.value;
  if (!Number.isFinite(amount) || !from || !to) {
    resultEl.textContent = '—';
    unitRateEl.textContent = '';
    return;
  }
  const value = convert(amount, from, to);
  if (value === null) {
    resultEl.textContent = '—';
    unitRateEl.textContent = '';
    return;
  }
  resultEl.textContent = formatMoney(value, to);
  const unit = convert(1, from, to);
  unitRateEl.textContent = `1 ${from} = ${unit.toLocaleString(undefined, { maximumSignificantDigits: 6 })} ${to}`;
  renderAge();
}

function renderAge() {
  const when = new Date(current.timestamp);
  const label = current.fallback ? 'bundled rates from' : 'rates updated';
  ageEl.textContent = `${label} ${when.toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' })}`;
}

function renderConnection() {
  const online = navigator.onLine;
  badgeEl.textContent = online ? 'online' : 'offline';
  badgeEl.classList.toggle('online', online);
  badgeEl.classList.toggle('offline', !online);
}

// --- Events ----------------------------------------------------------------

amountEl.addEventListener('input', render);
fromEl.addEventListener('change', () => { savePrefs(); render(); });
toEl.addEventListener('change', () => { savePrefs(); render(); });

document.getElementById('swap').addEventListener('click', () => {
  const from = fromEl.value;
  fromEl.value = toEl.value;
  toEl.value = from;
  savePrefs();
  render();
});

window.addEventListener('online', () => {
  renderConnection();
  refreshRates();
});
window.addEventListener('offline', renderConnection);

// --- Boot ------------------------------------------------------------------

populateCurrencies();
renderConnection();
render();

// Update rates in the background if they are stale.
if (Date.now() - current.timestamp > MAX_FRESH_AGE_MS) {
  refreshRates();
}

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('sw.js').catch(() => { /* offline first load */ });
}
