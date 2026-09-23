const question = document.getElementById('question');
const askBtn = document.getElementById('askBtn');
const result = document.getElementById('result');
const answer = document.getElementById('answer');
const classification = document.getElementById('classification');
const confidence = document.getElementById('confidence');

async function askQuestion() {
  const text = question.value.trim();
  if (!text) {
    question.focus();
    return;
  }

  askBtn.disabled = true;
  askBtn.textContent = 'Checking...';
  result.classList.remove('hidden');
  answer.textContent = 'Please wait...';
  classification.textContent = '';
  confidence.textContent = '';

  try {
    const response = await fetch('/api/ask', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({question: text})
    });
    const data = await response.json();

    if (!response.ok || !data.ok) {
      throw new Error(data.error || 'Request failed');
    }

    classification.textContent = data.classification || '';
    confidence.textContent = data.confidence !== undefined
      ? `Confidence: ${(data.confidence * 100).toFixed(1)}%`
      : '';
    answer.textContent = data.answer || 'No answer returned.';
  } catch (err) {
    answer.textContent = err.message || 'Something went wrong.';
    classification.textContent = 'Error';
    confidence.textContent = '';
  } finally {
    askBtn.disabled = false;
    askBtn.textContent = 'Ask Medical Question';
  }
}

askBtn.addEventListener('click', askQuestion);
question.addEventListener('keydown', (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') askQuestion();
});
