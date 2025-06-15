let selectedImages = [];

function previewImages(input) {
  const preview = document.getElementById('preview');
  preview.innerHTML = '';
  selectedImages = [];

  if (input.files) {
    Array.from(input.files).forEach(file => {
      const reader = new FileReader();
      reader.onload = function (e) {
        const img = document.createElement('img');
        img.src = e.target.result;
        preview.appendChild(img);
      };
      reader.readAsDataURL(file);
      selectedImages.push(file);
    });

    document.getElementById('confirmation').classList.remove('hidden');
  }
}

document.getElementById('cameraInput').addEventListener('change', function () {
  previewImages(this);
});
document.getElementById('galleryInput').addEventListener('change', function () {
  previewImages(this);
});

function uploadImages() {
  if (!selectedImages.length) return;

  const formData = new FormData();
  selectedImages.forEach(image => formData.append('images', image));

  document.getElementById('loading').classList.remove('hidden');
  document.getElementById('confirmation').classList.add('hidden');

  fetch('/upload', {
    method: 'POST',
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      document.getElementById('loading').classList.add('hidden');
      if (data.success !== false && Array.isArray(data.results)) {
        displayResults(data.annotated_images, data.results);
      } else {
        displayError("Неуспешно извличане на цени.");
      }
    })
    .catch(error => {
      document.getElementById('loading').classList.add('hidden');
      displayError("Възникна грешка при качване на изображения.");
    });
}

function displayResults(annotatedImages, allResults) {
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = '';

  allResults.forEach((resultSet, index) => {
    const card = document.createElement('div');
    card.className = 'result-card';

    if (annotatedImages && annotatedImages[index]) {
      const img = document.createElement('img');
      img.src = `data:image/jpeg;base64,${annotatedImages[index]}`;
      img.alt = `Анотирано изображение ${index + 1}`;
      img.className = 'annotated-image';
      card.appendChild(img);
    }

    const header = document.createElement('h6');
    header.textContent = `Намерени цени ${index + 1}`;
    card.appendChild(header);

    if (!Array.isArray(resultSet) || resultSet.length === 0) {
      const empty = document.createElement('p');
      empty.textContent = 'Няма открити цени.';
      card.appendChild(empty);
    } else {
      const table = document.createElement('table');
      table.className = 'ocr-table';
      table.innerHTML = `
        <thead>
          <tr>
            <th>Възможни цени</th>
            <th>Конвентирана цена (лв.)</th>
          </tr>
        </thead>
        <tbody>
          ${resultSet.map(item => `
            <tr>
              <td>${item.original}</td>
              <td>${item.converted_bgn.toFixed(2)}</td>
            </tr>
          `).join('')}
        </tbody>
      `;
      card.appendChild(table);
    }

    resultsDiv.appendChild(card);
  });
}


function displayError(message) {
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = `<div class="result-card error">${message}</div>`;
}
