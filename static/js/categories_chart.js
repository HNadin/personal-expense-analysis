(function () {
    const dataElement = document.getElementById('chart-data');
    if (!dataElement) return;

    const chartData = JSON.parse(dataElement.textContent);
    const canvas = document.getElementById('categoriesChart');
    if (!canvas) return;

    const palette = [
        '#0d6efd', '#dc3545', '#198754', '#ffc107', '#6f42c1',
        '#fd7e14', '#20c997', '#d63384', '#0dcaf0', '#6c757d',
    ];

    const colors = chartData.labels.map((_, i) => palette[i % palette.length]);
    const totalSum = chartData.values.reduce((a, b) => a + b, 0);

    new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: chartData.labels,
            datasets: [{
                data: chartData.values,
                backgroundColor: colors,
                borderColor: '#fff',
                borderWidth: 2,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        padding: 12,
                        font: { size: 13 },
                    },
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const value = context.parsed;
                            const percent = totalSum > 0
                                ? ((value / totalSum) * 100).toFixed(1)
                                : 0;
                            return `${context.label}: ${value.toLocaleString('uk-UA')} UAH (${percent}%)`;
                        },
                    },
                },
            },
        },
    });
})();