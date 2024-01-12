// Открыть модальное окно
function openModal() {
    document.getElementById('myModal').style.display = 'block';
}

// Закрыть модальное окно
function closeModal() {
    document.getElementById('myModal').style.display = 'none';
	document.getElementById('myModal2').style.display = 'none';
    document.getElementById('mySchemeModal').style.display = 'none';
}

// Закрыть модальное окно при клике вне окна
window.onclick = function(event) {
    var modal = document.getElementById('myModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};


// Открыть модальное окно
function openSchemeModal() {
    document.getElementById('mySchemeModal').style.display = 'block';
}

// Функция открытия модального окна для отчета
function openReportModal() {
    // Получите данные из основной страницы, например, из элементов формы, и внесите их в тело отчета
    var reportBody = "Текст вашего отчета с данными: " + getDataFromMainPage();

    // Откройте модальное окно и вставьте тело отчета
    document.getElementById('myModal2').style.display = 'block';
    document.getElementById('modalContent2').innerHTML = reportBody;
}

// Функция для получения данных из основной страницы (замените на ваши реальные данные)
function getDataFromMainPage() {
    return "Ваши данные из основной страницы";
}

// Функция сохранения отчета в PDF
function saveReportAsPDF() {
    // Реализуйте сохранение отчета в PDF, например, с использованием библиотеки jsPDF
    // Пример:
    var pdf = new jsPDF();
    pdf.text(document.getElementById('modalContent2').innerText, 10, 10);
    pdf.save("report.pdf");
}

// Функция отправки отчета на печать
function printReport() {
    // Используйте стандартный метод печати браузера
    window.print();
}


function generateReport() {
    // Собираем данные из полей ввода
    var goal = document.getElementById('goal-input').value;
    var output = document.getElementById('output-input').value;
    var theor = document.getElementById('theor-input').value;

    // Собираем данные из таблицы (пример)
    var tableData = [];
    var table = document.getElementById('data-table');
    var data = [];

    // Iterate through rows and cells to collect data
    for (var i = 1; i < table.rows.length; i++) {
        var row = table.rows[i];
        var rowData = [];

        for (var j = 0; j < row.cells.length; j++) {
            rowData.push(row.cells[j].innerText);
        }

        data.push(rowData);
    }

    // Отправляем AJAX запрос на сервер Flask
    fetch('/generate_report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            goal: goal,
            output: output,
            theor: theor,
            tableData: data
            // tableData: tableData
        }),
    })
    .then(response => {
		// Проверяем успешность запроса
		if (!response.ok) {
		  throw new Error(`HTTP error! Status: ${response.status}`);
		}
		
		// Возвращаем ответ в виде blob (файла)
		return response.blob();
	  })
	  .then(blob => {
		// Создаем ссылку для загрузки файла
		const url = window.URL.createObjectURL(blob);
		
		// Создаем ссылку для скачивания файла
		const a = document.createElement('a');
		a.href = url;
		a.download = 'output11.docx'; // Укажите имя файла
		document.body.appendChild(a);
		
		// Запускаем событие "клик" для начала загрузки файла
		a.click();
		
		// Удаляем ссылку после загрузки
		window.URL.revokeObjectURL(url);
	  })
	  .catch(error => {
		// Обрабатываем ошибки
		console.error('Error:', error);
		// Добавьте здесь код для обработки ошибок, если необходимо
	  });
}
