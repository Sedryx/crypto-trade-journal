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
    title: "Vue d'ensemble du journal",
  },
  trades: {
    kicker: "Trades",
    title: "Liste, filtres et lecture des executions",
  },
  sync: {
    kicker: "Synchronisation",
    title: "Pilotage de l'import Bybit",
  },
  stats: {
    kicker: "Statistiques",
    title: "Lecture analytique de la performance",
  },
  settings: {
    kicker: "Configuration",
    title: "Configuration de l'application",
  },
};

let uiInitialized = false;
let dataBootstrapped = false;
let currentDashboardData = null;
let selectedWalletCurrency = "USD";
let autoSyncStarted = false;

function getApi() {
  return window.pywebview?.api || null;
}

function setBanner(title, copy) {
  document.getElementById("app-banner-title").textContent = title;
  document.getElementById("app-banner-copy").textContent = copy;
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
  document.getElementById("trade-count-label").textContent = `${trades.length} trade(s) charge(s)`;

  if (!trades.length) {
    body.innerHTML = `
      <tr>
        <td colspan="7">Aucun trade trouve avec les filtres actuels.</td>
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
        <p class="compact-title">Aucun trade recent</p>
        <p class="compact-copy">La base ne contient pas encore de ligne exploitable.</p>
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
        <p class="compact-title">Stables indisponibles</p>
        <p class="compact-copy">${wallet?.error || "Impossible de lire les stablecoins."}</p>
      </div>
    `;
    container.innerHTML = `
      <div class="compact-item">
        <p class="compact-title">Portefeuille indisponible</p>
        <p class="compact-copy">${wallet?.error || "Impossible de lire le compte Bybit."}</p>
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
        <p class="compact-title">Aucun stable detecte</p>
        <p class="compact-copy">Aucune ligne USDT, USDC ou equivalent n'a ete trouvee.</p>
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
        <p class="compact-title">Aucun autre actif</p>
        <p class="compact-copy">Le portefeuille ne contient pas d'actif hors stablecoin.</p>
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
    ? "Configuration API OK"
    : "API incomplete";
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
      <p class="insight-title">Trades gagnants</p>
      <p class="insight-copy">${stats.winning_trades} trade(s) gagnant(s)</p>
    </article>
    <article class="insight-card">
      <p class="insight-title">Trades perdants</p>
      <p class="insight-copy">${stats.losing_trades} trade(s) perdant(s)</p>
    </article>
    <article class="insight-card">
      <p class="insight-title">Breakeven</p>
      <p class="insight-copy">${stats.breakeven_trades} trade(s) a zero</p>
    </article>
  `;
}

function renderExportSummary(exportData) {
  const container = document.getElementById("export-summary");
  container.innerHTML = `
    <div class="compact-item">
      <p class="compact-title">${exportData.count} trade(s) exporte(s)</p>
      <p class="compact-copy">Fichier cree : ${exportData.path}</p>
      <p class="compact-copy">Genere le ${exportData.generated_at}</p>
    </div>
  `;
}

function renderSyncSummary(syncData) {
  document.getElementById("topbar-last-sync").textContent = `Derniere sync : ${syncData.days} jour(s)`;
  document.getElementById("sync-summary-list").innerHTML = syncData.categories
    .map(
      (category) => `
        <div class="sync-card">
          <span class="sync-category">${category.category}</span>
          <strong>${category.inserted_count} nouvelle(s) execution(s)</strong>
        </div>
      `
    )
    .join("");

  document.getElementById("sync-progress-bar").style.width = "100%";
  document.getElementById("sync-progress-copy").textContent =
    `${syncData.total_inserted} execution(s) inseree(s) sur ${syncData.days} jour(s).`;
}

function updateApiStatus(apiStatus) {
  document.getElementById("sidebar-status-value").textContent = apiStatus.has_credentials
    ? "API configuree"
    : "API incomplete";
  document.getElementById("sidebar-status-copy").textContent = apiStatus.message || "";
  document.getElementById("settings-api-status").textContent = apiStatus.has_credentials
    ? "Configure"
    : "Incomplet";
  document.getElementById("settings-api-status").className = `badge ${
    apiStatus.has_credentials ? "success" : "warning"
  }`;
  document.getElementById("settings-env-path").textContent = apiStatus.env_path || "-";
  document.getElementById("settings-db-path").textContent = apiStatus.db_path || "-";
  document.getElementById("settings-exports-path").textContent = apiStatus.exports_dir || "-";
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
    throw new Error("Bridge PyWebView indisponible. Lance l'application via le shell desktop.");
  }

  const result = await api[methodName](...args);
  if (!result.success) {
    throw new Error(result.error || `Echec de l'appel ${methodName}.`);
  }

  return result.data;
}

async function loadDashboard() {
  const data = await callBridge("get_dashboard");
  renderDashboard(data);
}

async function loadTrades() {
  setBanner("Chargement des trades", "Lecture des trades depuis SQLite...");
  const data = await callBridge("get_trades", readTradeFilters());
  renderTradeRows(data.trades || []);
  setBanner("Trades charges", `${data.count} trade(s) recuperes depuis le backend.`);
}

async function loadStats() {
  const data = await callBridge("get_stats", {});
  renderStats(data);
}

async function refreshApiStatus() {
  const data = await callBridge("get_api_status");
  updateApiStatus(data);
}

async function runSync() {
  const days = parseOptionalInt(document.getElementById("sync-days").value, 7);
  document.getElementById("sync-progress-bar").style.width = "25%";
  document.getElementById("sync-progress-copy").textContent = "Synchronisation en cours...";
  setBanner("Synchronisation Bybit", `Lancement sur ${days} jour(s)...`);

  const data = await callBridge("sync_trades", days);
  renderSyncSummary(data);
  setBanner("Synchronisation terminee", `${data.total_inserted} execution(s) inseree(s).`);
  await Promise.all([loadDashboard(), loadTrades(), loadStats()]);
}

async function saveSettings() {
  const apiKey = document.getElementById("settings-api-key").value;
  const apiSecret = document.getElementById("settings-api-secret").value;

  const data = await callBridge("save_api_config", apiKey, apiSecret);
  setBanner("Configuration enregistree", `Fichier mis a jour : ${data.env_path}`);
  await Promise.all([refreshApiStatus(), loadDashboard()]);
}

async function exportTradesExcel() {
  const data = await callBridge("export_trades_excel", readTradeFilters());
  renderExportSummary(data);
  setBanner("Export Excel termine", `${data.count} trade(s) exporte(s) vers ${data.path}`);
}

async function deleteTrade(tradeId) {
  await callBridge("delete_trade", Number(tradeId));
  setBanner("Trade supprime", `Le trade local ${tradeId} a ete retire de la base.`);
  await Promise.all([loadTrades(), loadDashboard(), loadStats()]);
}

async function seedDevTrades() {
  const data = await callBridge("seed_dev_trades", 20);
  setBanner("Trades de dev ajoutes", `${data.inserted} trade(s) de test insere(s) dans SQLite.`);
  await Promise.all([loadDashboard(), loadTrades(), loadStats()]);
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
    runAction(loadTrades, "Erreur trades");
  });
  document.getElementById("dashboard-open-sync-button").addEventListener("click", () => {
    setActiveView("sync");
  });
  document.getElementById("dashboard-open-settings-button").addEventListener("click", () => {
    setActiveView("settings");
    runAction(refreshApiStatus, "Erreur configuration");
  });
  document.getElementById("trade-table-body").addEventListener("click", (event) => {
    const button = event.target.closest(".row-action-button");
    if (!button) {
      return;
    }
    runAction(() => deleteTrade(button.dataset.tradeId), "Erreur suppression");
  });

  document
    .getElementById("reload-dashboard-button")
    .addEventListener("click", () => runAction(loadDashboard, "Erreur dashboard"));
  document
    .getElementById("load-trades-button")
    .addEventListener("click", () => runAction(loadTrades, "Erreur trades"));
  document
    .getElementById("export-trades-button")
    .addEventListener("click", () => runAction(exportTradesExcel, "Erreur export Excel"));
  document
    .getElementById("reload-stats-button")
    .addEventListener("click", () => runAction(loadStats, "Erreur statistiques"));
  document
    .getElementById("run-sync-button")
    .addEventListener("click", () => runAction(runSync, "Erreur sync"));
  document
    .getElementById("reload-settings-button")
    .addEventListener("click", () => runAction(refreshApiStatus, "Erreur configuration"));
  document
    .getElementById("save-settings-button")
    .addEventListener("click", () => runAction(saveSettings, "Erreur configuration"));
  document
    .getElementById("seed-dev-trades-button")
    .addEventListener("click", () => runAction(seedDevTrades, "Erreur dev test"));
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
  setBanner("Interface prete", "Connexion au backend Python en cours...");
}

async function bootstrapData() {
  if (dataBootstrapped) {
    return;
  }
  dataBootstrapped = true;
  initializeUi();
  setBanner("Initialisation", "Chargement des donnees depuis le backend Python...");

  try {
    const apiStatus = await callBridge("get_api_status");
    updateApiStatus(apiStatus);

    await Promise.all([loadDashboard(), loadTrades(), loadStats()]);
    setBanner("Application prete", "Le dashboard est charge et pret a etre utilise.");

    // Trigger the same sync flow as the manual button shortly after startup.
    if (apiStatus.has_credentials && !autoSyncStarted) {
      autoSyncStarted = true;
      setBanner("Synchronisation planifiee", "La sync automatique va demarrer dans 1 seconde.");
      await delay(1000);
      await runSync();
    }
  } catch (error) {
    setBanner("Initialisation incomplete", error.message);
  }
}

window.addEventListener("DOMContentLoaded", initializeUi);
document.addEventListener("pywebviewready", bootstrapData);
