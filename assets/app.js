const API_BASE = './predictions';

async function loadTicker(ticker) {
  try {
    const response = await fetch(`${API_BASE}/${ticker}.json`);
    if (!response.ok) throw new Error(`No  ${response.status}`);
    const data = await response.json();
    
    document.getElementById('rawjson').textContent = JSON.stringify(data, null, 2);
    
    // Update summary
    const summary = document.getElementById('summary');
    const signal = data.signal === 'BUY' ? '📈 BUY' : data.signal === 'SELL' ? '📉 SELL' : '➡️ HOLD';
    summary.innerHTML = `
      <h2>${data.ticker}</h2>
      <p><strong>Prediction:</strong> ₹${data.predicted_price} 
         <span class="signal ${data.signal.toLowerCase()}">${signal}</span></p>
      <p><strong>Last Close:</strong> ₹${data.last_close} | 
         <strong>RMSE:</strong> ₹${data.rmse || 'N/A'}</p>
    `;
    
    // Chart
    const ctx = document.getElementById('priceChart').getContext('2d');
    if (window.priceChart) window.priceChart.destroy();
    
    window.priceChart = new Chart(ctx, {
      type: 'line',
       {
        labels: data.recent_history.map(h => h.date),
        datasets: [{
          label: 'Close Price (₹)',
           data.recent_history.map(h => h.close),
          borderColor: '#1e90ff',
          backgroundColor: 'rgba(30, 144, 255, 0.1)',
          tension: 0.4,
          fill: true
        }]
      },
      options: {
        responsive: true,
        scales: { y: { beginAtZero: false } }
      }
    });
    
  } catch (e) {
    document.getElementById('rawjson').textContent = `Error: ${e.message}`;
    document.getElementById('summary').innerHTML = `<p>Error loading ${ticker}</p>`;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const select = document.getElementById('ticker-select');
  const loadBtn = document.getElementById('load-btn');
  const refreshBtn = document.getElementById('refresh-btn');
  
  // HARDCODE tickers
  const tickers = ['RELIANCE.NS'];
  tickers.forEach(ticker => {
    const option = document.createElement('option');
    option.value = ticker;
    option.textContent = ticker;
    select.appendChild(option);
  });
  
  loadBtn.onclick = () => loadTicker(select.value);
  refreshBtn.onclick = () => loadTicker(select.value);
  
  // AUTO LOAD RELIANCE
  loadTicker('RELIANCE.NS');
});
