// Load charts once the page is ready
document.addEventListener("DOMContentLoaded", function() {
    // Get data from Flask (injected into template)
    const categoryLabels = JSON.parse(document.getElementById("category-labels").textContent);
    const categoryValues = JSON.parse(document.getElementById("category-values").textContent);

    // Expense by Category Chart
    const ctx = document.getElementById("expenseChart").getContext("2d");
    new Chart(ctx, {
        type: "pie",
        data: {
            labels: categoryLabels,
            datasets: [{
                data: categoryValues,
                backgroundColor: [
                    "#007bff", "#00c6ff", "#0056b3", "#3399ff", "#80d4ff", "#004080"
                ],
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    position: "bottom",
                    labels: { color: "#333", font: { size: 14 } }
                },
                title: {
                    display: true,
                    text: "Expenses by Category",
                    font: { size: 18 }
                }
            }
        }
    });
});
