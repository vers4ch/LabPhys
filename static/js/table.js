// Функция для сбора данных и отправки на сервер
function sendDataToServer() {
    var table = document.getElementById('data-table');
    var rows = table.getElementsByTagName('tr');

    var allData = [];

    // Проходим по строкам таблицы, начиная с 1, чтобы пропустить заголовок
    for (var i = 1; i < rows.length; i++) {
        var cells = rows[i].getElementsByTagName('td');
        
        var rowData = {
            'опыт': cells[0].innerText,
            'номер_измерения': cells[1].innerText,
            'L': cells[2].innerText,
            'T': cells[3].innerText,
            'Тср.': cells[4].innerText,
            'g': cells[5].innerText
        };

        allData.push(rowData);
    }

    // Отправляем данные на сервер (замените URL на ваш)
    fetch('/generate_report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(allData)
    })
    .then(response => response.json())
    .then(data => console.log('Ответ от сервера:', data))
    .catch(error => console.error('Ошибка при отправке данных:', error));
}

// Вызываем функцию отправки данных при загрузке страницы
window.onload = sendDataToServer;
