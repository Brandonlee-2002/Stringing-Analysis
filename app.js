const DATA_URL = "./data/stringing_data.csv";
const CHART_COLORS = ["#176c51", "#d46d56", "#92aa42", "#486c88", "#c69a49", "#6d8878", "#a86a7d", "#7b8c36"];
const PRIVATE_COLUMNS = new Set(["name", "player", "notes"]);
const charts = new Map();
let allRows = [];
let visibleColumns = [];

const byId = (id) => document.getElementById(id);
const cleanText = (value) => value == null ? "" : String(value).trim();

function normalizeHeader(value) {
  const text = cleanText(value).toLowerCase().replace(/[^a-z0-9]/g, "");
  if (text.includes("gender")) return "Gender";
  if (text.includes("racket")) return "Racket";
  if (text.includes("string")) return "String";
  if (text.includes("tension")) return "Tension";
  if (text.includes("date")) return "Date";
  if (text === "nameid" || text === "playerid") return "Player_ID";
  if (text === "name") return "Player";
  if (text === "paid" || text === "pickedup") return cleanText(value);
  if (text === "number") return "Number";
  if (text === "notes") return "Notes";
  return cleanText(value);
}

function normalizeRows(rawRows) {
  const headers = rawRows.length ? rawRows[0].map(normalizeHeader) : [];
  const seen = new Set();
  const uniqueHeaders = headers.map((header, index) => {
    const safeHeader = header || `Field ${index + 1}`;
    if (!seen.has(safeHeader)) {
      seen.add(safeHeader);
      return safeHeader;
    }
    return `${safeHeader}_${index + 1}`;
  });

  return rawRows.slice(1).map((values) => {
    const row = {};
    uniqueHeaders.forEach((header, index) => { row[header] = values[index] ?? ""; });
    row.Tension = row.Tension === "" ? null : Number(row.Tension);
    row.Date = parseDate(row.Date);
    ["Gender", "Racket", "String", "Player_ID"].forEach((key) => { row[key] = cleanText(row[key]); });
    return row;
  }).filter((row) => Object.values(row).some((value) => value !== "" && value != null));
}

function parseDate(value) {
  if (value instanceof Date && !Number.isNaN(value.valueOf())) return value;
  if (typeof value === "number" && window.XLSX) {
    const parsed = XLSX.SSF.parse_date_code(value);
    if (parsed) return new Date(parsed.y, parsed.m - 1, parsed.d);
  }
  if (value == null || value === "") return null;
  const date = new Date(value);
  return Number.isNaN(date.valueOf()) ? null : date;
}

async function loadWorkbook() {
  try {
    if (!window.XLSX || !window.Chart) throw new Error("Dashboard libraries did not load. Check your connection and refresh.");
    const response = await fetch(DATA_URL);
    if (!response.ok) throw new Error(`Could not load the data workbook (${response.status}).`);
    const workbook = XLSX.read(await response.arrayBuffer(), { type: "array", cellDates: true });
    const sheetName = workbook.SheetNames.find((name) => name.toLowerCase() === "string log") || workbook.SheetNames[0];
    if (!sheetName) throw new Error("No worksheet was found in the workbook.");
    const worksheet = workbook.Sheets[sheetName];
    const rawRows = XLSX.utils.sheet_to_json(worksheet, { header: 1, raw: true, defval: "" });
    allRows = normalizeRows(rawRows);
    visibleColumns = rawRows[0].map(normalizeHeader).filter((name, index, list) => name && list.indexOf(name) === index && !PRIVATE_COLUMNS.has(name.toLowerCase()));
    if (!allRows.length) throw new Error("The String Log worksheet has no records.");
    byId("data-status").classList.add("is-ready");
    byId("data-status").innerHTML = '<span class="status-dot"></span> Workbook ready';
    byId("record-count-label").textContent = `${allRows.length.toLocaleString()} records`;
    populateFilters();
    renderDashboard();
  } catch (error) {
    byId("data-status").classList.add("is-error");
    byId("data-status").innerHTML = '<span class="status-dot"></span> Data unavailable';
    byId("empty-state").hidden = false;
    byId("empty-state").textContent = `${error.message} The workbook should be available at data/stringing_data.csv.`;
    byId("record-count-label").textContent = "Unable to load records";
    console.error(error);
  }
}

function populateFilters() {
  [["filter-gender", "Gender"], ["filter-racket", "Racket"], ["filter-string", "String"]].forEach(([id, column]) => {
    const select = byId(id);
    [...new Set(allRows.map((row) => row[column]).filter(Boolean))].sort((a, b) => a.localeCompare(b)).forEach((value) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = value;
      select.append(option);
    });
    select.addEventListener("change", renderDashboard);
  });
  byId("reset-filters").addEventListener("click", () => {
    ["filter-gender", "filter-racket", "filter-string"].forEach((id) => { byId(id).value = ""; });
    renderDashboard();
  });
}

function currentRows() {
  const filters = { Gender: byId("filter-gender").value, Racket: byId("filter-racket").value, String: byId("filter-string").value };
  return allRows.filter((row) => Object.entries(filters).every(([key, value]) => !value || row[key] === value));
}

function countBy(rows, column) {
  const counts = new Map();
  rows.forEach((row) => { if (row[column]) counts.set(row[column], (counts.get(row[column]) || 0) + 1); });
  return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
}

function mean(numbers) { return numbers.length ? numbers.reduce((sum, value) => sum + value, 0) / numbers.length : null; }
function median(numbers) {
  if (!numbers.length) return null;
  const sorted = [...numbers].sort((a, b) => a - b);
  const middle = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[middle] : (sorted[middle - 1] + sorted[middle]) / 2;
}
function quantile(numbers, fraction) {
  const sorted = [...numbers].sort((a, b) => a - b);
  if (!sorted.length) return null;
  const position = (sorted.length - 1) * fraction;
  const lower = Math.floor(position);
  return sorted[lower] + (sorted[Math.ceil(position)] - sorted[lower]) * (position - lower);
}
function mode(rows, column) { return countBy(rows, column)[0]?.[0] || "N/A"; }
function tensionValues(rows) { return rows.map((row) => row.Tension).filter((value) => Number.isFinite(value)); }
function formatNumber(value, digits = 2) { return Number.isFinite(value) ? value.toFixed(digits) : "N/A"; }

function getOutliers(rows) {
  const tensions = tensionValues(rows);
  const low = quantile(tensions, .25);
  const high = quantile(tensions, .75);
  if (low == null || high == null) return { rows: [], low: null, high: null };
  const spread = high - low;
  const lowerBound = low - 1.5 * spread;
  const upperBound = high + 1.5 * spread;
  return { rows: rows.filter((row) => Number.isFinite(row.Tension) && (row.Tension < lowerBound || row.Tension > upperBound)), low: lowerBound, high: upperBound };
}

function destroyChart(id) { charts.get(id)?.destroy(); charts.delete(id); }
function makeChart(id, config) {
  destroyChart(id);
  const canvas = byId(id);
  if (canvas) charts.set(id, new Chart(canvas, config));
}
function baseOptions(extra = {}) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false }, tooltip: { backgroundColor: "#1d2825", padding: 10, titleFont: { family: "DM Sans" }, bodyFont: { family: "DM Sans" } } },
    scales: {
      x: { grid: { display: false }, border: { display: false }, ticks: { color: "#737c76", font: { family: "DM Sans", size: 10 } } },
      y: { beginAtZero: true, grid: { color: "#edf0eb" }, border: { display: false }, ticks: { color: "#737c76", font: { family: "DM Sans", size: 10 }, precision: 0 } },
    },
    ...extra,
  };
}
function barConfig(labels, data, color = "#176c51", horizontal = false) {
  return { type: "bar", data: { labels, datasets: [{ data, backgroundColor: color, borderRadius: 2, maxBarThickness: 25 }] }, options: baseOptions({ indexAxis: horizontal ? "y" : "x" }) };
}
function drawPopular(id, counts) { makeChart(id, barConfig(counts.map(([label]) => label), counts.map(([, count]) => count), "#176c51", true)); }

function renderDashboard() {
  const rows = currentRows();
  byId("empty-state").hidden = rows.length > 0;
  if (!rows.length) {
    byId("empty-state").textContent = "No records match these filters. Adjust a selection or reset the filters.";
    updateMetricText("—", "—", "—", "—");
    destroyAllCharts();
    return;
  }
  const tensions = tensionValues(rows);
  updateMetricText(rows.length.toLocaleString(), tensions.length ? formatNumber(mean(tensions)) : "N/A", mode(rows, "Racket"), mode(rows, "String"));
  byId("metric-tension-delta").textContent = tensions.length ? `median ${formatNumber(median(tensions))}` : "";
  byId("outlier-badge").textContent = getOutliers(rows).rows.length;
  drawPopular("chart-rackets", countBy(rows, "Racket").slice(0, 10));
  drawPopular("chart-strings", countBy(rows, "String").slice(0, 10));
  drawDistribution(tensions);
  drawInsights(rows, tensions);
  drawTrends(rows);
  drawRacketTension(rows);
  drawGenderTension(rows);
  drawGenderRackets(rows);
  drawOutliers(rows);
  renderTable("data-table", rows, visibleColumns, 250);
  byId("table-footer").textContent = `Showing ${Math.min(rows.length, 250).toLocaleString()} of ${rows.length.toLocaleString()} filtered records`;
  byId("download-csv").onclick = () => downloadCsv(rows);
}

function updateMetricText(jobs, tension, racket, string) {
  byId("metric-jobs").textContent = jobs;
  byId("metric-tension").textContent = tension;
  byId("metric-racket").textContent = racket;
  byId("metric-string").textContent = string;
}
function destroyAllCharts() { [...charts.keys()].forEach(destroyChart); }

function drawDistribution(tensions) {
  const bins = 14;
  const min = tensions.length ? Math.floor(Math.min(...tensions)) : 0;
  const max = tensions.length ? Math.ceil(Math.max(...tensions)) : bins;
  const width = Math.max((max - min) / bins, 1);
  const counts = Array.from({ length: bins }, () => 0);
  tensions.forEach((value) => { counts[Math.min(bins - 1, Math.floor((value - min) / width))] += 1; });
  const labels = counts.map((_, index) => `${(min + index * width).toFixed(0)}–${(min + (index + 1) * width).toFixed(0)}`);
  makeChart("chart-distribution", { type: "bar", data: { labels, datasets: [{ data: counts, backgroundColor: "#d7ed65", borderColor: "#92aa42", borderWidth: 1, borderRadius: 2 }] }, options: baseOptions() });
}

function drawInsights(rows, tensions) {
  const cards = [
    ["Median tension", tensions.length ? `${formatNumber(median(tensions))} lbs` : "N/A"],
    ["Gender mix", countBy(rows, "Gender").slice(0, 2).map(([name, count]) => `${name} ${count}`).join(" · ") || "Not recorded"],
    ["Top racket", mode(rows, "Racket")],
    ["Tension spread", tensions.length ? `${formatNumber(Math.min(...tensions), 1)}–${formatNumber(Math.max(...tensions), 1)} lbs` : "N/A"],
  ];
  byId("insights").replaceChildren(...cards.map(([label, value]) => {
    const item = document.createElement("div"); item.className = "insight-item";
    const name = document.createElement("span"); name.textContent = label;
    const result = document.createElement("strong"); result.textContent = value;
    item.append(name, result); return item;
  }));
}

function drawTrends(rows) {
  const monthly = new Map();
  rows.forEach((row) => {
    if (!row.Date || !Number.isFinite(row.Tension)) return;
    const key = `${row.Date.getFullYear()}-${String(row.Date.getMonth() + 1).padStart(2, "0")}`;
    if (!monthly.has(key)) monthly.set(key, []);
    monthly.get(key).push(row.Tension);
  });
  const points = [...monthly.entries()].sort(([a], [b]) => a.localeCompare(b));
  byId("trend-note").textContent = points.length ? `${points.length} months with valid date and tension data.` : "No usable date values were found in the current selection.";
  makeChart("chart-trends", { type: "line", data: { labels: points.map(([key]) => key), datasets: [{ data: points.map(([, values]) => mean(values)), borderColor: "#176c51", backgroundColor: "#d7ed65", pointBackgroundColor: "#d46d56", pointRadius: 3, tension: .25, fill: false }] }, options: baseOptions() });
}

function drawRacketTension(rows) {
  const groups = countBy(rows, "Racket").map(([racket]) => [racket, mean(rows.filter((row) => row.Racket === racket && Number.isFinite(row.Tension)).map((row) => row.Tension))]).filter(([, value]) => Number.isFinite(value)).sort((a, b) => b[1] - a[1]).slice(0, 15);
  makeChart("chart-racket-tension", barConfig(groups.map(([label]) => label), groups.map(([, value]) => Number(value.toFixed(2))), "#d46d56", true));
}

function drawGenderTension(rows) {
  const groups = countBy(rows, "Gender").map(([gender]) => [gender, rows.filter((row) => row.Gender === gender && Number.isFinite(row.Tension)).map((row) => row.Tension)]).filter(([, values]) => values.length);
  const categories = groups.map(([gender]) => gender);
  const data = groups.flatMap(([gender, values]) => values.map((value) => ({ x: gender, y: value })));
  makeChart("chart-gender-tension", { type: "scatter", data: { datasets: [{ data, pointRadius: 3, pointHoverRadius: 5, backgroundColor: "#176c5177" }] }, options: baseOptions({ scales: { x: { type: "category", labels: categories, grid: { display: false }, border: { display: false }, ticks: { color: "#737c76", font: { family: "DM Sans", size: 10 } } }, y: { beginAtZero: false, title: { display: true, text: "Tension (lbs)", color: "#737c76" }, grid: { color: "#edf0eb" }, border: { display: false } } } }) });
}

function drawGenderRackets(rows) {
  const topRackets = countBy(rows, "Racket").slice(0, 8).map(([racket]) => racket);
  const genders = countBy(rows, "Gender").map(([gender]) => gender);
  const datasets = genders.map((gender, index) => ({ label: gender, data: topRackets.map((racket) => rows.filter((row) => row.Gender === gender && row.Racket === racket).length), backgroundColor: CHART_COLORS[index % CHART_COLORS.length], borderRadius: 2, maxBarThickness: 25 }));
  makeChart("chart-gender-rackets", { type: "bar", data: { labels: topRackets, datasets }, options: baseOptions({ indexAxis: "y", plugins: { legend: { display: true, position: "bottom", labels: { boxWidth: 10, color: "#737c76", font: { family: "DM Sans", size: 10 } } } }, scales: { x: { stacked: false, grid: { color: "#edf0eb" }, border: { display: false } }, y: { stacked: false, grid: { display: false }, border: { display: false }, ticks: { color: "#737c76", font: { family: "DM Sans", size: 10 } } } } }) });
}

function drawOutliers(rows) {
  const result = getOutliers(rows);
  byId("outlier-summary").textContent = result.low == null ? "No valid tension measurements are available." : `${result.rows.length} of ${tensionValues(rows).length} measured jobs fall outside ${formatNumber(result.low, 1)}–${formatNumber(result.high, 1)} lbs by the 1.5 × IQR rule.`;
  makeChart("chart-outliers", { type: "scatter", data: { datasets: [{ label: "Typical", data: rows.filter((row) => Number.isFinite(row.Tension) && !result.rows.includes(row)).map((row) => ({ x: "In range", y: row.Tension })), backgroundColor: "#176c5177", pointRadius: 3 }, { label: "Outlier", data: result.rows.map((row) => ({ x: "Flagged", y: row.Tension })), backgroundColor: "#d46d56", pointRadius: 5 }] }, options: baseOptions({ plugins: { legend: { display: true, position: "bottom", labels: { boxWidth: 10, font: { family: "DM Sans", size: 10 } } } }, scales: { x: { type: "category", labels: ["In range", "Flagged"], grid: { display: false }, border: { display: false } }, y: { beginAtZero: false, title: { display: true, text: "Tension (lbs)" }, grid: { color: "#edf0eb" }, border: { display: false } } } }) });
  renderTable("outlier-table", result.rows, visibleColumns, 100);
}

function renderTable(tableId, rows, columns, limit) {
  const table = byId(tableId);
  const shownColumns = columns.filter((column) => rows.some((row) => row[column] !== "" && row[column] != null));
  const head = document.createElement("thead");
  const headerRow = document.createElement("tr");
  shownColumns.forEach((column) => { const cell = document.createElement("th"); cell.textContent = column.replaceAll("_", " "); headerRow.append(cell); });
  head.append(headerRow);
  const body = document.createElement("tbody");
  rows.slice(0, limit).forEach((row) => {
    const tr = document.createElement("tr");
    shownColumns.forEach((column) => {
      const cell = document.createElement("td");
      const value = row[column];
      cell.textContent = value instanceof Date ? value.toLocaleDateString() : value == null ? "" : String(value);
      tr.append(cell);
    });
    body.append(tr);
  });
  table.replaceChildren(head, body);
}

function downloadCsv(rows) {
  const columns = visibleColumns.filter((column) => rows.some((row) => row[column] !== "" && row[column] != null));
  const escape = (value) => `"${String(value ?? "").replaceAll('"', '""')}"`;
  const content = [columns.map(escape).join(","), ...rows.map((row) => columns.map((column) => escape(row[column] instanceof Date ? row[column].toISOString().slice(0, 10) : row[column])).join(","))].join("\r\n");
  const link = document.createElement("a");
  link.href = URL.createObjectURL(new Blob(["\ufeff", content], { type: "text/csv;charset=utf-8" }));
  link.download = "filtered_stringing_data.csv";
  link.click();
  URL.revokeObjectURL(link.href);
}

document.querySelectorAll(".tab").forEach((tab) => tab.addEventListener("click", () => {
  document.querySelectorAll(".tab").forEach((item) => { item.classList.remove("is-active"); item.setAttribute("aria-selected", "false"); });
  document.querySelectorAll(".tab-panel").forEach((panel) => { panel.classList.remove("is-active"); panel.hidden = true; });
  tab.classList.add("is-active");
  tab.setAttribute("aria-selected", "true");
  const panel = byId(tab.getAttribute("aria-controls"));
  panel.hidden = false;
  panel.classList.add("is-active");
  charts.forEach((chart) => chart.resize());
}));

loadWorkbook();