document.getElementById('generate-btn').addEventListener('click', function () {
    const numRecords = parseInt(document.getElementById('record-count').value) || 10000;
    fetch('/api/generator/generate_xml', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ num_of_records: numRecords, currency: 'PLN' })
    })
    .then(res => res.json())
    .then(data => alert(data.message || "Wygenerowano XML"))
    .catch(() => alert("Błąd generowania XML"));
  });
  
  document.getElementById('convert-btn').addEventListener('click', function () {
    fetch('/api/generator/convert_xml_to_json', { method: 'POST' })
      .then(res => res.json())
      .then(data => alert(data.message || "Konwersja zakończona"))
      .catch(() => alert("Błąd konwersji"));
  });
  
  document.getElementById('download-yml-btn').addEventListener('click', function () {
    fetch('/api/generator/download_yml')
      .then(res => res.blob())
      .then(blob => {
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'data.yml';
        link.click();
      })
      .catch(() => alert("Błąd pobierania YML"));
  });
  