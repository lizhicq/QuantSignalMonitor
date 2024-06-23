function updateClock() {
    const now = new Date();
    const timeString = now.toTimeString().split(" ")[0];
    document.getElementById("clock").textContent = timeString;
}

function fetchData() {
    fetch("/leaderboard")
        .then(response => response.json())
        .then(data => {
            console.log('fetchData called', data); // Additional log for debugging
            updateLeaderboard(data);
            document.getElementById("lastUpdate").textContent = "Last updated at " + new Date().toTimeString().split(" ")[0];
        })
        .catch(error => {
            console.error("Error fetching data:", error);
            document.getElementById('data-tables').innerHTML = `<p>Error loading data: ${error.message}</p>`;
        });
}

function updateLeaderboard(data) {
    let html = '';
    Object.entries(data).forEach(([window, stocks]) => {
        html += `<h2>Top 10 for ${window} Minutes</h2>
                 <table class="table table-striped">
                 <thead>
                     <tr>
                         <th>Stock ID</th>
                         <th>Stock Name</th>
                         <th>Total Amount</th>
                         <th>Price Increase</th>
                         <th>Interval Price Increase</th>
                         <th>Statistical Interval</th>
                         <th>Price Surge</th>
                     </tr>
                 </thead>
                 <tbody>`;
        stocks.forEach(stock => {
            html += `<tr>
                         <td>${stock.StockId}</td>
                         <td>${stock.StockName}</td>
                         <td>${stock.TotalAmount}</td>
                         <td>${stock.PriceIncrease}</td>
                         <td>${stock.IntervalPriceIncrease}</td>
                         <td>${stock.StatisticalInterval}</td>
                         <td>${stock.PriceSurge}</td>
                     </tr>`;
        });
        html += '</tbody></table>';
    });
    document.getElementById('data-tables').innerHTML = html;
}

document.addEventListener('DOMContentLoaded', function() {
    updateClock();
    setInterval(updateClock, 1000);
    fetchData();
    setInterval(fetchData, 60000); // Call fetchData every minute
});
