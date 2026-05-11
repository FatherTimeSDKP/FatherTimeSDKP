let display = document.getElementById('display');
let currentInput = '';
let previousInput = '';
let operator = '';
let shouldResetDisplay = false;

// Append number to display
function appendNumber(number) {
    if (shouldResetDisplay) {
        currentInput = '';
        shouldResetDisplay = false;
    }
    
    // Prevent multiple leading zeros
    if (currentInput === '0' && number === '0') return;
    
    // Replace leading zero with new number
    if (currentInput === '0' && number !== '.') {
        currentInput = number;
    } else {
        currentInput += number;
    }
    
    updateDisplay();
}

// Append operator
function appendOperator(op) {
    if (currentInput === '' && previousInput === '') return;
    
    // If there's already an operator and current input, calculate first
    if (operator !== '' && currentInput !== '') {
        calculate();
    } else if (currentInput !== '') {
        previousInput = currentInput;
        currentInput = '';
    }
    
    operator = op;
    shouldResetDisplay = true;
}

// Handle decimal point
function appendDecimal() {
    if (shouldResetDisplay) {
        currentInput = '0';
        shouldResetDisplay = false;
    }
    
    // Prevent multiple decimals
    if (currentInput.includes('.')) return;
    
    if (currentInput === '') {
        currentInput = '0';
    }
    
    currentInput += '.';
    updateDisplay();
}

// Clear display
function clearDisplay() {
    currentInput = '';
    previousInput = '';
    operator = '';
    shouldResetDisplay = false;
    updateDisplay();
}

// Delete last character
function deleteLast() {
    if (currentInput !== '') {
        currentInput = currentInput.slice(0, -1);
        updateDisplay();
    }
}

// Calculate result
function calculate() {
    if (currentInput === '' || previousInput === '' || operator === '') return;
    
    let result;
    const prev = parseFloat(previousInput);
    const current = parseFloat(currentInput);
    
    switch (operator) {
        case '+':
            result = prev + current;
            break;
        case '-':
            result = prev - current;
            break;
        case '*':
            result = prev * current;
            break;
        case '/':
            if (current === 0) {
                alert('Cannot divide by zero!');
                clearDisplay();
                return;
            }
            result = prev / current;
            break;
        default:
            return;
    }
    
    // Handle floating point precision
    result = Math.round(result * 100000000) / 100000000;
    
    currentInput = result.toString();
    operator = '';
    previousInput = '';
    shouldResetDisplay = true;
    updateDisplay();
}

// Update display
function updateDisplay() {
    display.value = currentInput || '0';
}

// Keyboard support
document.addEventListener('keydown', (e) => {
    if (e.key >= '0' && e.key <= '9') {
        appendNumber(e.key);
    } else if (e.key === '.') {
        appendDecimal();
    } else if (e.key === '+') {
        appendOperator('+');
    } else if (e.key === '-') {
        appendOperator('-');
    } else if (e.key === '*') {
        appendOperator('*');
    } else if (e.key === '/') {
        e.preventDefault();
        appendOperator('/');
    } else if (e.key === 'Enter' || e.key === '=') {
        e.preventDefault();
        calculate();
    } else if (e.key === 'Backspace') {
        deleteLast();
    } else if (e.key === 'Escape') {
        clearDisplay();
    }
});

// Initialize display
updateDisplay();
