document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('networkSelect').addEventListener('change', updateTheme);
    updateTheme(); // Imposta il tema iniziale
});

function updateTheme() {
    const network = document.getElementById('networkSelect').value;
    document.body.setAttribute('data-theme', network);

    // Resetta l'indirizzo quando si cambia rete
    document.getElementById('addressDisplay').textContent = "";
}

async function fetchNewAddress() {
    const network = document.getElementById('networkSelect').value;

    try {
        const response = await fetch(`/generate?network=${network}`);
        const data = await response.json();
        document.getElementById('addressDisplay').textContent = data.address;
        window.currentData = data;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('addressDisplay').textContent = 'Errore nella generazione';
    }
}

function generateNewAddress() {
    document.getElementById('addressDisplay').textContent = 'Generazione in corso...';
    fetchNewAddress();
}

function downloadKey() {
    if (!window.currentData) {
        alert('Nessuna chiave generata ancora!');
        return;
    }

    const blob = new Blob([JSON.stringify(window.currentData, null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `key.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}
