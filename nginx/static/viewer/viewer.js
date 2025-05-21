let xmlLoaded = false;
let debtLoaded = false;
let allRecordsLoaded = false;

document.getElementById('toggle-xml-btn').addEventListener('click', function () {
  const display = document.getElementById('xml-display');
  const toggleBtn = this;

  if (!xmlLoaded) {
    fetch('/api/generator/get_xml')
      .then(res => res.text())
      .then(data => {
        display.textContent = data.trim() || "Brak XML";
        display.style.display = "block";
        toggleBtn.textContent = "Ukryj XML";
        xmlLoaded = true;
      })
      .catch(() => {
        display.textContent = "Błąd ładowania XML";
        display.style.display = "block";
        toggleBtn.textContent = "Ukryj XML";
      });
  } else {
    const isVisible = display.style.display !== "none";
    display.style.display = isVisible ? "none" : "block";
    toggleBtn.textContent = isVisible ? "Pokaż XML" : "Ukryj XML";
  }
});

document.getElementById('top-debt-btn').addEventListener('click', function () {
  const table = document.getElementById('debt-table');
  const toggleBtn = this;

  if (!debtLoaded) {
    fetch('/api/stats/top_cities_by_debt')
      .then(res => res.json())
      .then(resp => {
        const data = resp.data;
        const tbody = document.getElementById('debt-table-body');
        tbody.innerHTML = '';
        if (Array.isArray(data)) {
          data.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td class="border p-2">${row._id}</td><td class="border p-2">${row.total_debt.toFixed(2)}</td>`;
            tbody.appendChild(tr);
          });
          table.style.display = "table";
          toggleBtn.textContent = "Ukryj długi";
          debtLoaded = true;
        } else {
          alert("Brak danych");
        }
      })
      .catch(() => alert("Błąd ładowania danych"));
  } else {
    const isVisible = table.style.display !== "none";
    table.style.display = isVisible ? "none" : "table";
    toggleBtn.textContent = isVisible ? "Top miasta wg długu" : "Ukryj długi";
  }
});
  

document.getElementById('query-all-btn').addEventListener('click', async function () {
  const table = document.getElementById('all-records-table');
  const toggleBtn = this;
  const filterContainer = document.getElementById('filter-container');

  if (!allRecordsLoaded) {
    try {
      const res = await fetch('/api/stats/all_records');
      const data = await res.json();
      if (data.status !== 'success' || !Array.isArray(data.data)) {
        alert("Błąd danych");
        return;
      }

      const thead = table.querySelector('thead tr');
      const tbody = table.querySelector('tbody');
      const filterInput = document.getElementById('record-filter');

      thead.innerHTML = '';
      tbody.innerHTML = '';
      filterContainer.classList.remove('hidden');

      const columns = Object.keys(data.data[0]);
      columns.forEach(col => {
        const th = document.createElement('th');
        th.textContent = col;
        th.className = 'border p-2';
        thead.appendChild(th);
      });

      data.data.forEach(doc => {
        const tr = document.createElement('tr');
        tr.classList.add('data-row');
        columns.forEach(col => {
          const td = document.createElement('td');
          td.textContent = doc[col];
          td.className = 'border p-2';
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });

      table.style.display = 'table';
      toggleBtn.textContent = 'Ukryj rekordy';
      allRecordsLoaded = true;

      filterInput.addEventListener('input', function () {
        const search = this.value.toLowerCase();
        const rows = document.querySelectorAll('#all-records-table tbody tr');
        rows.forEach(row => {
          const text = row.textContent.toLowerCase();
          row.style.display = text.includes(search) ? '' : 'none';
        });
      });

    } catch {
      alert("Błąd ładowania rekordów");
    }
  } else {
    const isVisible = table.style.display !== "none";
    table.style.display = isVisible ? "none" : "table";
    filterContainer.classList.toggle('hidden', isVisible);
    toggleBtn.textContent = isVisible ? "Wszystkie rekordy" : "Ukryj rekordy";
  }
});
