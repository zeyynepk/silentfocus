# styles/themes.py

WORK_THEME = """
QWidget {
    background-color: #0b1220;
    color: #e5e7eb;
    font-family: 'Inter', 'Arial';
}

QLabel#label_time {
    font-size: 64px;
    font-weight: 800;
    color: #f8fafc;
}

QLabel#session_label {
    font-size: 14px;
    color: #94a3b8;
}

QPushButton {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 14px 22px;
    min-width: 100px;
}

QPushButton:hover {
    background-color: #334155;
}

QPushButton:disabled {
    background-color: #475569;
    color: #cbd5e1;
}

QWidget#hero_card {
    background-color: rgba(255, 255, 255, 0.04);
    border-radius: 24px;
}

QWidget#hero_card {
    background-color: rgba(59, 130, 246, 0.10);
    border-radius: 24px;
    border: 1px solid rgba(59, 130, 246, 0.45);
}

QLabel#hero_icon {
    font-size: 28px;
    color: rgba(147, 197, 253, 0.85);
}
"""

BREAK_THEME = """
QWidget {
    background-color: #10231c;
    color: #ecfeff;
    font-family: 'Inter', 'Arial';
}

QLabel#label_time {
    font-size: 64px;
    font-weight: 800;
    color: #a7f3d0;
}

QLabel#session_label {
    font-size: 14px;
    color: #6ee7b7;
}

QPushButton {
    background-color: #14532d;
    border: 1px solid #166534;
    border-radius: 14px;
    padding: 14px 22px;
    min-width: 100px;
}

QPushButton:hover {
    background-color: #166534;
}

QWidget#hero_card {
    background-color: rgba(255, 255, 255, 0.06);
    border-radius: 24px;
}

QWidget#hero_card {
    background-color: rgba(167, 243, 208, 0.08);
    border-radius: 24px;
    border: 1px solid rgba(167, 243, 208, 0.35);
}

QLabel#hero_icon {
    font-size: 28px;
    color: rgba(167, 243, 208, 0.9);
}
"""

LONG_BREAK_THEME = """
QWidget {
    background-color: #2a0f1f;   /* koyu gül kurusu */
    color: #fce7f3;
    font-family: 'Inter', 'Arial';
}

QLabel#label_time {
    font-size: 64px;
    font-weight: 800;
    color: #fecdd3;   /* yumuşak pastel pembe */
}

QLabel#session_label {
    font-size: 14px;
    color: #fbcfe8;
}

QPushButton {
    background-color: #7a284b;
    border: 1px solid #9d3a66;
    border-radius: 14px;
    padding: 14px 22px;
    min-width: 100px;
    color: #fff1f2;
}

QPushButton:hover {
    background-color: #9d3a66;
}

QPushButton:disabled {
    background-color: #5b1f38;
    color: #f5d0e0;
}

QWidget#hero_card {
    background-color: rgba(255, 192, 203, 0.10);
    border-radius: 24px;
    border: 1px solid rgba(255, 182, 193, 0.35);
}

QLabel#hero_icon {
    font-size: 28px;
    color: rgba(255, 182, 193, 0.9);
}
"""