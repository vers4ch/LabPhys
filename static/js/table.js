// Глобальная переменная для хранения ссылки на график
var myChart;

// Функция для создания графика
function createChart() {
	var table = document.getElementById('data-table');
	var rows = table.getElementsByTagName('tr');

	var labels = [];
	var data = [];

	// Проходим по строкам таблицы, начиная с 1, чтобы пропустить заголовок
	for (var i = 1; i < rows.length; i++) {
		var cells = rows[i].getElementsByTagName('td');
		labels.push(cells[1].innerText);  // Значения из столбца L, м.
		data.push(Math.pow(cells[2].innerText, 2));    // Квадрат значения из столбца T, с.
	}

	var ctx = document.getElementById('myChart').getContext('2d');

	// Если график уже существует, уничтожим его перед созданием нового
	if (myChart) {
		myChart.destroy();
	}

	myChart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [{
				label: 'T², L',
				data: data,
				borderColor: 'rgba(75, 192, 192, 1)',
				borderWidth: 1
			}]
		},
		options: {
			scales: {
				x: {
					type: 'linear',
					position: 'bottom'
				},
				y: {
					type: 'linear',
					position: 'left'
				}
			}
		}
	});
}

// Функция для обновления графика
function updateChart() {
	// Ваш код обновления графика, если нужно
	createChart(); // Просто создаем новый график, предполагая, что у вас уже обновленные данные
}