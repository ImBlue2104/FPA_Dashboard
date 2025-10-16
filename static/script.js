const labels = JSON.parse(document.getElementById("category-labels").textContent);
const data = JSON.parse(document.getElementById("category-values").textContent);

const ctx = document.getElementById('expenseChart').getContext('2d');

new Chart(ctx, {
    type: 'pie',
    data: {
        labels: labels,
        datasets: [{
            label: 'Expenses',
            data: data,
            backgroundColor: [
                '#42a5f5',
                '#66bb6a',
                '#ffa726',
                '#ef5350',
                '#ab47bc'
            ]
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'bottom'
            }
        }
    }
});
