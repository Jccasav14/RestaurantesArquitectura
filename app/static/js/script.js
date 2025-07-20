// Gráficos de estadísticas
document.addEventListener('DOMContentLoaded', function() {
    // Si existe el gráfico de restaurantes, inicializa los gráficos
    if (document.getElementById('frequentRestaurantsChart')) {
        initCharts();
    }
    
    // Manejo del dropdown del perfil de usuario
    const userProfile = document.getElementById('userProfile');
    if (userProfile) {
        userProfile.addEventListener('click', function(e) {
            e.stopPropagation();
            document.querySelector('.user-dropdown').classList.toggle('show');
        });
        
        // Cierra el dropdown al hacer clic fuera
        document.addEventListener('click', function() {
            document.querySelector('.user-dropdown').classList.remove('show');
        });
    }
});

// Variables globales para gráficos
let restaurantChart;
const chartColors = ['#4e73df', '#1cc88a', '#36b9cc', '#f6c23e', '#e74a3b', '#5a5c69', '#858796', '#6f42c1', '#fd7e14', '#20c997'];

// Inicializa ambos gráficos si existen
function initCharts() {
    // Gráfico de barras: restaurantes más visitados
    const ctx = document.getElementById('frequentRestaurantsChart').getContext('2d');
    restaurantChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: JSON.parse(document.getElementById('frequentRestaurantsChart').dataset.labels),
            datasets: [{
                label: 'Visitas',
                data: JSON.parse(document.getElementById('frequentRestaurantsChart').dataset.data),
                backgroundColor: chartColors,
                borderColor: '#fff',
                borderWidth: 2,
                borderRadius: 8,
                barPercentage: 0.7
            }]
        },
        options: getChartOptions('bar'),
        plugins: [ChartDataLabels]
    });

    // Gráfico de líneas: reservas por día
    const ctx2 = document.getElementById('reservationChart').getContext('2d');
    new Chart(ctx2, {
        type: 'line',
        data: {
            labels: JSON.parse(document.getElementById('reservationChart').dataset.labels),
            datasets: [{
                label: 'Reservas por Día',
                data: JSON.parse(document.getElementById('reservationChart').dataset.data),
                borderColor: '#4e73df',
                backgroundColor: 'rgba(78, 115, 223, 0.1)',
                borderWidth: 3,
                pointBackgroundColor: '#fff',
                pointBorderColor: '#4e73df',
                pointBorderWidth: 2,
                pointRadius: 5,
                pointHoverRadius: 7,
                fill: true,
                tension: 0.4,
                cubicInterpolationMode: 'monotone'
            }]
        },
        options: getChartOptions('line')
    });
}

// Retorna opciones comunes para los distintos tipos de gráfico
function getChartOptions(type) {
    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'right',
                labels: {
                    boxWidth: 12,
                    padding: 20,
                    font: { size: 12 },
                    usePointStyle: true
                }
            },
            tooltip: {
                backgroundColor: 'rgba(0,0,0,0.85)',
                titleFont: { size: 14, weight: 'bold' },
                bodyFont: { size: 12 },
                padding: 12,
                cornerRadius: 8,
                displayColors: true,
                usePointStyle: true
            }
        }
    };

    // Configura etiquetas para gráficos tipo barra o doughnut
    if (type === 'bar' || type === 'doughnut') {
        commonOptions.plugins.datalabels = {
            color: '#fff',
            font: { weight: 'bold', size: 12 },
            formatter: value => value > 0 ? value : '',
            anchor: 'end',
            align: 'end'
        };
    }

    // Configuración específica para el gráfico de líneas
    if (type === 'line') {
        commonOptions.scales = {
            y: {
                beginAtZero: true,
                grid: { drawBorder: false, color: 'rgba(0, 0, 0, 0.03)' },
                ticks: { precision: 0 }
            },
            x: {
                grid: { display: false, drawBorder: false }
            }
        };
        commonOptions.interaction = { intersect: false, mode: 'index' };
    }

    return commonOptions;
}

// Cambia el tipo de gráfico dinámicamente (barra, pastel, etc.)
function changeChartType(type) {
    // Marca el botón seleccionado como activo
    document.querySelectorAll('.chart-btn').forEach(btn => {
        btn.classList.toggle('active', btn.textContent.toLowerCase() === type);
    });

    // Destruye el gráfico anterior y crea uno nuevo con el nuevo tipo
    restaurantChart.destroy();
    const ctx = document.getElementById('frequentRestaurantsChart').getContext('2d');
    restaurantChart = new Chart(ctx, {
        type: type,
        data: {
            labels: JSON.parse(document.getElementById('frequentRestaurantsChart').dataset.labels),
            datasets: [{
                label: 'Visitas',
                data: JSON.parse(document.getElementById('frequentRestaurantsChart').dataset.data),
                backgroundColor: chartColors,
                borderColor: '#fff',
                borderWidth: 2
            }]
        },
        options: getChartOptions(type),
        plugins: [ChartDataLabels]
    });
}