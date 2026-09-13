/**
 * Modern Web Calculator
 * 
 * Demonstrates:
 * 1. DOM Event Listeners (click, keydown)
 * 2. Loops (for...of, forEach for element collection handling and validation)
 * 3. If-Else statements for branching logic & error handling
 * 4. Arithmetic and logical operators (+, -, *, /, %, ===, &&, ||)
 */

class Calculator {
  /**
   * @param {HTMLElement} previousOperandTextElement 
   * @param {HTMLElement} currentOperandTextElement 
   */
  constructor(previousOperandTextElement, currentOperandTextElement) {
    this.previousOperandTextElement = previousOperandTextElement;
    this.currentOperandTextElement = currentOperandTextElement;
    this.clear();
  }

  /**
   * Resets all calculator states (AC - All Clear)
   */
  clear() {
    this.currentOperand = '0';
    this.previousOperand = '';
    this.operation = undefined;
    this.shouldResetScreen = false;
  }

  /**
   * Deletes the last entered character (DEL / Backspace)
   * Uses if-else statements to handle screen reset and boundary cases.
   */
  delete() {
    // REQUIREMENT: If-Else Statement
    if (this.shouldResetScreen) {
      this.clear();
      return;
    }

    if (
      this.currentOperand === '0' || 
      this.currentOperand === 'Error' || 
      this.currentOperand === 'Cannot divide by 0'
    ) {
      this.currentOperand = '0';
      return;
    }

    // If only one digit or negative single digit (e.g., "-5"), reset to '0'
    if (
      this.currentOperand.length <= 1 || 
      (this.currentOperand.length === 2 && this.currentOperand.startsWith('-'))
    ) {
      this.currentOperand = '0';
    } else {
      this.currentOperand = this.currentOperand.slice(0, -1);
    }
  }

  /**
   * Appends a number or decimal point to the current operand
   * @param {string} number 
   */
  appendNumber(number) {
    // REQUIREMENT: If-Else Statements for input validation
    if (this.currentOperand === 'Error' || this.currentOperand === 'Cannot divide by 0') {
      this.clear();
    }

    if (this.shouldResetScreen) {
      this.currentOperand = '';
      this.shouldResetScreen = false;
    }

    // Decimal point handling
    if (number === '.') {
      // Prevent multiple decimals in the same number
      if (this.currentOperand.includes('.')) {
        return;
      }
      // If decimal is pressed first, prefix with 0
      if (this.currentOperand === '' || this.currentOperand === '0') {
        this.currentOperand = '0.';
        return;
      }
    }

    // Prevent duplicate leading zeros (e.g. "000")
    if (this.currentOperand === '0' && number !== '.') {
      this.currentOperand = number;
    } else {
      this.currentOperand = this.currentOperand + number;
    }
  }

  /**
   * Toggles the positive/negative sign of the active operand
   */
  negate() {
    // REQUIREMENT: If-Else Statements
    if (
      this.currentOperand === '0' || 
      this.currentOperand === 'Error' || 
      this.currentOperand === 'Cannot divide by 0'
    ) {
      return;
    }

    if (this.currentOperand.startsWith('-')) {
      this.currentOperand = this.currentOperand.substring(1);
    } else {
      this.currentOperand = '-' + this.currentOperand;
    }
  }

  /**
   * Calculates the percentage of the current operand
   */
  computePercent() {
    const current = parseFloat(this.currentOperand);
    // REQUIREMENT: If-Else validation
    if (isNaN(current)) {
      return;
    }

    // REQUIREMENT: Arithmetic operator (/)
    const result = current / 100;
    this.currentOperand = this.formatNumber(result);
  }

  /**
   * Selects the mathematical operation (+, −, ×, ÷)
   * @param {string} operation 
   */
  chooseOperation(operation) {
    if (this.currentOperand === 'Error' || this.currentOperand === 'Cannot divide by 0') {
      this.clear();
      return;
    }

    // If user changes operation before entering the second operand
    if (this.currentOperand === '' && this.previousOperand !== '') {
      this.operation = operation;
      return;
    }

    // If both operands exist, compute intermediate result
    // REQUIREMENT: If-Else Statement & Logical Operators (&&)
    if (this.previousOperand !== '' && this.currentOperand !== '') {
      this.compute();
    }

    this.operation = operation;
    this.previousOperand = this.currentOperand;
    this.currentOperand = '';
    this.shouldResetScreen = false;
  }

  /**
   * Performs the calculation based on previousOperand, currentOperand, and chosen operation
   * Highlights: Arithmetic Operators (+, -, *, /) and If-Else Statements
   */
  compute() {
    let computation;
    const prev = parseFloat(this.previousOperand);
    const current = parseFloat(this.currentOperand);

    // REQUIREMENT: If-Else Statements & Logical Operators (||)
    if (isNaN(prev) || isNaN(current)) {
      return;
    }

    // REQUIREMENT: Performing calculations using if-else and arithmetic operators
    if (this.operation === '+') {
      computation = prev + current;
    } else if (this.operation === '−' || this.operation === '-') {
      computation = prev - current;
    } else if (this.operation === '×' || this.operation === '*') {
      computation = prev * current;
    } else if (this.operation === '÷' || this.operation === '/') {
      // Handle division by zero edge case
      if (current === 0) {
        this.currentOperand = 'Cannot divide by 0';
        this.previousOperand = '';
        this.operation = undefined;
        this.shouldResetScreen = true;
        return;
      } else {
        computation = prev / current;
      }
    } else {
      return;
    }

    // Fix floating point precision issues (e.g. 0.1 + 0.2 = 0.30000000000000004)
    const rounded = Math.round((computation + Number.EPSILON) * 1e12) / 1e12;
    this.currentOperand = rounded.toString();
    this.operation = undefined;
    this.previousOperand = '';
    this.shouldResetScreen = true;
  }

  /**
   * Helper function to format numbers with thousand separators
   * @param {number|string} number 
   */
  formatDisplayNumber(number) {
    const stringNumber = number.toString();
    if (stringNumber === 'Cannot divide by 0' || stringNumber === 'Error') {
      return stringNumber;
    }

    const integerDigits = parseFloat(stringNumber.split('.')[0]);
    const decimalDigits = stringNumber.split('.')[1];
    let integerDisplay;

    // REQUIREMENT: If-Else Statement
    if (isNaN(integerDigits)) {
      integerDisplay = '';
    } else {
      integerDisplay = integerDigits.toLocaleString('en', { maximumFractionDigits: 0 });
    }

    if (decimalDigits != null) {
      return `${integerDisplay}.${decimalDigits}`;
    } else {
      return integerDisplay;
    }
  }

  /**
   * Formats raw numeric results cleanly
   * @param {number} num 
   */
  formatNumber(num) {
    return (Math.round((num + Number.EPSILON) * 1e12) / 1e12).toString();
  }

  /**
   * Updates the display screen elements
   */
  updateDisplay() {
    // Current operand display
    if (this.currentOperand === 'Cannot divide by 0') {
      this.currentOperandTextElement.innerText = this.currentOperand;
      this.currentOperandTextElement.style.fontSize = '1.35rem';
    } else {
      this.currentOperandTextElement.style.fontSize = '';
      if (this.currentOperand !== '') {
        this.currentOperandTextElement.innerText = this.formatDisplayNumber(this.currentOperand);
      } else {
        this.currentOperandTextElement.innerText = '0';
      }
    }

    // Previous operand and operation history display
    if (this.operation != null) {
      this.previousOperandTextElement.innerText = 
        `${this.formatDisplayNumber(this.previousOperand)} ${this.operation}`;
    } else {
      this.previousOperandTextElement.innerText = '';
    }
  }
}

// ==========================================================================
// INITIALIZATION & EVENT LISTENERS SETUP
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const previousOperandTextElement = document.getElementById('previous-operand');
  const currentOperandTextElement = document.getElementById('current-operand');
  const allButtons = document.querySelectorAll('.keypad .btn');

  // Create Calculator Instance
  const calculator = new Calculator(previousOperandTextElement, currentOperandTextElement);

  // ------------------------------------------------------------------------
  // REQUIREMENT: Using Loops to Process Buttons
  // ------------------------------------------------------------------------
  // Using a for...of loop to iterate through every button element and bind
  // the corresponding event listener dynamically.
  for (const button of allButtons) {
    // REQUIREMENT: Event Listener for user click input
    button.addEventListener('click', () => {
      handleButtonInput(button);
      calculator.updateDisplay();
    });
  }

  /**
   * Routes button clicks based on attributes
   * REQUIREMENT: If-Else Statements to handle user input
   * @param {HTMLButtonElement} button 
   */
  function handleButtonInput(button) {
    const number = button.getAttribute('data-number');
    const operator = button.getAttribute('data-operator');
    const action = button.getAttribute('data-action');

    if (number !== null) {
      calculator.appendNumber(number);
    } else if (operator !== null) {
      calculator.chooseOperation(operator);
    } else if (action === 'calculate') {
      calculator.compute();
    } else if (action === 'all-clear') {
      calculator.clear();
    } else if (action === 'delete') {
      calculator.delete();
    } else if (action === 'decimal') {
      calculator.appendNumber('.');
    } else if (action === 'negate') {
      calculator.negate();
    } else if (action === 'percent') {
      calculator.computePercent();
    }
  }

  // ------------------------------------------------------------------------
  // REQUIREMENT: Keyboard Event Listener for Complete Interactivity
  // ------------------------------------------------------------------------
  window.addEventListener('keydown', (event) => {
    const key = event.key;

    // REQUIREMENT: If-Else Decision Tree for Keyboard Input
    if ((key >= '0' && key <= '9')) {
      calculator.appendNumber(key);
      highlightKey(key);
    } else if (key === '.') {
      calculator.appendNumber('.');
      highlightKey('.');
    } else if (key === '+' || key === '-') {
      const opSymbol = key === '-' ? '−' : '+';
      calculator.chooseOperation(opSymbol);
      highlightKey(opSymbol);
    } else if (key === '*') {
      calculator.chooseOperation('×');
      highlightKey('×');
    } else if (key === '/') {
      event.preventDefault(); // Prevent browser quick-find
      calculator.chooseOperation('÷');
      highlightKey('÷');
    } else if (key === 'Enter' || key === '=') {
      event.preventDefault(); // Prevent default form behavior
      calculator.compute();
      highlightKey('=');
    } else if (key === 'Backspace') {
      calculator.delete();
      highlightKey('DEL');
    } else if (key === 'Escape') {
      calculator.clear();
      highlightKey('AC');
    } else if (key === '%') {
      calculator.computePercent();
      highlightKey('%');
    }

    calculator.updateDisplay();
  });

  /**
   * Helper function: Visual feedback for keyboard presses
   * REQUIREMENT: Loop to search matching button
   * @param {string} identifier 
   */
  function highlightKey(identifier) {
    for (const btn of allButtons) {
      const match = 
        btn.innerText === identifier ||
        btn.getAttribute('data-number') === identifier ||
        btn.getAttribute('data-operator') === identifier ||
        (identifier === '.' && btn.getAttribute('data-action') === 'decimal') ||
        (identifier === '=' && btn.getAttribute('data-action') === 'calculate') ||
        (identifier === 'DEL' && btn.getAttribute('data-action') === 'delete') ||
        (identifier === 'AC' && btn.getAttribute('data-action') === 'all-clear');

      if (match) {
        btn.classList.add('active');
        setTimeout(() => btn.classList.remove('active'), 150);
        break; // Exit loop early once matched
      }
    }
  }

  // Initial display render
  calculator.updateDisplay();
});
