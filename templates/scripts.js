function clearTables() {
    const reqsTable = document.getElementById('reqs-table');
    const termsTable = document.getElementById('terms-table');
    const chargesTable = document.getElementById('charges-table');
    const notesTable = document.getElementById('notes-table');

    reqsTable.innerHTML = '';
    termsTable.innerHTML = '';
    chargesTable.innerHTML = '';
    notesTable.innerHTML = '';
}

function updateTableHeights() {
    const reqsTable = document.getElementById('reqs-table');
    const termsTable = document.getElementById('terms-table');
    const chargesTable = document.getElementById('charges-table');
    const notesTable = document.getElementById('notes-table');

    const maxTableHeight = Math.max(
        reqsTable.offsetHeight,
        termsTable.offsetHeight,
        chargesTable.offsetHeight,
        notesTable.offsetHeight
    );

    reqsTable.style.height = maxTableHeight + 'px';
    termsTable.style.height = maxTableHeight + 'px';
    chargesTable.style.height = maxTableHeight + 'px';
    notesTable.style.height = maxTableHeight + 'px';
}

async function sendTextToServer(text) {
    try {
        const response = await fetch('/change_text', { // Изменили URL запроса на текущий хост
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text
            })
        });

        if (response.ok) {
            const data = await response.json();
            return data.newText;
        } else {
            throw new Error('Ошибка при отправке запроса на сервер');
        }
    } catch (error) {
        console.error(error);
    }
}


document.getElementById('input-text').addEventListener('input', async function(e) {
    const inputValue = e.target.value;
    const outputText = document.getElementById('output-text');
    const newText = await sendTextToServer(inputValue);
    const reqs = newText[0]
    const terms = newText[1]
    const charges = newText[2]
    const notes = newText[3]
    clearTables();
    let reqsTable = document.getElementById('reqs-table');
    for (var i = 0; i < reqs.length; i++) {
        var row = reqsTable.insertRow();
        var cell = row.insertCell();
        cell.textContent = reqs[i];
    }
    var termsTable = document.getElementById('terms-table');
    for (var i = 0; i < terms.length; i++) {
        var row = termsTable.insertRow();
        var cell = row.insertCell();
        cell.textContent = terms[i];
    }

    // Заполняем таблицу "Обязанности"
    var chargesTable = document.getElementById('charges-table');
    for (var i = 0; i < charges.length; i++) {
        var row = chargesTable.insertRow();
        var cell = row.insertCell();
        cell.textContent = charges[i];
    }

    // Заполняем таблицу "Примечания"
    var notesTable = document.getElementById('notes-table');
    for (var i = 0; i < notes.length; i++) {
        var row = notesTable.insertRow();
        var cell = row.insertCell();
        cell.textContent = notes[i];
    }
    updateTableHeights();
});
document.getElementById("example-button").addEventListener("click", function() {
  fetch('/sample')
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      var sample = data.sample;
      var inputText = document.getElementById("input-text");
      setTimeout(function() {
      inputText.value = sample;
      inputText.dispatchEvent(new Event('input'));
    }, 0);
    })
    .catch(function(error) {
      console.log('Error:', error);
    });
});

document.getElementById('file-upload').addEventListener('change', function(e) {
    var file = e.target.files[0];
    var reader = new FileReader();
    var formData = new FormData();
    formData.append('file',file)
    fetch('/upload', {
      method: 'POST',
      body: formData
    })
    .then(function(response) {
      if (response.ok) {
        console.log('Файл успешно загружен');
      } else {
        console.log('Ошибка загрузки файла');
      }
    })
    .catch(function(error) {
      console.log('Ошибка при отправке запроса:', error.message);
    });

    reader.onload = function(e) {
        var data = new Uint8Array(e.target.result);
        var workbook = XLSX.read(data, {
            type: 'array'
        });
        var worksheet = workbook.Sheets[workbook.SheetNames[0]];
        var jsonData = XLSX.utils.sheet_to_json(worksheet, {
            header: 1
        });

        // Отображение таблицы
        var tableContainer = document.getElementById('table-container');
        tableContainer.innerHTML = '';

        var table = document.createElement('table');

        // Создание заголовка таблицы
        var headerRow = document.createElement('tr');
        for (var i = 0; i < jsonData[0].length; i++) {
            var cell = document.createElement('th');
            cell.textContent = jsonData[0][i];
            headerRow.appendChild(cell);
        }
        table.appendChild(headerRow);

        // Создание строк и ячеек таблицы (случайные 5 строк)
        var randomRows = getRandomRows(jsonData, 5);
        for (var i = 1; i < randomRows.length; i++) {
            var row = document.createElement('tr');
            for (var j = 0; j < randomRows[i].length; j++) {
                var cell = document.createElement('td');
                cell.textContent = randomRows[i][j];
                row.appendChild(cell);
            }
            table.appendChild(row);
        }

        tableContainer.appendChild(table);
    };

    reader.readAsArrayBuffer(file);
});

// Функция для получения случайных строк из массива данных
function getRandomRows(data, count) {
    var rows = [];
    var rowIndexes = getRandomIndexes(data.length - 1, count);

    for (var i = 0; i < rowIndexes.length; i++) {
        rows.push(data[rowIndexes[i] + 1]);
    }

    return rows;
}

// Функция для получения случайных индексов
function getRandomIndexes(maxIndex, count) {
    var indexes = [];
    while (indexes.length < count) {
        var randomIndex = Math.floor(Math.random() * (maxIndex + 1));
        if (!indexes.includes(randomIndex)) {
            indexes.push(randomIndex);
        }
    }
    return indexes;
}

document.querySelector('.download-btn').addEventListener('click', function() {
  window.location.href = '/download';
});

