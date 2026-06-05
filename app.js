const urlInput = document.getElementById('url');
const downloadBtn = document.getElementById('downloadBtn');
const status = document.getElementById('status');
const formatBtns = document.querySelectorAll('.format-btn');

let selectedFormat = 'mp3';

formatBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    formatBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    selectedFormat = btn.dataset.format;
  });
});

function setStatus(type, message) {
  status.className = 'status ' + type;
  if (type === 'loading') {
    status.innerHTML = `<span class="spinner"></span>${message}`;
  } else {
    status.textContent = message;
  }
}

function clearStatus() {
  status.className = 'status';
  status.textContent = '';
}

downloadBtn.addEventListener('click', async () => {
  const url = urlInput.value.trim();

  if (!url) {
    setStatus('error', 'Please paste a YouTube URL first.');
    return;
  }

  if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
    setStatus('error', 'That doesn\'t look like a YouTube URL.');
    return;
  }

  downloadBtn.disabled = true;
  setStatus('loading', `Preparing ${selectedFormat.toUpperCase()} download…`);

  try {
    const response = await fetch('http://localhost:5000/download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, format: selectedFormat }),
    });

    if (!response.ok) {
      const err = await response.json().catch(() => ({}));
      throw new Error(err.error || `Server error (${response.status})`);
    }

    const filename = response.headers.get('X-Filename') || `download.${selectedFormat}`;
    const blob = await response.blob();

    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);

    setStatus('success', `✓ "${filename}" is downloading`);
  } catch (err) {
    if (err.message.includes('Failed to fetch')) {
      setStatus('error', 'Cannot reach the local server. Make sure server.py is running.');
    } else {
      setStatus('error', err.message);
    }
  } finally {
    downloadBtn.disabled = false;
  }
});

urlInput.addEventListener('input', clearStatus);
