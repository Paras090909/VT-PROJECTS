#!/usr/bin/env python3
"""
GUI-Based Calculator using Python and PyQt5.
Author: Antigravity AI Pair Programmer
Description: A highly polished standard and scientific calculator application featuring:
  - Responsive layouts
  - Custom Dark and Light Themes
  - Continuous evaluation and validation
  - Memory functions (M+, M-, MR, MC)
  - Scientific functions (sin, cos, tan, log, ln, square, sqrt, power, parentheses)
  - Full keyboard event bindings
  - Built-in error handling (e.g. Division by zero, domain errors)
"""

import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLineEdit, QPushButton, QLabel, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QColor, QPen

# ==========================================
# QSS STYLE SHEETS
# ==========================================

DARK_STYLESHEET = """
QMainWindow {
    background-color: #1a1b20;
}

QWidget {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    color: #ffffff;
}

#DisplayFrame {
    background-color: #111215;
    border: 1px solid #25262c;
    border-radius: 12px;
}

#HistoryLabel {
    color: #7a7c85;
    font-size: 13px;
    font-weight: normal;
    background: transparent;
    border: none;
}

#DisplayInput {
    color: #ffffff;
    font-size: 30px;
    font-weight: bold;
    background: transparent;
    border: none;
}

#MemoryLabel {
    color: #14b8a6;
    font-size: 11px;
    font-weight: bold;
    background: #112d2a;
    border: 1px solid #14b8a6;
    border-radius: 4px;
    padding: 2px 6px;
}

QPushButton {
    background-color: #23242a;
    border: 1px solid #2e3038;
    border-radius: 10px;
    color: #ffffff;
    padding: 12px;
    font-size: 16px;
    font-weight: 500;
    min-height: 48px;
}

QPushButton:hover {
    background-color: #31333c;
    border-color: #40434f;
}

QPushButton:pressed {
    background-color: #18191d;
}

/* Custom class overrides */
QPushButton[class="NumberButton"] {
    background-color: #23242a;
}

QPushButton[class="OperatorButton"] {
    background-color: #3b2075;
    border: 1px solid #4a2894;
    color: #c084fc;
    font-size: 18px;
    font-weight: bold;
}

QPushButton[class="OperatorButton"]:hover {
    background-color: #4a2894;
    color: #d8b4fe;
}

QPushButton[class="OperatorButton"]:pressed {
    background-color: #2b1757;
}

QPushButton[class="EqualsButton"] {
    background-color: #f97316;
    border: 1px solid #ea580c;
    color: #ffffff;
    font-size: 20px;
    font-weight: bold;
}

QPushButton[class="EqualsButton"]:hover {
    background-color: #fb923c;
}

QPushButton[class="EqualsButton"]:pressed {
    background-color: #c2410c;
}

QPushButton[class="SpecialButton"] {
    background-color: #7f1d1d;
    border: 1px solid #991b1b;
    color: #fca5a5;
    font-weight: bold;
}

QPushButton[class="SpecialButton"]:hover {
    background-color: #991b1b;
    color: #fecaca;
}

QPushButton[class="SpecialButton"]:pressed {
    background-color: #450a0a;
}

QPushButton[class="SciButton"] {
    background-color: #1e293b;
    border: 1px solid #334155;
    color: #38bdf8;
    font-size: 13px;
    font-weight: bold;
}

QPushButton[class="SciButton"]:hover {
    background-color: #334155;
    color: #7dd3fc;
}

QPushButton[class="SciButton"]:pressed {
    background-color: #0f172a;
}

#HeaderButton {
    background-color: #23242a;
    border: 1px solid #2e3038;
    border-radius: 6px;
    color: #94a3b8;
    font-size: 12px;
    padding: 6px 12px;
    min-height: 28px;
}

#HeaderButton:hover {
    background-color: #31333c;
    color: #ffffff;
}

#HeaderButton:checked {
    background-color: #6366f1;
    border-color: #4f46e5;
    color: #ffffff;
}
"""

LIGHT_STYLESHEET = """
QMainWindow {
    background-color: #f1f5f9;
}

QWidget {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    color: #0f172a;
}

#DisplayFrame {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
}

#HistoryLabel {
    color: #64748b;
    font-size: 13px;
    font-weight: normal;
    background: transparent;
    border: none;
}

#DisplayInput {
    color: #0f172a;
    font-size: 30px;
    font-weight: bold;
    background: transparent;
    border: none;
}

#MemoryLabel {
    color: #0f766e;
    font-size: 11px;
    font-weight: bold;
    background: #ccfbf1;
    border: 1px solid #0f766e;
    border-radius: 4px;
    padding: 2px 6px;
}

QPushButton {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    color: #0f172a;
    padding: 12px;
    font-size: 16px;
    font-weight: 500;
    min-height: 48px;
}

QPushButton:hover {
    background-color: #f8fafc;
    border-color: #94a3b8;
}

QPushButton:pressed {
    background-color: #e2e8f0;
}

/* Custom class overrides */
QPushButton[class="NumberButton"] {
    background-color: #ffffff;
}

QPushButton[class="OperatorButton"] {
    background-color: #e0e7ff;
    border: 1px solid #c7d2fe;
    color: #4f46e5;
    font-size: 18px;
    font-weight: bold;
}

QPushButton[class="OperatorButton"]:hover {
    background-color: #c7d2fe;
    color: #3730a3;
}

QPushButton[class="OperatorButton"]:pressed {
    background-color: #a5b4fc;
}

QPushButton[class="EqualsButton"] {
    background-color: #2563eb;
    border: 1px solid #1d4ed8;
    color: #ffffff;
    font-size: 20px;
    font-weight: bold;
}

QPushButton[class="EqualsButton"]:hover {
    background-color: #3b82f6;
}

QPushButton[class="EqualsButton"]:pressed {
    background-color: #1e3a8a;
}

QPushButton[class="SpecialButton"] {
    background-color: #fee2e2;
    border: 1px solid #fca5a5;
    color: #991b1b;
    font-weight: bold;
}

QPushButton[class="SpecialButton"]:hover {
    background-color: #fca5a5;
    color: #7f1d1d;
}

QPushButton[class="SpecialButton"]:pressed {
    background-color: #fecaca;
}

QPushButton[class="SciButton"] {
    background-color: #f0fdf4;
    border: 1px solid #bbf7d0;
    color: #15803d;
    font-size: 13px;
    font-weight: bold;
}

QPushButton[class="SciButton"]:hover {
    background-color: #bbf7d0;
    color: #166534;
}

QPushButton[class="SciButton"]:pressed {
    background-color: #dcfce7;
}

#HeaderButton {
    background-color: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    color: #475569;
    font-size: 12px;
    padding: 6px 12px;
    min-height: 28px;
}

#HeaderButton:hover {
    background-color: #f8fafc;
    color: #0f172a;
}

#HeaderButton:checked {
    background-color: #2563eb;
    border-color: #1d4ed8;
    color: #ffffff;
}
"""

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def format_result(value, expression_had_decimal):
    """
    Formats arithmetic results nicely:
    - If result is mathematically a whole number (e.g. 16.0), and the user's expression
      involved decimals, preserve .0 representation (e.g., '16.0') as standard for decimal inputs.
    - Otherwise, strip the decimal point and return as an integer string (e.g., '25').
    - If floating point is non-integral, formats with up to 10 significant digits.
    """
    try:
        val = float(value)
        if val.is_integer():
            if expression_had_decimal:
                return f"{val:.1f}"
            else:
                return str(int(val))
        # Strip trailing zeros in floating precision and limit representation length
        formatted = f"{val:.10g}"
        return formatted
    except (ValueError, TypeError):
        return str(value)


def create_app_icon():
    """Draws a beautiful self-contained application icon using QPixmap and QPainter."""
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Background
    painter.setBrush(QColor("#4f46e5"))  # Premium violet/indigo
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(4, 4, 56, 56, 12, 12)
    
    # Display Outline
    painter.setPen(QPen(QColor("#ffffff"), 3))
    painter.setBrush(Qt.NoBrush)
    painter.drawRoundedRect(12, 14, 40, 12, 2, 2)
    
    # Small buttons
    painter.setBrush(QColor("#ffffff"))
    painter.setPen(Qt.NoPen)
    painter.drawRect(16, 32, 6, 6)
    painter.drawRect(26, 32, 6, 6)
    painter.drawRect(36, 32, 6, 6)
    
    painter.drawRect(16, 42, 6, 6)
    painter.drawRect(26, 42, 6, 6)
    painter.drawRect(36, 42, 6, 6)
    
    # Action key (accent color orange)
    painter.setBrush(QColor("#ea580c"))
    painter.drawRect(46, 32, 6, 16)
    
    painter.end()
    return QIcon(pixmap)


# ==========================================
# MAIN CALCULATOR APPLICATION WINDOW
# ==========================================

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Premium Calculator")
        self.setWindowIcon(create_app_icon())
        
        # State variables
        self.expression_list = []
        self.current_operand = ""
        self.memory_value = 0.0
        self.should_clear_on_next_digit = False
        self.is_showing_scientific = False
        self.current_theme = "dark"
        
        self.init_ui()
        self.apply_theme()
        
    def init_ui(self):
        # Set up central widget and layouts
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)
        
        # 1. Dual-Display Area
        display_frame = QFrame()
        display_frame.setObjectName("DisplayFrame")
        display_layout = QVBoxLayout(display_frame)
        display_layout.setContentsMargins(12, 12, 12, 12)
        display_layout.setSpacing(6)
        
        # Memory status indicator and History row
        display_top_layout = QHBoxLayout()
        
        self.memory_badge = QLabel("M")
        self.memory_badge.setObjectName("MemoryLabel")
        self.memory_badge.setVisible(False)
        display_top_layout.addWidget(self.memory_badge)
        
        display_top_layout.addStretch()
        
        self.history_label = QLabel("")
        self.history_label.setObjectName("HistoryLabel")
        self.history_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        display_top_layout.addWidget(self.history_label)
        
        display_layout.addLayout(display_top_layout)
        
        # Main Display Input
        self.display_input = QLineEdit("0")
        self.display_input.setObjectName("DisplayInput")
        self.display_input.setReadOnly(True)
        self.display_input.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        display_layout.addWidget(self.display_input)
        
        main_layout.addWidget(display_frame)
        
        # 2. Top Header Options Panel
        header_layout = QHBoxLayout()
        
        self.sci_toggle_btn = QPushButton("Scientific Mode")
        self.sci_toggle_btn.setObjectName("HeaderButton")
        self.sci_toggle_btn.setCheckable(True)
        self.sci_toggle_btn.setFocusPolicy(Qt.NoFocus)
        self.sci_toggle_btn.clicked.connect(self.toggle_scientific)
        header_layout.addWidget(self.sci_toggle_btn)
        
        header_layout.addStretch()
        
        self.theme_toggle_btn = QPushButton("Theme: Dark")
        self.theme_toggle_btn.setObjectName("HeaderButton")
        self.theme_toggle_btn.setFocusPolicy(Qt.NoFocus)
        self.theme_toggle_btn.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_toggle_btn)
        
        main_layout.addLayout(header_layout)
        
        # 3. Keyboards Container
        self.keyboards_container = QWidget()
        keyboards_layout = QHBoxLayout(self.keyboards_container)
        keyboards_layout.setContentsMargins(0, 0, 0, 0)
        keyboards_layout.setSpacing(12)
        
        # A. Standard Keypad
        self.standard_keypad = QWidget()
        standard_layout = QGridLayout(self.standard_keypad)
        standard_layout.setContentsMargins(0, 0, 0, 0)
        standard_layout.setSpacing(8)
        
        standard_buttons = [
            ['C', '⌫', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['±', '0', '.', '=']
        ]
        
        for r_idx, row in enumerate(standard_buttons):
            for c_idx, text in enumerate(row):
                btn = QPushButton(text)
                btn.setFocusPolicy(Qt.NoFocus)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                
                # Class mapping for custom style sheet bindings
                if text in ['C', '⌫']:
                    btn.setProperty('class', 'SpecialButton')
                elif text in ['÷', '×', '-', '+', '%']:
                    btn.setProperty('class', 'OperatorButton')
                elif text == '=':
                    btn.setProperty('class', 'EqualsButton')
                else:
                    btn.setProperty('class', 'NumberButton')
                
                standard_layout.addWidget(btn, r_idx, c_idx)
                btn.clicked.connect(lambda _, t=text: self.handle_button(t))
                
        keyboards_layout.addWidget(self.standard_keypad)
        
        # B. Scientific Keypad (Initially hidden)
        self.scientific_keypad = QWidget()
        self.scientific_keypad.setVisible(False)
        sci_layout = QGridLayout(self.scientific_keypad)
        sci_layout.setContentsMargins(0, 0, 0, 0)
        sci_layout.setSpacing(8)
        
        sci_buttons = [
            ['MC', 'MR', 'M+', 'M-'],
            ['x²', '√x', 'xʸ', '1/x'],
            ['sin', 'cos', 'tan', 'π'],
            ['log', 'ln', '(', ')']
        ]
        
        for r_idx, row in enumerate(sci_buttons):
            for c_idx, text in enumerate(row):
                btn = QPushButton(text)
                btn.setFocusPolicy(Qt.NoFocus)
                btn.setProperty('class', 'SciButton')
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                
                sci_layout.addWidget(btn, r_idx, c_idx)
                btn.clicked.connect(lambda _, t=text: self.handle_button(t))
                
        keyboards_layout.addWidget(self.scientific_keypad)
        
        main_layout.addWidget(self.keyboards_container)
        
        # Adjust layout proportions
        main_layout.setStretch(0, 1)  # Display screen
        main_layout.setStretch(2, 5)  # Keypads area
        
        # Fix starting size
        self.setFixedSize(380, 520)

    # ==========================================
    # VIEW ACTIONS
    # ==========================================
    
    def toggle_scientific(self):
        """Shows or hides the scientific sidebar panel and resizes the window accordingly."""
        self.is_showing_scientific = self.sci_toggle_btn.isChecked()
        self.scientific_keypad.setVisible(self.is_showing_scientific)
        
        # Adjust window sizing
        if self.is_showing_scientific:
            self.setMaximumSize(16777215, 16777215)
            self.setFixedSize(740, 520)
        else:
            self.setMaximumSize(16777215, 16777215)
            self.setFixedSize(380, 520)

    def toggle_theme(self):
        """Switches between Dark and Light mode styling."""
        if self.current_theme == "dark":
            self.current_theme = "light"
            self.theme_toggle_btn.setText("Theme: Light")
        else:
            self.current_theme = "dark"
            self.theme_toggle_btn.setText("Theme: Dark")
        self.apply_theme()
        
    def apply_theme(self):
        """Applies the current QSS stylesheet to the application."""
        if self.current_theme == "dark":
            self.setStyleSheet(DARK_STYLESHEET)
        else:
            self.setStyleSheet(LIGHT_STYLESHEET)

    # ==========================================
    # LOGIC CONTROLLER / DISPATCHER
    # ==========================================

    def handle_button(self, text):
        """Core coordinator that dispatches button clicks to their specific handlers."""
        display_val = self.display_input.text()
        
        # If there is currently an error shown, only allow clearing
        if "Error" in display_val and text != 'C':
            return
            
        if text.isdigit():
            self.handle_digit(text)
        elif text == '.':
            self.handle_decimal()
        elif text == '±':
            self.handle_sign_toggle()
        elif text in ['+', '-', '×', '÷', 'xʸ']:
            self.handle_operator(text)
        elif text == '%':
            self.handle_percentage()
        elif text == '=':
            self.evaluate_expression()
        elif text == '⌫':
            self.handle_backspace()
        elif text == 'C':
            self.clear_all()
        elif text in ['x²', '√x', '1/x', 'sin', 'cos', 'tan', 'log', 'ln']:
            self.handle_unary_operator(text)
        elif text in ['π', 'e']:
            self.handle_constant(text)
        elif text in ['(', ')']:
            self.handle_parenthesis(text)
        elif text in ['MC', 'MR', 'M+', 'M-']:
            self.handle_memory(text)

    # ==========================================
    # DETAILED BUTTON HANDLERS
    # ==========================================

    def handle_digit(self, digit):
        """Appends digits to the current operand buffer, preventing leading zero sequences."""
        if self.should_clear_on_next_digit:
            self.current_operand = digit
            self.should_clear_on_next_digit = False
        else:
            if self.current_operand == "0":
                self.current_operand = digit
            else:
                self.current_operand += digit
                
        self.display_input.setText(self.current_operand)

    def handle_decimal(self):
        """Appends a decimal dot to the current operand if it doesn't already contain one."""
        if self.should_clear_on_next_digit:
            self.current_operand = "0."
            self.should_clear_on_next_digit = False
        else:
            if "." not in self.current_operand:
                if not self.current_operand:
                    self.current_operand = "0."
                else:
                    self.current_operand += "."
                    
        self.display_input.setText(self.current_operand)

    def handle_sign_toggle(self):
        """Toggles the sign (+/-) of the current operand or the active result."""
        if self.current_operand:
            if self.current_operand.startswith("-"):
                self.current_operand = self.current_operand[1:]
            else:
                self.current_operand = "-" + self.current_operand
            self.display_input.setText(self.current_operand)
        else:
            # Toggle sign on the calculated value in display
            display_val = self.display_input.text()
            if display_val not in ["0", "Error: Div by 0", "Error: Invalid Input"]:
                if display_val.startswith("-"):
                    self.current_operand = display_val[1:]
                else:
                    self.current_operand = "-" + display_val
                self.display_input.setText(self.current_operand)

    def handle_operator(self, op):
        """
        Pushes the current operand and operator to the expression stack.
        Supports continuous calculations (operator chaining) and operator replacement.
        """
        # If operand is active, commit it to history first
        if self.current_operand:
            if self.current_operand.endswith('.'):
                self.current_operand = self.current_operand[:-1]
                
            self.expression_list.append(self.current_operand)
            self.current_operand = ""
            
            # Evaluate immediately if we already have a binary expression
            # This makes running totals update continuously (e.g. 10 + 20 + -> 30 +)
            if len(self.expression_list) >= 3:
                running_val = self.evaluate_running_expression()
                if "Error" in str(running_val):
                    self.display_input.setText(running_val)
                    self.expression_list = []
                    self.should_clear_on_next_digit = True
                    return
                else:
                    self.display_input.setText(running_val)
                    self.expression_list = [running_val]
            
            self.expression_list.append(op)
            self.should_clear_on_next_digit = False
        else:
            # If operator is clicked without a typed number
            if self.expression_list:
                last_token = self.expression_list[-1]
                # If last token was another operator, replace it
                if last_token in ['+', '-', '×', '÷', 'xʸ']:
                    self.expression_list[-1] = op
                else:
                    self.expression_list.append(op)
            else:
                # Use current displayed number as first operand
                val = self.display_input.text()
                if val not in ["Error: Div by 0", "Error: Invalid Input"]:
                    self.expression_list = [val, op]
                    
        self.update_history_display()

    def handle_percentage(self):
        """
        Applies standard percentage calculations:
        - In binary contexts (e.g., '100 + 10%'), calculates 10% of 100 (= 10).
        - In single operand contexts (e.g., '50%'), calculates 50 / 100 (= 0.5).
        """
        display_val = self.display_input.text()
        try:
            val = float(display_val)
        except ValueError:
            return
            
        percent_val = 0.0
        # If there is a previous operand in list (e.g. ['100', '+']), calculate relative percentage
        if len(self.expression_list) >= 2:
            try:
                prev_val = float(self.expression_list[-2])
                percent_val = (prev_val * val) / 100.0
            except ValueError:
                percent_val = val / 100.0
        else:
            percent_val = val / 100.0
            
        has_decimal = '.' in display_val or percent_val % 1 != 0
        formatted_val = format_result(percent_val, has_decimal)
        self.current_operand = formatted_val
        self.display_input.setText(formatted_val)

    def handle_unary_operator(self, op):
        """Applies mathematical unary functions directly to the active displayed value."""
        display_val = self.display_input.text()
        
        try:
            val = float(display_val)
        except ValueError:
            return
            
        res = 0.0
        op_repr = ""
        val_formatted = format_result(val, '.' in display_val)
        
        try:
            if op == 'x²':
                res = val ** 2
                op_repr = f"sqr({val_formatted})"
            elif op == '√x':
                if val < 0:
                    raise ValueError("Negative square root")
                res = math.sqrt(val)
                op_repr = f"√({val_formatted})"
            elif op == '1/x':
                if val == 0:
                    raise ZeroDivisionError("1/0 reciprocal")
                res = 1 / val
                op_repr = f"recip({val_formatted})"
            elif op == 'sin':
                res = math.sin(math.radians(val))
                op_repr = f"sin({val_formatted})"
            elif op == 'cos':
                res = math.cos(math.radians(val))
                op_repr = f"cos({val_formatted})"
            elif op == 'tan':
                # Check for odd multiples of 90 degrees (tan is undefined)
                if abs((val - 90) % 180) < 1e-9:
                    raise ValueError("Tan undefined")
                res = math.tan(math.radians(val))
                op_repr = f"tan({val_formatted})"
            elif op == 'log':
                if val <= 0:
                    raise ValueError("Log domain error")
                res = math.log10(val)
                op_repr = f"log({val_formatted})"
            elif op == 'ln':
                if val <= 0:
                    raise ValueError("Ln domain error")
                res = math.log(val)
                op_repr = f"ln({val_formatted})"
                
            formatted_res = format_result(res, '.' in display_val or isinstance(res, float))
            self.current_operand = formatted_res
            self.display_input.setText(formatted_res)
            
            # Show the function call inside history visually
            if self.expression_list and self.expression_list[-1] not in ['+', '-', '×', '÷', 'xʸ', '(']:
                self.expression_list[-1] = op_repr
            
            running_history = " ".join(self.expression_list) + " " + op_repr
            self.history_label.setText(running_history.strip())
            
        except ZeroDivisionError:
            self.display_input.setText("Error: Div by 0")
            self.expression_list = []
            self.current_operand = ""
            self.should_clear_on_next_digit = True
        except ValueError:
            self.display_input.setText("Error: Invalid Input")
            self.expression_list = []
            self.current_operand = ""
            self.should_clear_on_next_digit = True

    def handle_constant(self, const):
        """Appends mathematical constants to the active operand."""
        if const == 'π':
            val = math.pi
        elif const == 'e':
            val = math.e
        else:
            return
            
        self.current_operand = format_result(val, True)
        self.display_input.setText(self.current_operand)
        self.should_clear_on_next_digit = False

    def handle_parenthesis(self, paren):
        """Handles parenthesis injection while auto-inserting multiplication signs where required."""
        if paren == '(':
            if self.current_operand:
                self.expression_list.append(self.current_operand)
                self.expression_list.append('×')
                self.current_operand = ""
            elif self.expression_list and self.expression_list[-1] not in ['+', '-', '×', '÷', 'xʸ', '(']:
                self.expression_list.append('×')
            self.expression_list.append('(')
        else:  # paren == ')'
            open_count = self.expression_list.count('(')
            close_count = self.expression_list.count(')')
            if open_count > close_count:
                if self.current_operand:
                    if self.current_operand.endswith('.'):
                        self.current_operand = self.current_operand[:-1]
                    self.expression_list.append(self.current_operand)
                    self.current_operand = ""
                self.expression_list.append(')')
                
        self.update_history_display()

    def handle_memory(self, op):
        """Performs memory storage, addition, subtraction, recall, and clearance actions."""
        display_val = self.display_input.text()
        
        try:
            val = float(display_val)
        except ValueError:
            return
            
        if op == 'MC':
            self.memory_value = 0.0
            self.memory_badge.setVisible(False)
        elif op == 'MR':
            formatted_mem = format_result(self.memory_value, True)
            self.current_operand = formatted_mem
            self.display_input.setText(formatted_mem)
            self.should_clear_on_next_digit = False
        elif op == 'M+':
            self.memory_value += val
            self.memory_badge.setVisible(self.memory_value != 0.0)
            self.should_clear_on_next_digit = True
        elif op == 'M-':
            self.memory_value -= val
            self.memory_badge.setVisible(self.memory_value != 0.0)
            self.should_clear_on_next_digit = True

    def handle_backspace(self):
        """Removes the last typed digit from the active buffer."""
        if self.should_clear_on_next_digit:
            self.clear_all()
            return
            
        if self.current_operand:
            self.current_operand = self.current_operand[:-1]
            if not self.current_operand or self.current_operand == "-":
                self.current_operand = "0"
            self.display_input.setText(self.current_operand)

    def clear_all(self):
        """Full reset of the calculator's state, displays, and internal calculations."""
        self.expression_list = []
        self.current_operand = ""
        self.display_input.setText("0")
        self.history_label.setText("")
        self.should_clear_on_next_digit = False

    # ==========================================
    # EVALUATION LOGIC
    # ==========================================

    def evaluate_running_expression(self):
        """Evaluates the active state representation to return the running total."""
        has_decimal = any('.' in token for token in self.expression_list)
        res = self.safe_eval(self.expression_list)
        if isinstance(res, (int, float)):
            return format_result(res, has_decimal)
        return res

    def evaluate_expression(self):
        """Triggered by the '=' button. Performs final evaluation of the stack."""
        if self.current_operand:
            if self.current_operand.endswith('.'):
                self.current_operand = self.current_operand[:-1]
            self.expression_list.append(self.current_operand)
            self.current_operand = ""
            
        if not self.expression_list:
            return
            
        # Remove trailing operators if present
        if self.expression_list[-1] in ['+', '-', '×', '÷', 'xʸ']:
            self.expression_list.pop()
            
        if not self.expression_list:
            self.history_label.setText("")
            return
            
        has_decimal = any('.' in token for token in self.expression_list)
        
        # Display history equation
        history_text = " ".join(self.expression_list) + " ="
        self.history_label.setText(history_text)
        
        # Evaluate
        res = self.safe_eval(self.expression_list)
        if isinstance(res, (int, float)):
            formatted_res = format_result(res, has_decimal)
            self.display_input.setText(formatted_res)
            self.should_clear_on_next_digit = True
        else:
            self.display_input.setText(res)  # Shows error message (e.g. Div by zero)
            self.should_clear_on_next_digit = True
            
        self.expression_list = []

    def safe_eval(self, expr_list):
        """
        Parses list elements and evaluates them safely.
        Restricts standard python scope variables to math domain values.
        """
        processed_tokens = []
        for token in expr_list:
            if token == '×':
                processed_tokens.append('*')
            elif token == '÷':
                processed_tokens.append('/')
            elif token == 'xʸ':
                processed_tokens.append('**')
            else:
                processed_tokens.append(token)
                
        expression_str = " ".join(processed_tokens)
        
        try:
            # Define scope for the safe evaluation
            local_scope = {
                "math": math,
                "pi": math.pi,
                "e": math.e,
                "sin": lambda x: math.sin(math.radians(x)),
                "cos": lambda x: math.cos(math.radians(x)),
                "tan": lambda x: math.tan(math.radians(x)),
                "log": lambda x: math.log10(x),
                "ln": lambda x: math.log(x),
                "sqrt": lambda x: math.sqrt(x)
            }
            # Evaluate under sandboxed context (no builtins)
            result = eval(expression_str, {"__builtins__": None}, local_scope)
            return result
        except ZeroDivisionError:
            return "Error: Div by 0"
        except (ValueError, OverflowError):
            return "Error: Invalid Input"
        except Exception:
            return "Error: Invalid Input"

    def update_history_display(self):
        """Updates the history display label above the input screen."""
        history_str = " ".join(self.expression_list)
        self.history_label.setText(history_str)

    # ==========================================
    # KEYBOARD SHORTCUT EVENT CAPTURING
    # ==========================================

    def keyPressEvent(self, event):
        """Binds standard keyboard and numpad keys to calculator actions."""
        key = event.key()
        text = event.text()
        
        # Digit keys
        if Qt.Key_0 <= key <= Qt.Key_9:
            self.handle_button(text)
        # Decimal dot
        elif key == Qt.Key_Period or text == '.':
            self.handle_button('.')
        # Plus operator
        elif key == Qt.Key_Plus or text == '+':
            self.handle_button('+')
        # Minus operator
        elif key == Qt.Key_Minus or text == '-':
            self.handle_button('-')
        # Multiplication operator
        elif key == Qt.Key_Asterisk or text == '*':
            self.handle_button('×')
        # Division operator
        elif key == Qt.Key_Slash or text == '/':
            self.handle_button('÷')
        # Equals / Evaluate
        elif key in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Equal) or text == '=':
            self.handle_button('=')
        # Backspace
        elif key == Qt.Key_Backspace:
            self.handle_button('⌫')
        # Escape / Clear
        elif key == Qt.Key_Escape:
            self.handle_button('C')
        # Percent
        elif text == '%':
            self.handle_button('%')
        # Exponentiation power symbol (Shift + 6)
        elif text == '^':
            self.handle_button('xʸ')
        # Parentheses
        elif text == '(':
            self.handle_button('(')
        elif text == ')':
            self.handle_button(')')
        else:
            # Let standard event bubble up if not handled
            super().keyPressEvent(event)


# ==========================================
# MAIN EXECUTION ROUTINE
# ==========================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Enable High DPI scaling for crisp visuals on modern displays
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    calc = CalculatorApp()
    calc.show()
    sys.exit(app.exec_())
