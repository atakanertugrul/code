// DOM Elements
const productForm = document.getElementById('productForm');
const generateBtn = document.getElementById('generateBtn');
const copyBtn = document.getElementById('copyBtn');

const loadingState = document.getElementById('loadingState');
const errorState = document.getElementById('errorState');
const resultState = document.getElementById('resultState');
const emptyState = document.getElementById('emptyState');

const descriptionOutput = document.getElementById('descriptionOutput');
const errorMessage = document.querySelector('.error-message');

// State Management
let currentDescription = '';

// Show/Hide States
function showState(state) {
    loadingState.style.display = 'none';
    errorState.style.display = 'none';
    resultState.style.display = 'none';
    emptyState.style.display = 'none';

    if (state === 'loading') {
        loadingState.style.display = 'flex';
    } else if (state === 'error') {
        errorState.style.display = 'flex';
    } else if (state === 'result') {
        resultState.style.display = 'flex';
    } else if (state === 'empty') {
        emptyState.style.display = 'flex';
    }
}

// Form Submission
productForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get form data
    const formData = {
        product_name: document.getElementById('product_name').value.trim(),
        category: document.getElementById('category').value.trim(),
        features: document.getElementById('features').value.trim(),
        target_audience: document.getElementById('target_audience').value.trim(),
        tone: document.getElementById('tone').value,
        language: document.getElementById('language').value
    };

    // Validate
    if (!formData.product_name) {
        showError('Lütfen ürün adını girin!');
        return;
    }

    // Show loading state
    showState('loading');
    generateBtn.disabled = true;

    try {
        // Call API
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Bir hata oluştu');
        }

        if (data.success) {
            currentDescription = data.description;
            displayDescription(data.description);
            showState('result');
        } else {
            throw new Error(data.error || 'Açıklama oluşturulamadı');
        }

    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'Bir hata oluştu. Lütfen tekrar deneyin.');
    } finally {
        generateBtn.disabled = false;
    }
});

// Display Description
function displayDescription(description) {
    // Format the description with basic HTML
    let formatted = description
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
        .replace(/\*(.*?)\*/g, '<em>$1</em>') // Italic
        .replace(/\n\n/g, '</p><p>') // Paragraphs
        .replace(/\n/g, '<br>'); // Line breaks

    descriptionOutput.innerHTML = `<p>${formatted}</p>`;
}

// Show Error
function showError(message) {
    errorMessage.textContent = message;
    showState('error');
}

// Copy to Clipboard
copyBtn.addEventListener('click', async () => {
    try {
        await navigator.clipboard.writeText(currentDescription);

        // Visual feedback
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✓ Kopyalandı!';
        copyBtn.style.background = '#27ae60';

        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = '';
        }, 2000);
    } catch (error) {
        console.error('Copy failed:', error);
        alert('Kopyalama başarısız oldu. Lütfen manuel olarak kopyalayın.');
    }
});

// Initialize
showState('empty');
