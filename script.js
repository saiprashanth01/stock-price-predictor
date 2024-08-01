document.getElementById('predictForm').addEventListener('submit', function(event) {
    var tickerInput = document.getElementById('ticker').value.trim();

    // Form validation: check if ticker input is empty or not valid
    if (!tickerInput) {
        alert('Please enter a valid stock ticker.');
        event.preventDefault();
        return;
    }

    // Display the stock name below the input box
    document.getElementById('stockName').textContent = `Stock: ${tickerInput}`;

    // Show the loading indicator
    document.getElementById('loading').style.display = 'block';
});
