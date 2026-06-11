/**
 * AetherCalc - Scientific Calculator Controller and Mathematical Parser
 * Implements a safe tokenizing recursive descent parser with extensive error handling.
 */

document.addEventListener('DOMContentLoaded', () => {
  // UI Elements
  const displayMain = document.getElementById('display-main');
  const displayExpr = document.getElementById('display-expr');
  const errorBadge = document.getElementById('error-badge');
  const modeDegRad = document.getElementById('mode-deg-rad');
  const mode2ndBadge = document.getElementById('mode-2nd');
  
  const btn2nd = document.getElementById('btn-2nd');
  const btnDegRad = document.getElementById('btn-deg-rad');
  const btnHistoryToggle = document.getElementById('history-toggle');
  const btnHistoryClose = document.getElementById('history-close');
  const historyDrawer = document.getElementById('history-drawer');
  const historyList = document.getElementById('history-list');
  const btnClearHistory = document.getElementById('clear-history');
  const btnThemeToggle = document.getElementById('theme-toggle');
  
  const keypadContainer = document.querySelector('.keypad-container');
  const btnShowBasic = document.getElementById('btn-show-basic');
  const btnShowSci = document.getElementById('btn-show-scientific');

  // Calculator State
  let angleMode = 'DEG'; // 'DEG' or 'RAD'
  let is2ndActive = false;
  let lastAnswer = 0;
  let isResultDisplayed = false;
  let isErrorState = false;

  // Initialize
  initCalculator();

  function initCalculator() {
    setupTheme();
    setupEventListeners();
    loadHistory();
    runSelfTests();
  }

  // --- Theme Controller ---
  function setupTheme() {
    const savedTheme = localStorage.getItem('calc-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
  }

  function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('calc-theme', newTheme);
  }

  // --- Mobile Tab Toggles ---
  if (btnShowBasic && btnShowSci && keypadContainer) {
    btnShowBasic.addEventListener('click', () => {
      keypadContainer.classList.remove('show-scientific');
      keypadContainer.classList.add('show-basic');
      btnShowBasic.classList.add('active');
      btnShowSci.classList.remove('active');
    });

    btnShowSci.addEventListener('click', () => {
      keypadContainer.classList.remove('show-basic');
      keypadContainer.classList.add('show-scientific');
      btnShowSci.classList.add('active');
      btnShowBasic.classList.remove('active');
    });
  }

  // --- Event Listeners Setup ---
  function setupEventListeners() {
    // Buttons Click Event Delegations
    document.querySelectorAll('.btn').forEach(button => {
      button.addEventListener('click', handleButtonClick);
    });

    // Theme Toggle
    btnThemeToggle.addEventListener('click', toggleTheme);

    // History Panel Drawer Controls
    btnHistoryToggle.addEventListener('click', () => historyDrawer.classList.add('open'));
    btnHistoryClose.addEventListener('click', () => historyDrawer.classList.remove('open'));
    btnClearHistory.addEventListener('click', clearHistory);

    // Dynamic keyboard input formatting and error resets
    displayMain.addEventListener('input', handleKeyboardInput);
    
    // Physical Keyboard key bindings (global)
    document.addEventListener('keydown', handlePhysicalKeyboard);
  }

  // --- Handle Click Operations ---
  const label2nd = {
    'sin': 'sin<sup>-1</sup>', 'cos': 'cos<sup>-1</sup>', 'tan': 'tan<sup>-1</sup>',
    '^': '<sup>y</sup>√x', 'sqrt': '<sup>3</sup>√', 'sqr': 'x³',
    'ln': 'e<sup>x</sup>', 'log': '10<sup>x</sup>'
  };
  const labelNormal = {
    'sin': 'sin', 'cos': 'cos', 'tan': 'tan',
    '^': 'x<sup>y</sup>', 'sqrt': '√', 'sqr': 'x²',
    'ln': 'ln', 'log': 'log'
  };

  function handleButtonClick(e) {
    const btn = e.currentTarget;
    const action = btn.dataset.action;
    const value = btn.dataset.val;
    const shiftVal = btn.dataset.shiftVal;

    // Reset error state on click
    if (isErrorState) {
      clearDisplay();
    }

    // Handle special toggles first
    if (action === '2nd') {
      is2ndActive = !is2ndActive;
      btn2nd.classList.toggle('active', is2ndActive);
      updateButtonLabels();
      return;
    }

    if (action === 'deg-rad') {
      angleMode = angleMode === 'DEG' ? 'RAD' : 'DEG';
      btnDegRad.textContent = angleMode;
      modeDegRad.textContent = angleMode;
      return;
    }

    if (action === 'clear') {
      clearDisplay();
      return;
    }

    if (action === 'delete') {
      backspace();
      return;
    }

    if (action === 'equal') {
      calculateResult();
      return;
    }

    if (action === 'ans') {
      insertText(`ans`);
      return;
    }

    // Normal button inputs (numbers/operators/functions)
    let inputToInsert = '';
    
    if (is2ndActive && shiftVal) {
      inputToInsert = getButtonInputValue(shiftVal);
      // Automatically turn off 2nd after a click (standard calculator behavior)
      is2ndActive = false;
      btn2nd.classList.remove('active');
      updateButtonLabels();
    } else if (value) {
      inputToInsert = getButtonInputValue(value);
    }

    if (inputToInsert) {
      // If result is displayed and we type a number or function, start fresh.
      // If we type an operator, append to the result.
      if (isResultDisplayed) {
        const isOperator = ['+', '-', '*', '/', '÷', '×', '^', '%', '!', '²', '³'].includes(inputToInsert.trim()[0]) || 
                           ['+', '-', '*', '/', '%'].includes(inputToInsert.trim());
        if (!isOperator) {
          displayMain.value = '';
        }
        isResultDisplayed = false;
      }
      insertText(inputToInsert);
    }
  }

  function getButtonInputValue(val) {
    // Returns the proper string to insert in display screen
    switch (val) {
      case 'sin': return 'sin(';
      case 'cos': return 'cos(';
      case 'tan': return 'tan(';
      case 'asin': return 'asin(';
      case 'acos': return 'acos(';
      case 'atan': return 'atan(';
      case 'ln': return 'ln(';
      case 'log': return 'log(';
      case 'sqrt': return '√(';
      case 'cbrt': return 'cbrt(';
      case 'abs': return 'abs(';
      case 'exp': return 'exp(';
      case '10^': return '10^(';
      case 'sqr': return '²';
      case 'cube': return '³';
      case 'pi': return 'π';
      case 'e': return 'e';
      case '*': return '×';
      case '/': return '÷';
      case '-': return '−';
      default: return val;
    }
  }

  function updateButtonLabels() {
    document.querySelectorAll('.btn-sci').forEach(btn => {
      const val = btn.dataset.val;
      if (label2nd[val] && labelNormal[val]) {
        btn.innerHTML = is2ndActive ? label2nd[val] : labelNormal[val];
      }
    });
    mode2ndBadge.style.display = is2ndActive ? 'inline-block' : 'none';
  }

  // --- Insertion & Caret Management ---
  function insertText(text) {
    const input = displayMain;
    const start = input.selectionStart;
    const end = input.selectionEnd;
    const val = input.value;
    
    input.value = val.substring(0, start) + text + val.substring(end);
    
    const newPos = start + text.length;
    input.setSelectionRange(newPos, newPos);
    input.focus();
    scrollDisplayToEnd();
  }

  function backspace() {
    const input = displayMain;
    const start = input.selectionStart;
    const end = input.selectionEnd;
    const val = input.value;

    if (start === 0 && end === 0) return;

    if (start !== end) {
      // Delete selected block
      input.value = val.substring(0, start) + val.substring(end);
      input.setSelectionRange(start, start);
    } else {
      // Check if deleting a multi-char function e.g. "sin(", "asin(", "log("
      // Find what precedes the cursor
      let deleteCount = 1;
      const precede = val.substring(0, start);
      
      const functions = ['asin(', 'acos(', 'atan(', 'cbrt(', 'exp(', 'sin(', 'cos(', 'tan(', 'log(', 'ln(', 'abs(', '10^('];
      for (const fn of functions) {
        if (precede.endsWith(fn)) {
          deleteCount = fn.length;
          break;
        }
      }

      input.value = val.substring(0, start - deleteCount) + val.substring(start);
      const newPos = start - deleteCount;
      input.setSelectionRange(newPos, newPos);
    }
    input.focus();
  }

  function clearDisplay() {
    displayMain.value = '';
    displayExpr.textContent = '';
    isResultDisplayed = false;
    hideError();
  }

  function scrollDisplayToEnd() {
    displayMain.scrollLeft = displayMain.scrollWidth;
  }

  // --- Error Display Utilities ---
  function showError(msg) {
    displayMain.value = msg;
    errorBadge.textContent = msg.toUpperCase();
    errorBadge.style.display = 'inline-block';
    isErrorState = true;
    
    // Trigger vibration-like shake effect
    const container = document.querySelector('.display-container');
    container.classList.add('badge-error');
    setTimeout(() => {
      container.classList.remove('badge-error');
    }, 500);
  }

  function hideError() {
    errorBadge.style.display = 'none';
    isErrorState = false;
  }

  // --- Keyboard Event Handler ---
  function handleKeyboardInput(e) {
    if (isErrorState) {
      hideError();
    }
    
    // Live mapping of keyboard characters into styled characters
    let value = displayMain.value;
    value = value.replace(/\*/g, '×');
    value = value.replace(/\//g, '÷');
    value = value.replace(/-/g, '−'); // Replace standard dash with proper mathematical minus
    
    if (displayMain.value !== value) {
      const cursor = displayMain.selectionStart;
      displayMain.value = value;
      displayMain.setSelectionRange(cursor, cursor);
    }
  }

  function handlePhysicalKeyboard(e) {
    // Ignore keyboard shortcuts if user is doing copy/paste (Ctrl+C, Ctrl+V, etc.)
    if (e.ctrlKey || e.metaKey) return;

    const key = e.key;

    // Add brief active press animation to matching keyboard keys
    let matchedBtn = null;
    if (key >= '0' && key <= '9') {
      matchedBtn = Array.from(document.querySelectorAll('.btn-num')).find(b => b.dataset.val === key);
    } else if (key === '.') {
      matchedBtn = Array.from(document.querySelectorAll('.btn-num')).find(b => b.dataset.val === '.');
    } else if (key === '+') {
      matchedBtn = Array.from(document.querySelectorAll('.btn-op')).find(b => b.dataset.val === '+');
    } else if (key === '-') {
      matchedBtn = Array.from(document.querySelectorAll('.btn-op')).find(b => b.dataset.val === '-');
    } else if (key === '*') {
      matchedBtn = Array.from(document.querySelectorAll('.btn-op')).find(b => b.dataset.val === '*');
    } else if (key === '/') {
      matchedBtn = Array.from(document.querySelectorAll('.btn-op')).find(b => b.dataset.val === '/');
    } else if (key === '(' || key === ')') {
      matchedBtn = Array.from(document.querySelectorAll('.btn-op')).find(b => b.dataset.val === key);
    } else if (key === 'Enter' || key === '=') {
      matchedBtn = document.getElementById('key-equal');
    } else if (key === 'Backspace') {
      matchedBtn = document.getElementById('key-delete');
    } else if (key === 'Escape') {
      matchedBtn = document.getElementById('key-clear');
    }

    if (matchedBtn) {
      matchedBtn.classList.add('pressed');
      setTimeout(() => matchedBtn.classList.remove('pressed'), 100);
    }

    // Input handlers
    if (key === 'Enter') {
      e.preventDefault();
      calculateResult();
    } else if (key === 'Escape') {
      e.preventDefault();
      clearDisplay();
    }
  }

  // --- History Service ---
  function saveHistoryItem(expr, result) {
    let history = JSON.parse(localStorage.getItem('calc-history')) || [];
    // Keep max 30 items
    history.unshift({ expr, result });
    if (history.length > 30) history.pop();
    
    localStorage.setItem('calc-history', JSON.stringify(history));
    loadHistory();
  }

  function loadHistory() {
    const history = JSON.parse(localStorage.getItem('calc-history')) || [];
    if (history.length === 0) {
      historyList.innerHTML = '<div class="empty-history">No calculations yet</div>';
      return;
    }

    historyList.innerHTML = history.map((item, idx) => `
      <div class="history-item" data-expr="${item.expr}" data-result="${item.result}">
        <span class="history-item-expr">${item.expr}</span>
        <span class="history-item-result">${item.result}</span>
      </div>
    `).join('');

    // Attach click events to load items
    document.querySelectorAll('.history-item').forEach(item => {
      item.addEventListener('click', (e) => {
        const expr = e.currentTarget.dataset.expr;
        displayMain.value = expr;
        displayExpr.textContent = '';
        isResultDisplayed = false;
        hideError();
        historyDrawer.classList.remove('open');
        displayMain.focus();
      });
    });
  }

  function clearHistory() {
    localStorage.removeItem('calc-history');
    loadHistory();
  }

  // --- Computational Core (Parser & Compiler) ---
  function calculateResult() {
    const rawExpr = displayMain.value.trim();
    if (rawExpr === '') {
      showError("Empty input");
      return;
    }

    try {
      const sanitized = preprocessExpression(rawExpr);
      const tokens = tokenize(sanitized);
      const parsedAST = parseTokens(tokens);
      const numericResult = evaluateAST(parsedAST, angleMode);

      // Validate result
      if (isNaN(numericResult)) {
        throw new Error("Invalid Input");
      }
      if (!isFinite(numericResult)) {
        throw new Error("Overflow");
      }

      const formattedResult = formatResult(numericResult);
      
      // Save values
      lastAnswer = numericResult;
      displayExpr.textContent = `${rawExpr} =`;
      displayMain.value = formattedResult;
      isResultDisplayed = true;
      hideError();
      
      saveHistoryItem(rawExpr, formattedResult);
    } catch (err) {
      showError(err.message.startsWith("Error:") ? err.message : `Error: ${err.message}`);
    }
  }

  function preprocessExpression(str) {
    // Map human operators to standard mathematical operators
    let expr = str;
    expr = expr.replace(/×/g, '*');
    expr = expr.replace(/÷/g, '/');
    expr = expr.replace(/−/g, '-');
    expr = expr.replace(/π/g, 'pi');
    expr = expr.replace(/²/g, '²');
    expr = expr.replace(/³/g, '³');
    return expr;
  }

  // --- Lexical Analyzer (Tokenizer) ---
  function tokenize(str) {
    const tokens = [];
    let i = 0;
    
    const isDigit = (c) => (c >= '0' && c <= '9');
    const isLetter = (c) => ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z'));

    while (i < str.length) {
      const char = str[i];

      if (char === ' ') {
        i++;
        continue;
      }

      // Check numbers (e.g. 3.14, .5, 1e+5, 2.5e-3)
      if (isDigit(char) || (char === '.' && i + 1 < str.length && isDigit(str[i + 1]))) {
        let numStr = '';
        while (i < str.length && (isDigit(str[i]) || str[i] === '.')) {
          numStr += str[i];
          i++;
        }

        // Check for scientific E-notation
        if (i < str.length && (str[i] === 'e' || str[i] === 'E')) {
          let eStr = str[i];
          let j = i + 1;
          if (j < str.length && (str[j] === '+' || str[j] === '-')) {
            eStr += str[j];
            j++;
          }
          if (j < str.length && isDigit(str[j])) {
            while (j < str.length && isDigit(str[j])) {
              eStr += str[j];
              j++;
            }
            numStr += eStr;
            i = j;
          }
        }

        const parsedVal = parseFloat(numStr);
        if (isNaN(parsedVal)) {
          throw new Error("Invalid number formatting");
        }
        tokens.push({ type: 'NUMBER', value: parsedVal });
        continue;
      }

      // Check functions and constants
      if (isLetter(char)) {
        let word = '';
        while (i < str.length && (isLetter(str[i]) || isDigit(str[i]))) {
          word += str[i];
          i++;
        }

        const lowerWord = word.toLowerCase();
        if (lowerWord === 'pi') {
          tokens.push({ type: 'CONSTANT', value: Math.PI });
        } else if (lowerWord === 'e') {
          tokens.push({ type: 'CONSTANT', value: Math.E });
        } else if (lowerWord === 'ans') {
          tokens.push({ type: 'CONSTANT', value: lastAnswer });
        } else if (['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'ln', 'log', 'sqrt', 'cbrt', 'abs', 'exp'].includes(lowerWord)) {
          tokens.push({ type: 'FUNCTION', value: lowerWord });
        } else {
          throw new Error(`Unknown identifier '${word}'`);
        }
        continue;
      }

      // Bracket parentheses
      if (char === '(') {
        tokens.push({ type: 'LPAREN', value: '(' });
        i++;
        continue;
      }
      if (char === ')') {
        tokens.push({ type: 'RPAREN', value: ')' });
        i++;
        continue;
      }

      // Prefix Sqrt symbol directly
      if (char === '√') {
        tokens.push({ type: 'FUNCTION', value: 'sqrt' });
        i++;
        continue;
      }

      // Postfix operators
      if (char === '²') {
        tokens.push({ type: 'POSTFIX_POWER', value: 2 });
        i++;
        continue;
      }
      if (char === '³') {
        tokens.push({ type: 'POSTFIX_POWER', value: 3 });
        i++;
        continue;
      }

      // Infix Operators & Factorial
      if (['+', '-', '*', '/', '^', '%', '!'].includes(char)) {
        tokens.push({ type: 'OPERATOR', value: char });
        i++;
        continue;
      }

      throw new Error(`Invalid character '${char}'`);
    }

    return insertImplicitMultiplication(tokens);
  }

  // Auto-inserts mathematical multiplication where implicit: e.g. 2pi -> 2 * pi, 2(3) -> 2 * (3)
  function insertImplicitMultiplication(tokens) {
    const result = [];
    for (let i = 0; i < tokens.length; i++) {
      const curr = tokens[i];
      result.push(curr);

      if (i + 1 < tokens.length) {
        const next = tokens[i + 1];
        
        const isCurrPostfix = (curr.type === 'OPERATOR' && curr.value === '!') || 
                              curr.type === 'RPAREN' || 
                              curr.type === 'NUMBER' || 
                              curr.type === 'CONSTANT' ||
                              curr.type === 'POSTFIX_POWER';

        const isNextValue = next.type === 'LPAREN' || 
                            next.type === 'CONSTANT' || 
                            next.type === 'FUNCTION' || 
                            next.type === 'NUMBER';

        if (isCurrPostfix && isNextValue) {
          result.push({ type: 'OPERATOR', value: '*' });
        }
      }
    }
    return result;
  }

  // --- Syntax Analyzer (AST Compiler) ---
  function parseTokens(tokens) {
    let pos = 0;

    const peek = () => (pos < tokens.length ? tokens[pos] : null);
    const consume = (type) => {
      const tok = peek();
      if (tok && tok.type === type) {
        pos++;
        return tok;
      }
      throw new Error(`Mismatched Parentheses`);
    };

    // Precedence hierarchy: Expression -> Term -> Power -> Factor -> Postfix -> Primary
    
    function parseExpression() {
      let node = parseTerm();
      while (true) {
        const tok = peek();
        if (tok && tok.type === 'OPERATOR' && (tok.value === '+' || tok.value === '-')) {
          pos++;
          const right = parseTerm();
          node = { type: 'BINARY', op: tok.value, left: node, right: right };
        } else {
          break;
        }
      }
      return node;
    }

    function parseTerm() {
      let node = parsePower();
      while (true) {
        const tok = peek();
        if (tok && tok.type === 'OPERATOR' && (tok.value === '*' || tok.value === '/' || tok.value === '%')) {
          pos++;
          const right = parsePower();
          node = { type: 'BINARY', op: tok.value, left: node, right: right };
        } else {
          break;
        }
      }
      return node;
    }

    function parsePower() {
      let node = parseFactor();
      const tok = peek();
      if (tok && tok.type === 'OPERATOR' && tok.value === '^') {
        pos++;
        // Right associative
        const right = parsePower();
        node = { type: 'BINARY', op: '^', left: node, right: right };
      }
      return node;
    }

    function parseFactor() {
      const tok = peek();
      if (tok && tok.type === 'OPERATOR' && (tok.value === '+' || tok.value === '-')) {
        pos++;
        const arg = parseFactor();
        return { type: 'UNARY', op: tok.value, value: arg };
      }
      return parsePostfix();
    }

    function parsePostfix() {
      let node = parsePrimary();
      while (true) {
        const tok = peek();
        if (tok && tok.type === 'OPERATOR' && tok.value === '!') {
          pos++;
          node = { type: 'POSTFIX', op: '!', arg: node };
        } else if (tok && tok.type === 'POSTFIX_POWER') {
          pos++;
          node = { type: 'BINARY', op: '^', left: node, right: { type: 'NUMBER', value: tok.value } };
        } else {
          break;
        }
      }
      return node;
    }

    function parsePrimary() {
      const tok = peek();
      if (!tok) {
        throw new Error("Syntax Error");
      }

      if (tok.type === 'NUMBER' || tok.type === 'CONSTANT') {
        pos++;
        return { type: 'NUMBER', value: tok.value };
      }

      if (tok.type === 'FUNCTION') {
        pos++;
        // Parse the function parameter. It must be a primary (e.g. wrapped in parentheses or single number)
        const arg = parsePrimary();
        return { type: 'FUNCTION', name: tok.value, arg: arg };
      }

      if (tok.type === 'LPAREN') {
        pos++;
        const exprNode = parseExpression();
        consume('RPAREN');
        return exprNode;
      }

      throw new Error(`Unexpected symbol '${tok.value}'`);
    }

    const ast = parseExpression();
    if (pos < tokens.length) {
      throw new Error(`Unexpected extra tokens`);
    }
    return ast;
  }

  // --- Computational Evaluator ---
  function evaluateAST(node, mode) {
    if (node.type === 'NUMBER') {
      return node.value;
    }

    if (node.type === 'UNARY') {
      const val = evaluateAST(node.value, mode);
      if (node.op === '+') return val;
      if (node.op === '-') return -val;
      throw new Error("Unknown sign operator");
    }

    if (node.type === 'BINARY') {
      const left = evaluateAST(node.left, mode);
      const right = evaluateAST(node.right, mode);

      switch (node.op) {
        case '+': return left + right;
        case '-': return left - right;
        case '*': return left * right;
        case '/':
          if (Math.abs(right) < 1e-15) {
            throw new Error("Division by Zero");
          }
          return left / right;
        case '%':
          if (Math.abs(right) < 1e-15) {
            throw new Error("Division by Zero");
          }
          return left % right;
        case '^':
          // Check for fractional root of negative numbers e.g. (-4)^0.5 which is complex
          if (left < 0 && !Number.isInteger(right)) {
            throw new Error("Complex Result");
          }
          const powRes = Math.pow(left, right);
          if (isNaN(powRes)) {
            throw new Error("Invalid Input");
          }
          return powRes;
        default:
          throw new Error("Unknown math operation");
      }
    }

    if (node.type === 'POSTFIX') {
      const val = evaluateAST(node.arg, mode);
      if (node.op === '!') {
        return evaluateFactorial(val);
      }
      throw new Error("Unknown postfix action");
    }

    if (node.type === 'FUNCTION') {
      const argVal = evaluateAST(node.arg, mode);

      switch (node.name) {
        case 'sin':
          return cleanTrigResult(Math.sin(degToRad(argVal, mode)));
        case 'cos':
          return cleanTrigResult(Math.cos(degToRad(argVal, mode)));
        case 'tan':
          // Check tan(90) undefined conditions
          if (mode === 'DEG' && Math.abs((Math.abs(argVal) % 180) - 90) < 1e-10) {
            throw new Error("Tan Undefined");
          }
          return cleanTrigResult(Math.tan(degToRad(argVal, mode)));
        case 'asin':
          if (argVal < -1 || argVal > 1) {
            throw new Error("Domain Error");
          }
          return radToDeg(Math.asin(argVal), mode);
        case 'acos':
          if (argVal < -1 || argVal > 1) {
            throw new Error("Domain Error");
          }
          return radToDeg(Math.acos(argVal), mode);
        case 'atan':
          return radToDeg(Math.atan(argVal), mode);
        case 'ln':
          if (argVal <= 0) {
            throw new Error("Log Error");
          }
          return Math.log(argVal);
        case 'log':
          if (argVal <= 0) {
            throw new Error("Log Error");
          }
          return Math.log10(argVal);
        case 'sqrt':
          if (argVal < 0) {
            throw new Error("Invalid Input"); // Sqrt negative number
          }
          return Math.sqrt(argVal);
        case 'cbrt':
          return Math.cbrt(argVal);
        case 'abs':
          return Math.abs(argVal);
        case 'exp':
          return Math.exp(argVal);
        default:
          throw new Error(`Unsupported math function '${node.name}'`);
      }
    }

    throw new Error("Corrupted AST Node");
  }

  function degToRad(val, mode) {
    return mode === 'DEG' ? (val * Math.PI) / 180 : val;
  }

  function radToDeg(val, mode) {
    return mode === 'DEG' ? (val * 180) / Math.PI : val;
  }

  // Trims typical javascript floating point noise for trig computations (e.g. sin(pi) should be 0, not 1.2e-16)
  function cleanTrigResult(val) {
    return Math.abs(val) < 1e-15 ? 0 : val;
  }

  function evaluateFactorial(n) {
    if (n < 0) {
      throw new Error("Invalid Factorial");
    }
    if (!Number.isInteger(n)) {
      throw new Error("Integer required");
    }
    if (n > 170) {
      throw new Error("Overflow");
    }
    let res = 1;
    for (let i = 2; i <= n; i++) {
      res *= i;
    }
    return res;
  }

  function formatResult(num) {
    if (typeof num !== 'number' || isNaN(num)) return "Error";
    if (!isFinite(num)) return "Overflow";

    // Format scientific notation for extremely large or small numbers
    const absVal = Math.abs(num);
    if (absVal > 1e14 || (absVal < 1e-9 && absVal > 0)) {
      return num.toExponential(10).replace(/e\+?/i, 'e');
    }

    // Handle standard decimals: limit floating point noise
    let resStr = num.toString();
    if (resStr.includes('.') && !resStr.includes('e')) {
      let rounded = parseFloat(num.toFixed(12));
      return rounded.toString();
    }
    return resStr;
  }

  // --- Automated Self Tests ---
  function runSelfTests() {
    console.log("%c▲ AETHERCALC SELF-TESTING SUITE INITIALIZED ▲", "color: #06b6d4; font-weight: bold; font-size: 13px;");
    const tests = [
      { expr: "5 + 3 * 2", expected: "11" },
      { expr: "2^3", expected: "8" },
      { expr: "(2 + 3) * 4", expected: "20" },
      { expr: "5 ÷ 0", expected: "Error: Division by Zero" },
      { expr: "√(-4)", expected: "Error: Invalid Input" },
      { expr: "5!", expected: "120" },
      { expr: "(-2)!", expected: "Error: Invalid Factorial" },
      { expr: "2.5!", expected: "Error: Integer required" },
      { expr: "2pi", expected: (2 * Math.PI).toString() }, // Test implicit multiplication
      { expr: "sin(90)", expected: "1" }, // DEG Mode test
      { expr: "log(100)", expected: "2" },
      { expr: "ln(e)", expected: "1" },
      { expr: "10^(3)", expected: "1000" }
    ];

    let passedCount = 0;
    tests.forEach((t, index) => {
      try {
        const sanitized = preprocessExpression(t.expr);
        const tokens = tokenize(sanitized);
        const parsed = parseTokens(tokens);
        const resultVal = evaluateAST(parsed, 'DEG');
        const formatted = formatResult(resultVal);

        // Check if output matches expected value
        const matches = (formatted === t.expected || 
                        (typeof resultVal === 'number' && Math.abs(parseFloat(formatted) - parseFloat(t.expected)) < 1e-9));

        if (matches) {
          console.log(`%c✓ Test #${index + 1} Passed: "${t.expr}" === ${formatted}`, "color: #10b981;");
          passedCount++;
        } else {
          console.error(`✗ Test #${index + 1} FAILED: "${t.expr}". Expected: ${t.expected}, Got: ${formatted}`);
        }
      } catch (err) {
        const errMsg = err.message.startsWith("Error:") ? err.message : `Error: ${err.message}`;
        if (errMsg === t.expected) {
          console.log(`%c✓ Test #${index + 1} Passed (Expected Error): "${t.expr}" === "${errMsg}"`, "color: #10b981;");
          passedCount++;
        } else {
          console.error(`✗ Test #${index + 1} FAILED with unexpected error: "${t.expr}". Expected: "${t.expected}", Got: "${errMsg}"`);
        }
      }
    });

    console.log(`%cSelf-Test Summary: ${passedCount}/${tests.length} tests passed successfully.`, "font-weight: bold;");
  }
});
