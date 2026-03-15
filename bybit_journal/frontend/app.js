// Main desktop frontend controller.
// It handles navigation, bridge calls and rendering of backend data.

const navLinks = document.querySelectorAll(".nav-link");
const views = {
  dashboard: document.getElementById("view-dashboard"),
  trades: document.getElementById("view-trades"),
  sync: document.getElementById("view-sync"),
  stats: document.getElementById("view-stats"),
  settings: document.getElementById("view-settings"),
};

const viewMeta = {
  dashboard: {
    kicker: "Dashboard",
    title: "Overview",
  },
  trades: {
    kicker: "Trades",
    title: "Trades",
  },
  sync: {
    kicker: "Sync",
    title: "Synchronization",
  },
  stats: {
    kicker: "Stats",
    title: "Performance",
  },
  settings: {
    kicker: "Settings",
    title: "Application settings",
  },
};

let uiInitialized = false;
let dataBootstrapped = false;
let currentDashboardData = null;
let selectedWalletCurrency = "USD";
let autoSyncStarted = false;
let selectedTradeId = null;

function getApi() {
  return window.pywebview?.api || null;
}

function setBanner(title, copy) {
  document.getElementById("app-banner-title").textContent = title;
  document.getElementById("app-banner-copy").textContent = copy;
}

function setDevMode(enabled) {
  document.querySelectorAll("[data-dev-only='true']").forEach((element) => {
    element.classList.toggle("is-hidden", !enabled);
  });
}

function setActiveView(viewName) {
  navLinks.forEach((link) => {
    link.classList.toggle("is-active", link.dataset.view === viewName);
  });

  Object.entries(views).forEach(([name, element]) => {
    element.classList.toggle("is-hidden", name !== viewName);
  });

  document.getElementById("view-kicker").textContent = viewMeta[viewName].kicker;
  document.getElementById("view-title").textContent = viewMeta[viewName].title;
}

function formatNumber(value, digits = 2) {
  return Number(value || 0).toFixed(digits);
}

function formatCurrency(value, currency) {
  const number = Number(value || 0);
  return new Intl.NumberFormat("fr-FR", {
    style: "currency",
    currency,
    maximumFractionDigits: currency === "JPY" ? 0 : 2,
  }).format(number);
}

function renderTradeRows(trades) {
  const body = document.getElementById("trade-table-body");
  document.getElementById("trade-count-label").textContent = `${trades.length} trade(s)`;

  if (!trades.length) {
    body.innerHTML = `
      <tr>
        <td colspan="8">No trades found.</td>
      </tr>
    `;
    return;
  }

  body.innerHTML = trades
    .map((trade) => {
      const pnl = Number(trade.pnl || 0);
      return `
        <tr>
          <td>${trade.bybit_trade_id || trade.id || "-"}</td>
          <td>${trade.symbol || "-"}</td>
          <td>${trade.side || "-"}</td>
          <td>${trade.entry_price ?? "-"}</td>
          <td>${trade.qty ?? "-"}</td>
          <td class="trade-pnl ${pnl >= 0 ? "positive" : "negative"}">${formatNumber(pnl)}</td>
          <td>${trade.trade_time || "-"}</td>
          <td>
            <button class="row-action-button" data-trade-id="${trade.id}">Supprimer</button>
          </td>
        </tr>
      `;
    })
    .join("");
}

function renderRecentTrades(trades) {
  const container = document.getElementById("dashboard-recent-trades");
  if (!trades.length) {
    container.innerHTML = `
      <div class="compact-item">
        <p class="compact-title">No recent trades</p>
      </div>
    `;
    return;
  }

  container.innerHTML = trades
    .map((trade) => {
      const pnl = Number(trade.pnl || 0);
      return `
        <div class="compact-item">
          <div>
            <p class="compact-title">${trade.symbol} | ${trade.side}</p>
            <p class="compact-meta">${trade.trade_time || "-"}</p>
          </div>
          <strong class="trade-pnl ${pnl >= 0 ? "positive" : "negative"}">${formatNumber(pnl)}</strong>
        </div>
      `;
    })
    .join("");
}

function convertUsdAmount(value, wallet, currency) {
  const usdValue = Number(value || 0);
  const rates = wallet?.conversion_rates || {};
  const rate = Number(rates[currency] || 0);
  if (!rate) {
    return null;
  }
  return usdValue * rate;
}

function renderWallet(wallet, currency = "USD") {
  const totalEquity = document.getElementById("wallet-total-equity");
  const stableTotal = document.getElementById("wallet-stable-total");
  const stableContainer = document.getElementById("wallet-stable-list");
  const container = document.getElementById("wallet-balance-list");

  if (!wallet || !wallet.success || !wallet.account) {
    totalEquity.textContent = "-";
    stableTotal.textContent = "-";
    stableContainer.innerHTML = `
      <div class="compact-item">
        <p class="compact-title">Unavailable</p>
        <p class="compact-copy">${wallet?.error || "Unable to load stable balances."}</p>
      </div>
    `;
    container.innerHTML = `
      <div class="compact-item">
        <p class="compact-title">Unavailable</p>
        <p class="compact-copy">${wallet?.error || "Unable to load wallet data."}</p>
      </div>
    `;
    return;
  }

  const convertedEquity = convertUsdAmount(wallet.account.total_equity, wallet, currency);
  const convertedStableTotal = convertUsdAmount(wallet.stable_total_usd, wallet, currency);
  const otherBalances = (wallet.non_zero_balances || []).filter((balance) => {
    return !(wallet.stable_balances || []).some((stableBalance) => stableBalance.coin === balance.coin);
  });

  totalEquity.textContent = convertedEquity === null ? "-" : formatCurrency(convertedEquity, currency);
  stableTotal.textContent = convertedStableTotal === null ? "-" : formatCurrency(convertedStableTotal, currency);

  if (!wallet.stable_balances?.length) {
    stableContainer.innerHTML = `
      <div class="compact-item">
        <p class="compact-title">No stable balances</p>
      </div>
    `;
  } else {
    stableContainer.innerHTML = wallet.stable_balances
      .slice(0, 5)
      .map((balance) => {
        const convertedUsdValue = convertUsdAmount(balance.usd_value, wallet, currency);
        return `
          <div class="compact-item">
            <div>
              <p class="compact-title">${balance.coin}</p>
              <p class="compact-meta">Equity: ${balance.equity} | Wallet: ${balance.wallet_balance}</p>
            </div>
            <strong>${convertedUsdValue === null ? "-" : formatCurrency(convertedUsdValue, currency)}</strong>
          </div>
        `;
      })
      .join("");
  }

  if (!otherBalances.length) {
    container.innerHTML = `
      <div class="compact-item">
        <p class="compact-title">No other assets</p>
      </div>
    `;
    return;
  }

  container.innerHTML = otherBalances
    .slice(0, 5)
    .map(
      (balance) => {
        const convertedUsdValue = convertUsdAmount(balance.usd_value, wallet, currency);
        return `
        <div class="compact-item">
          <div>
            <p class="compact-title">${balance.coin}</p>
            <p class="compact-meta">Equity: ${balance.equity} | Wallet: ${balance.wallet_balance}</p>
          </div>
          <strong>${convertedUsdValue === null ? "-" : formatCurrency(convertedUsdValue, currency)}</strong>
        </div>
      `;
      }
    )
    .join("");
}

function renderDashboard(data) {
  currentDashboardData = data;
  const stats = data.stats || {};
  const apiStatus = data.api_status || {};

  document.getElementById("dashboard-api-status").textContent = apiStatus.has_credentials
    ? "Connected"
    : "Missing keys";
  document.getElementById("dashboard-api-copy").textContent = apiStatus.message || "";
  document.getElementById("metric-total-trades").textContent = stats.total_trades ?? 0;
  document.getElementById("metric-total-pnl").textContent = formatNumber(stats.total_pnl);
  document.getElementById("metric-win-rate").textContent = `${formatNumber(stats.win_rate)}%`;
  document.getElementById("metric-recent-count").textContent = data.recent_trade_count ?? 0;

  renderRecentTrades(data.recent_trades || []);
  renderWallet(data.wallet, selectedWalletCurrency);
  updateApiStatus(apiStatus);
}

function renderStats(stats) {
  document.getElementById("stats-best-trade").textContent = formatNumber(stats.best_trade);
  document.getElementById("stats-worst-trade").textContent = formatNumber(stats.worst_trade);
  document.getElementById("stats-average-pnl").textContent = formatNumber(stats.average_pnl);
  document.getElementById("stats-invested").textContent = formatNumber(stats.total_invested_amount);

  document.getElementById("stats-insight-grid").innerHTML = `
    <article class="insight-card">
      <p class="insight-title">Winners</p>
      <p class="insight-copy">${stats.winning_trades} trade(s)</p>
    </article>
    <article class="insight-card">
      <p class="insight-title">Losers</p>
      <p class="insight-copy">${stats.losing_trades} trade(s)</p>
    </article>
    <article class="insight-card">
      <p class="insight-title">Breakeven</p>
      <p class="insight-copy">${stats.breakeven_trades} trade(s)</p>
    </article>
  `;
  renderStatsChart(stats.chart_points || []);
}

function renderStatsChart(points) {
  const container = document.getElementById("stats-chart");
  if (!points.length) {
    container.innerHTML = `
      <div class="compact-item">
        <p class="compact-title">No chart data</p>
      </div>
    `;
    return;
  }

  const width = 760;
  const height = 280;
  const padding = { top: 20, right: 24, bottom: 54, left: 56 };
  const innerWidth = width - padding.left - padding.right;
  const innerHeight = height - padding.top - padding.bottom;

  const values = points.map((point) => Number(point.pnl || 0));
  const rawMin = Math.min(...values);
  const rawMax = Math.max(...values);
  const minValue = Math.min(rawMin, 0);
  const maxValue = Math.max(rawMax, 0);
  const valueRange = maxValue - minValue || 1;
  const stepX = points.length > 1 ? innerWidth / (points.length - 1) : innerWidth / 2;

  const scaleX = (index) => padding.left + (points.length > 1 ? index * stepX : innerWidth / 2);
  const scaleY = (value) => padding.top + ((maxValue - value) / valueRange) * innerHeight;

  const polylinePoints = points
    .map((point, index) => `${scaleX(index)},${scaleY(Number(point.pnl || 0))}`)
    .join(" ");

  const areaPoints = [
    `${scaleX(0)},${scaleY(0)}`,
    ...points.map((point, index) => `${scaleX(index)},${scaleY(Number(point.pnl || 0))}`),
    `${scaleX(points.length - 1)},${scaleY(0)}`,
  ].join(" ");

  const zeroY = scaleY(0);
  const ticks = 5;
  const tickValues = Array.from({ length: ticks }, (_, index) => {
    const ratio = index / (ticks - 1);
    return maxValue - ratio * valueRange;
  });

  container.innerHTML = `
    <svg class="line-chart" viewBox="0 0 ${width} ${height}" role="img" aria-label="Recent trade PnL chart">
      <defs>
        <linearGradient id="chart-area-gradient" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stop-color="rgba(155, 92, 255, 0.28)" />
          <stop offset="100%" stop-color="rgba(155, 92, 255, 0.02)" />
        </linearGradient>
      </defs>

      ${tickValues
        .map((tickValue) => {
          const y = scaleY(tickValue);
          return `
            <line class="chart-grid-line" x1="${padding.left}" y1="${y}" x2="${width - padding.right}" y2="${y}"></line>
            <text class="chart-axis-label chart-axis-label-y" x="${padding.left - 10}" y="${y + 4}">${formatNumber(tickValue, 1)}</text>
          `;
        })
        .join("")}

      <line class="chart-axis" x1="${padding.left}" y1="${padding.top}" x2="${padding.left}" y2="${height - padding.bottom}"></line>
      <line class="chart-axis" x1="${padding.left}" y1="${zeroY}" x2="${width - padding.right}" y2="${zeroY}"></line>

      <polygon class="chart-area" points="${areaPoints}"></polygon>
      <polyline class="chart-line" points="${polylinePoints}"></polyline>

      ${points
        .map((point, index) => {
          const x = scaleX(index);
          const y = scaleY(Number(point.pnl || 0));
          const label = point.label || point.symbol || "-";
          return `
            <circle class="chart-point" cx="${x}" cy="${y}" r="4.5"></circle>
            <text class="chart-point-value" x="${x}" y="${y - 12}">${formatNumber(point.pnl)}</text>
            <text class="chart-axis-label chart-axis-label-x" x="${x}" y="${height - 18}">${label}</text>
          `;
        })
        .join("")}
    </svg>
  `;
}

function renderExportSummary(exportData) {
  const container = document.getElementById("export-summary");
  container.innerHTML = `
    <div class="compact-item">
      <p class="compact-title">${exportData.count} trade(s) exported</p>
      <p class="compact-copy">${exportData.path}</p>
      <p class="compact-copy">${exportData.generated_at}</p>
    </div>
  `;
}

function renderBackupSummary(title, copy) {
  document.getElementById("backup-summary").innerHTML = `
    <div class="compact-item">
      <p class="compact-title">${title}</p>
      <p class="compact-copy">${copy}</p>
    </div>
  `;
}

function renderSyncSummary(syncData) {
  document.getElementById("topbar-last-sync").textContent = `Last sync: ${syncData.days} day(s)`;
  document.getElementById("sync-summary-list").innerHTML = syncData.categories
    .map(
      (category) => `
        <div class="sync-card">
          <span class="sync-category">${category.category}</span>
          <strong>${category.inserted_count} execution(s)</strong>
        </div>
      `
    )
    .join("");

  document.getElementById("sync-progress-bar").style.width = "100%";
  document.getElementById("sync-progress-copy").textContent =
    `${syncData.total_inserted} execution(s) inserted over ${syncData.days} day(s).`;
}

function updateApiStatus(apiStatus) {
  document.getElementById("sidebar-status-value").textContent = apiStatus.has_credentials
    ? "Connected"
    : "Missing keys";
  document.getElementById("sidebar-status-copy").textContent = apiStatus.message || "";
  document.getElementById("settings-api-status").textContent = apiStatus.has_credentials
    ? "Ready"
    : "Missing";
  document.getElementById("settings-api-status").className = `badge ${
    apiStatus.has_credentials ? "success" : "warning"
  }`;
  document.getElementById("settings-env-path").textContent = apiStatus.env_path || "-";
  document.getElementById("settings-db-path").textContent = apiStatus.db_path || "-";
  document.getElementById("settings-exports-path").textContent = apiStatus.exports_dir || "-";
  setDevMode(Boolean(apiStatus.dev_mode));
  populateSyncSettings(apiStatus.settings || {});
}

function populateSyncSettings(settings) {
  const defaultDays = settings.default_sync_days ?? 7;
  document.getElementById("sync-days").value = defaultDays;
  document.getElementById("settings-default-sync-days").value = defaultDays;
  document.getElementById("settings-auto-sync").checked = Boolean(settings.auto_sync_on_startup);
}

function normalizeDateInput(value, endOfDay = false) {
  const cleaned = value.trim();
  if (!cleaned) {
    return null;
  }
  if (cleaned.length === 10) {
    return `${cleaned} ${endOfDay ? "23:59:59" : "00:00:00"}`;
  }
  return cleaned;
}

function parseOptionalFloat(value) {
  const cleaned = value.trim();
  if (!cleaned) {
    return null;
  }
  const parsed = Number(cleaned);
  return Number.isNaN(parsed) ? null : parsed;
}

function parseOptionalInt(value, fallback = null) {
  const cleaned = value.trim();
  if (!cleaned) {
    return fallback;
  }
  const parsed = Number.parseInt(cleaned, 10);
  return Number.isNaN(parsed) ? fallback : parsed;
}

function readTradeFilters() {
  return {
    symbol: document.getElementById("filter-symbol").value.trim().toUpperCase() || null,
    side: document.getElementById("filter-side").value.trim() || null,
    start_time: normalizeDateInput(document.getElementById("filter-start").value),
    end_time: normalizeDateInput(document.getElementById("filter-end").value, true),
    min_pnl: parseOptionalFloat(document.getElementById("filter-min-pnl").value),
    limit: parseOptionalInt(document.getElementById("filter-limit").value, 50),
  };
}

async function callBridge(methodName, ...args) {
  // All Python calls go through the PyWebView bridge and share the same envelope.
  const api = getApi();
  if (!api || typeof api[methodName] !== "function") {
    throw new Error("Desktop bridge unavailable.");
  }

  const result = await api[methodName](...args);
  if (!result.success) {
    throw new Error(result.error || `Call failed: ${methodName}`);
  }

  return result.data;
}

async function loadDashboard() {
  const data = await callBridge("get_dashboard");
  renderDashboard(data);
}

async function loadTrades() {
  setBanner("Loading trades", "Reading SQLite data...");
  const data = await callBridge("get_trades", readTradeFilters());
  renderTradeRows(data.trades || []);
  setBanner("Trades loaded", `${data.count} trade(s) found.`);
}

async function loadTradeDetail(tradeId) {
  selectedTradeId = Number(tradeId);
  const trade = await callBridge("get_trade_detail", selectedTradeId);
  renderTradeDetail(trade);
}

function renderTradeDetail(trade) {
  document.getElementById("trade-detail-id").textContent = trade.bybit_trade_id || `#${trade.id}`;
  document.getElementById("trade-note-input").value = trade.note || "";
  document.getElementById("trade-screenshot-input").value = trade.screenshot_path || "";
  document.getElementById("trade-detail-fields").innerHTML = `
    <div class="setting-row"><span>Symbol</span><strong class="badge neutral">${trade.symbol || "-"}</strong></div>
    <div class="setting-row"><span>Side</span><strong class="badge neutral">${trade.side || "-"}</strong></div>
    <div class="setting-row"><span>Qty</span><strong class="badge neutral">${trade.qty ?? "-"}</strong></div>
    <div class="setting-row"><span>Entry</span><strong class="badge neutral">${trade.entry_price ?? "-"}</strong></div>
    <div class="setting-row"><span>Exit</span><strong class="badge neutral">${trade.exit_price ?? "-"}</strong></div>
    <div class="setting-row"><span>PnL</span><strong class="badge ${Number(trade.pnl || 0) >= 0 ? "success" : "warning"}">${formatNumber(trade.pnl)}</strong></div>
    <div class="setting-row"><span>Leverage</span><strong class="badge neutral">${trade.leverage ?? "-"}</strong></div>
    <div class="setting-row"><span>Time</span><strong class="badge neutral">${trade.trade_time || "-"}</strong></div>
  `;
}

async function loadStats() {
  const data = await callBridge("get_stats", {});
  renderStats(data);
}

async function refreshApiStatus() {
  const data = await callBridge("get_api_status");
  updateApiStatus(data);
}

async function loadSyncSettings() {
  const data = await callBridge("get_sync_settings");
  populateSyncSettings(data);
}

async function runSync() {
  const days = parseOptionalInt(document.getElementById("sync-days").value, 7);
  document.getElementById("sync-progress-bar").style.width = "25%";
  document.getElementById("sync-progress-copy").textContent = "Sync running...";
  setBanner("Bybit sync", `Running ${days}-day sync...`);

  const data = await callBridge("sync_trades", days);
  renderSyncSummary(data);
  setBanner("Sync completed", `${data.total_inserted} execution(s) inserted.`);
  await Promise.all([loadDashboard(), loadTrades(), loadStats()]);
}

async function saveSettings() {
  const apiKey = document.getElementById("settings-api-key").value;
  const apiSecret = document.getElementById("settings-api-secret").value;

  const data = await callBridge("save_api_config", apiKey, apiSecret);
  setBanner("Settings saved", data.env_path);
  await Promise.all([refreshApiStatus(), loadDashboard()]);
}

async function saveSyncSettings() {
  const autoSyncOnStartup = document.getElementById("settings-auto-sync").checked;
  const defaultSyncDays = parseOptionalInt(document.getElementById("settings-default-sync-days").value, 7);
  const data = await callBridge("save_sync_settings", autoSyncOnStartup, defaultSyncDays);
  populateSyncSettings(data);
  setBanner("Sync settings saved", `${data.default_sync_days} day(s), auto-sync ${data.auto_sync_on_startup ? "on" : "off"}.`);
}

async function exportTradesExcel() {
  const data = await callBridge("export_trades_excel", readTradeFilters());
  renderExportSummary(data);
  setBanner("Excel export", `${data.count} trade(s) exported.`);
}

async function deleteTrade(tradeId) {
  if (!window.confirm(`Delete trade #${tradeId}?`)) {
    return;
  }
  await callBridge("delete_trade", Number(tradeId));
  setBanner("Trade deleted", `Trade #${tradeId} removed.`);
  await Promise.all([loadTrades(), loadDashboard(), loadStats()]);
  if (selectedTradeId === Number(tradeId)) {
    selectedTradeId = null;
    document.getElementById("trade-detail-id").textContent = "No trade selected";
    document.getElementById("trade-detail-fields").innerHTML = `
      <div class="setting-row">
        <span>Status</span>
        <strong class="badge neutral">Select a trade</strong>
      </div>
    `;
    document.getElementById("trade-note-input").value = "";
    document.getElementById("trade-screenshot-input").value = "";
  }
}

async function seedDevTrades() {
  const data = await callBridge("seed_dev_trades", 20);
  setBanner("Dev trades added", `${data.inserted} test trade(s) inserted.`);
  await Promise.all([loadDashboard(), loadTrades(), loadStats()]);
}

async function openFolder(target) {
  const data = await callBridge("open_folder", target);
  setBanner("Folder opened", data.path);
}

async function saveTradeJournal() {
  if (!selectedTradeId) {
    throw new Error("Select a trade first.");
  }
  const note = document.getElementById("trade-note-input").value;
  const screenshotPath = document.getElementById("trade-screenshot-input").value;
  const data = await callBridge("save_trade_journal", selectedTradeId, note, screenshotPath);
  renderTradeDetail(data.trade);
  await Promise.all([loadTrades(), loadDashboard()]);
  setBanner("Trade updated", `Trade #${selectedTradeId} journal saved.`);
}

async function createBackup() {
  const data = await callBridge("create_backup");
  renderBackupSummary("Backup created", data.path);
  setBanner("Backup created", data.filename);
}

async function restoreBackup() {
  const backupPath = document.getElementById("restore-backup-path").value.trim();
  if (!backupPath) {
    throw new Error("Enter a backup path.");
  }
  if (!window.confirm("Restore database from this backup? This will replace the current local database.")) {
    return;
  }
  const data = await callBridge("restore_backup", backupPath);
  renderBackupSummary("Backup restored", data.path);
  await Promise.all([loadDashboard(), loadTrades(), loadStats(), refreshApiStatus()]);
  setBanner("Backup restored", data.path);
}

async function runAction(action, title) {
  try {
    await action();
  } catch (error) {
    setBanner(title, error.message);
  }
}

function bindEvents() {
  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      setActiveView(link.dataset.view);
    });
  });

  document.getElementById("dashboard-open-trades-button").addEventListener("click", () => {
    setActiveView("trades");
    runAction(loadTrades, "Trades error");
  });
  document.getElementById("dashboard-open-sync-button").addEventListener("click", () => {
    setActiveView("sync");
  });
  document.getElementById("dashboard-open-settings-button").addEventListener("click", () => {
    setActiveView("settings");
    runAction(refreshApiStatus, "Settings error");
  });
  document.getElementById("trade-table-body").addEventListener("click", (event) => {
    const button = event.target.closest(".row-action-button");
    if (button) {
      runAction(() => deleteTrade(button.dataset.tradeId), "Delete error");
      return;
    }
    const row = event.target.closest("tr");
    if (!row) {
      return;
    }
    const trigger = row.querySelector(".row-action-button");
    if (!trigger) {
      return;
    }
    runAction(() => loadTradeDetail(trigger.dataset.tradeId), "Trade detail error");
  });

  document
    .getElementById("reload-dashboard-button")
    .addEventListener("click", () => runAction(loadDashboard, "Dashboard error"));
  document
    .getElementById("load-trades-button")
    .addEventListener("click", () => runAction(loadTrades, "Trades error"));
  document
    .getElementById("export-trades-button")
    .addEventListener("click", () => runAction(exportTradesExcel, "Excel export error"));
  document
    .getElementById("reload-stats-button")
    .addEventListener("click", () => runAction(loadStats, "Stats error"));
  document
    .getElementById("run-sync-button")
    .addEventListener("click", () => runAction(runSync, "Sync error"));
  document
    .getElementById("reload-settings-button")
    .addEventListener("click", () => runAction(refreshApiStatus, "Settings error"));
  document
    .getElementById("save-settings-button")
    .addEventListener("click", () => runAction(saveSettings, "Settings error"));
  document
    .getElementById("seed-dev-trades-button")
    .addEventListener("click", () => runAction(seedDevTrades, "Dev tools error"));
  document
    .getElementById("save-trade-journal-button")
    .addEventListener("click", () => runAction(saveTradeJournal, "Trade update error"));
  document
    .getElementById("open-config-folder-button")
    .addEventListener("click", () => runAction(() => openFolder("config"), "Folder error"));
  document
    .getElementById("open-data-folder-button")
    .addEventListener("click", () => runAction(() => openFolder("data"), "Folder error"));
  document
    .getElementById("open-exports-folder-button")
    .addEventListener("click", () => runAction(() => openFolder("exports"), "Folder error"));
  document
    .getElementById("open-backups-folder-button")
    .addEventListener("click", () => runAction(() => openFolder("backups"), "Folder error"));
  document
    .getElementById("save-sync-settings-button")
    .addEventListener("click", () => runAction(saveSyncSettings, "Sync settings error"));
  document
    .getElementById("create-backup-button")
    .addEventListener("click", () => runAction(createBackup, "Backup error"));
  document
    .getElementById("restore-backup-button")
    .addEventListener("click", () => runAction(restoreBackup, "Restore error"));
  document.getElementById("wallet-currency-select").addEventListener("change", (event) => {
    selectedWalletCurrency = event.target.value;
    if (currentDashboardData?.wallet) {
      renderWallet(currentDashboardData.wallet, selectedWalletCurrency);
    }
  });
}

function delay(ms) {
  return new Promise((resolve) => window.setTimeout(resolve, ms));
}

function initializeUi() {
  if (uiInitialized) {
    return;
  }
  uiInitialized = true;
  bindEvents();
  setActiveView("dashboard");
  setBanner("Interface ready", "Connecting to Python backend...");
}

async function bootstrapData() {
  if (dataBootstrapped) {
    return;
  }
  dataBootstrapped = true;
  initializeUi();
  setBanner("Initializing", "Loading backend data...");

  try {
    const apiStatus = await callBridge("get_api_status");
    updateApiStatus(apiStatus);

    await Promise.all([loadDashboard(), loadTrades(), loadStats(), loadSyncSettings()]);
    setBanner("Ready", "Dashboard loaded.");

    // Trigger the same sync flow as the manual button shortly after startup.
    if (apiStatus.has_credentials && apiStatus.settings?.auto_sync_on_startup && !autoSyncStarted) {
      autoSyncStarted = true;
      setBanner("Auto sync", "Starting in 1 second...");
      await delay(1000);
      await runSync();
    }
  } catch (error) {
    setBanner("Initialization error", error.message);
  }
}

window.addEventListener("DOMContentLoaded", initializeUi);
document.addEventListener("pywebviewready", bootstrapData);
