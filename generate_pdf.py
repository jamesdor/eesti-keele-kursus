#!/usr/bin/env python3
"""
Generate a single HTML file from all course Markdown files.
Open in browser → Ctrl+P → Save as PDF.
"""

import os
import re
from datetime import datetime

FOLDER = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(FOLDER, "eesti_keele_kursus.html")

# Files in reading order
FILES_ORDER = [
    "ROADMAP.md",
    "study_plans.md",
    "pronunciation_guide.md",
    "grammar_cheatsheets.md",
    "grammar_complete.md",
    "flashcards_data.md",
    "common_mistakes.md",
    "materials_A1.md",
    "materials_A2.md",
    "materials_B1.md",
    "materials_B2.md",
    "materials_C1.md",
    "phrases_idioms_tests.md",
    "audio_resources.md",
    "speaking_topics.md",
    "mini_stories.md",
    "pictures_and_video.md",
    "business_estonian.md",
    "culture_guide.md",
    "estonian_holidays.md",
    "games.md",
    "lesson_plans.md",
    "workbook.md",
    "practice_exams.md",
    "progress_tracker.md",
    "e_nagu_eesti.md",
]

HEADER = """<!DOCTYPE html>
<html lang="et">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="theme-color" content="#0a1628">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Eesti Keele">
<meta name="application-name" content="Eesti Keele Kursus">
<link rel="manifest" href="manifest.json">
<link rel="apple-touch-icon" href="icon-192.png">
<title>Eesti keele kursus A1-C1</title>
<style>
  @page { margin: 1.8cm; size: A4; }
  * { box-sizing: border-box; }

  /* ===== БАЗОВЫЕ СТИЛИ ===== */
  body {
    font-family: 'Inter', 'Segoe UI', 'Arial', sans-serif;
    font-size: 11pt;
    line-height: 1.7;
    color: #1a1a1a;
    max-width: 210mm;
    margin: 0 auto;
    padding: 24px 32px;
    background: #fafafa;
  }

  /* ===== ЦВЕТОВЫЕ ТЕМЫ УРОВНЕЙ ===== */
  .level-a1 { --level-color: #2e7d32; --level-bg: #e8f5e9; --level-border: #a5d6a7; }
  .level-a2 { --level-color: #00796b; --level-bg: #e0f2f1; --level-border: #80cbc4; }
  .level-b1 { --level-color: #1565c0; --level-bg: #e3f2fd; --level-border: #90caf9; }
  .level-b2 { --level-color: #6a1b9a; --level-bg: #f3e5f5; --level-border: #ce93d8; }
  .level-c1 { --level-color: #e65100; --level-bg: #fff3e0; --level-border: #ffab91; }

  .level-badge {
    display: inline-block; padding: 4px 14px; border-radius: 20px;
    font-size: 10pt; font-weight: 700; letter-spacing: 1px;
    color: white; margin-bottom: 10px;
  }
  .level-a1 .level-badge { background: #2e7d32; }
  .level-a2 .level-badge { background: #00796b; }
  .level-b1 .level-badge { background: #1565c0; }
  .level-b2 .level-badge { background: #6a1b9a; }
  .level-c1 .level-badge { background: #e65100; }

  /* ===== ОБЛОЖКА ===== */
  .cover {
    text-align: center; padding: 60px 40px; page-break-after: always;
    background: linear-gradient(160deg, #0a1628 0%, #0d2137 25%, #003366 50%, #005599 75%, #0077b6 100%);
    color: white; border-radius: 16px; margin-bottom: 30px;
    min-height: 90vh; display: flex; flex-direction: column; justify-content: center;
    position: relative; overflow: hidden;
    box-shadow: 0 8px 40px rgba(0,0,0,0.15);
  }
  /* Decorative flag waves */
  .cover::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background-image:
      radial-gradient(circle at 20% 30%, rgba(255,255,255,0.05) 0%, transparent 50%),
      radial-gradient(circle at 80% 70%, rgba(0,119,182,0.15) 0%, transparent 50%),
      radial-gradient(circle at 50% 50%, rgba(255,255,255,0.02) 0%, transparent 70%);
    pointer-events: none;
  }
  /* Decorative stripes — subtle flag waves */
  .cover .bg-stripe {
    position: absolute; left: -10%; right: -10%; height: 60px;
    opacity: 0.06; pointer-events: none;
    border-radius: 30%;
    animation: coverWave 6s ease-in-out infinite;
  }
  .cover .bg-stripe:nth-child(1) { top: 15%; background: #0072ce; animation-delay: 0s; }
  .cover .bg-stripe:nth-child(2) { top: 35%; background: #000; animation-delay: 1s; }
  .cover .bg-stripe:nth-child(3) { top: 55%; background: #fff; animation-delay: 2s; }
  .cover .bg-stripe:nth-child(4) { top: 72%; background: #0072ce; animation-delay: 3s; }
  @keyframes coverWave {
    0%, 100% { transform: translateX(0) scaleY(1); }
    50% { transform: translateX(2%) scaleY(1.2); }
  }
  /* Decorative circles */
  .cover .deco-circle {
    position: absolute; border-radius: 50%; pointer-events: none;
    opacity: 0.04; border: 1px solid rgba(255,255,255,0.1);
  }
  .cover .deco-circle:nth-child(5) { width: 300px; height: 300px; top: -80px; right: -60px; }
  .cover .deco-circle:nth-child(6) { width: 200px; height: 200px; bottom: -40px; left: -60px; }
  .cover .deco-circle:nth-child(7) { width: 150px; height: 150px; bottom: 20%; right: 10%; }
  .cover::after {
    content: ''; position: absolute; bottom: 0; left: 0; right: 0;
    height: 120px;
    background: linear-gradient(transparent, rgba(0,0,0,0.2));
    pointer-events: none;
  }
  .cover .cover-inner { position: relative; z-index: 2; }
  /* Badge "UUS!" */
  .cover .badge {
    display: inline-block; padding: 6px 18px; border-radius: 20px;
    background: linear-gradient(135deg, #ff6f00, #ff8f00);
    color: white; font-size: 9pt; font-weight: 700; letter-spacing: 1.5px;
    text-transform: uppercase; margin-bottom: 20px;
    animation: badgePulse 2s ease-in-out infinite;
    box-shadow: 0 4px 12px rgba(255,111,0,0.3);
  }
  @keyframes badgePulse {
    0%, 100% { transform: scale(1); box-shadow: 0 4px 12px rgba(255,111,0,0.3); }
    50% { transform: scale(1.05); box-shadow: 0 6px 20px rgba(255,111,0,0.5); }
  }
  .cover .flag-row {
    display: flex; justify-content: center; align-items: center; gap: 24px; margin: 0 0 24px;
  }
  .cover .flag-item {
    display: flex; flex-direction: column; align-items: center; gap: 6px;
  }
  .cover .flag-item svg {
    width: 96px; height: 64px; border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    transition: transform 0.4s ease, box-shadow 0.4s ease;
    animation: flagWave 2.5s ease-in-out infinite;
    transform-origin: 50% 50% 0;
  }
  .cover .flag-item:nth-child(1) svg { animation-delay: 0s; }
  .cover .flag-item:nth-child(3) svg { animation-delay: 1.2s; }
  .cover .flag-item svg:hover { animation: none; transform: scale(1.08) translateY(-2px); box-shadow: 0 8px 30px rgba(0,0,0,0.4); }
  @keyframes flagWave {
    0%, 100% { transform: perspective(500px) rotateY(0deg) skewY(0deg); }
    20% { transform: perspective(500px) rotateY(6deg) skewY(1deg); }
    40% { transform: perspective(500px) rotateY(-3deg) skewY(-0.5deg); }
    60% { transform: perspective(500px) rotateY(4deg) skewY(0.5deg); }
    80% { transform: perspective(500px) rotateY(-2deg) skewY(-0.3deg); }
  }
  .cover .flag-label { font-size: 7pt; color: rgba(255,255,255,0.5); letter-spacing: 1px; text-transform: uppercase; }
  .cover .flag-divider {
    width: 1px; height: 50px; background: linear-gradient(transparent, rgba(255,255,255,0.2), transparent);
  }
  .cover h1 {
    font-size: 44pt; border: none; text-align: center; color: white;
    margin: 0 0 8px; font-weight: 800; letter-spacing: -2px;
    text-shadow: 0 2px 20px rgba(0,0,0,0.2);
    background: linear-gradient(135deg, #ffffff 0%, #90caf9 50%, #64b5f6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
  }
  .cover .subtitle {
    font-size: 17pt; color: rgba(255,255,255,0.85);
    margin: 0 0 8px; font-weight: 300;
    letter-spacing: 0.5px;
  }
  .cover .subtitle-em {
    font-size: 12pt; color: rgba(255,255,255,0.55);
    margin: 0 0 4px; font-weight: 300;
    font-style: italic;
  }
  .cover .estonia-bar {
    display: flex; height: 4px; width: 240px; margin: 22px auto; border-radius: 2px; overflow: hidden;
    box-shadow: 0 1px 8px rgba(0,0,0,0.15);
  }
  .cover .estonia-bar span { flex: 1; }
  .cover .estonia-bar .blue { background: #0072ce; }
  .cover .estonia-bar .black { background: #000; }
  .cover .estonia-bar .white { background: #fff; }
  .cover .stats {
    display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;
    margin: 24px auto 0; max-width: 650px;
  }
  .cover .stat {
    text-align: center;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 12px; padding: 14px 18px; min-width: 90px;
    transition: transform 0.3s ease, background 0.3s ease;
  }
  .cover .stat:hover { transform: translateY(-3px); background: rgba(255,255,255,0.14); }
  .cover .stat-num { font-size: 20pt; font-weight: 700; color: rgba(255,255,255,0.95); }
  .cover .stat-label { font-size: 7.5pt; color: rgba(255,255,255,0.55); text-transform: uppercase; letter-spacing: 1.5px; margin-top: 4px; }
  .cover .stat-highlight .stat-num { color: #ffcc02; }
  .cover .start-btn {
    display: inline-block; margin: 28px auto 0; padding: 14px 42px;
    border-radius: 30px; border: 2px solid rgba(255,255,255,0.35);
    background: linear-gradient(135deg, rgba(255,255,255,0.12), rgba(255,255,255,0.05));
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    color: white; font-size: 11pt; font-weight: 600;
    cursor: pointer; text-decoration: none;
    transition: all 0.3s ease;
    letter-spacing: 0.5px;
  }
  .cover .start-btn:hover {
    background: linear-gradient(135deg, rgba(255,255,255,0.22), rgba(255,255,255,0.12));
    border-color: rgba(255,255,255,0.6);
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.25);
  }
  .cover .start-btn-arrow { display: inline-block; transition: transform 0.3s ease; margin-left: 4px; }
  .cover .start-btn:hover .start-btn-arrow { transform: translateX(4px); }
  .cover .meta { margin-top: 28px; font-size: 8pt; color: rgba(255,255,255,0.4); line-height: 1.6; }

  /* ===== ЗАГОЛОВКИ ===== */
  h1 {
    font-size: 20pt; margin-top: 40px; margin-bottom: 16px; page-break-before: always;
    padding: 16px 20px; border-radius: 10px; font-weight: 700;
  }
  h1:first-of-type { page-break-before: avoid; }
  h1.section-A1 { background: linear-gradient(135deg, #e8f5e9, #c8e6c9); color: #1b5e20; border-left: 5px solid #2e7d32; }
  h1.section-A2 { background: linear-gradient(135deg, #e0f2f1, #b2dfdb); color: #004d40; border-left: 5px solid #00796b; }
  h1.section-B1 { background: linear-gradient(135deg, #e3f2fd, #bbdefb); color: #0d47a1; border-left: 5px solid #1565c0; }
  h1.section-B2 { background: linear-gradient(135deg, #f3e5f5, #e1bee7); color: #4a148c; border-left: 5px solid #6a1b9a; }
  h1.section-C1 { background: linear-gradient(135deg, #fff3e0, #ffe0b2); color: #bf360c; border-left: 5px solid #e65100; }
  h1.section-other { background: linear-gradient(135deg, #e8eaf6, #c5cae9); color: #1a237e; border-left: 5px solid #3949ab; }

  h2 {
    font-size: 15pt; color: #1a237e; margin-top: 28px; margin-bottom: 12px;
    padding-bottom: 6px; border-bottom: 2px solid #e0e0e0; font-weight: 600;
  }
  h3 { font-size: 12pt; color: #333; margin-top: 22px; margin-bottom: 8px; font-weight: 600; }
  h4 { font-size: 11pt; color: #555; margin-top: 18px; margin-bottom: 6px; font-weight: 600; }

  /* ===== ТАБЛИЦЫ ===== */
  table {
    width: 100%; border-collapse: separate; border-spacing: 0;
    margin: 16px 0; font-size: 10pt; page-break-inside: avoid;
    border-radius: 8px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  }
  th {
    background: linear-gradient(180deg, #37474f, #263238);
    color: white; padding: 10px 12px; text-align: left; font-weight: 600;
    font-size: 9.5pt; text-transform: uppercase; letter-spacing: 0.5px;
  }
  td { padding: 8px 12px; border-bottom: 1px solid #e0e0e0; }
  tr:last-child td { border-bottom: none; }
  tr:nth-child(even) { background: #f5f7fa; }
  tr:hover { background: #e3f2fd; }

  /* ===== БЛОК-ЦИТАТЫ ===== */
  blockquote {
    margin: 16px 0; padding: 12px 20px;
    background: linear-gradient(135deg, #f5f7fa, #eef1f5);
    border-left: 4px solid #1565c0; border-radius: 0 8px 8px 0;
    font-style: italic; color: #333;
  }

  /* ===== КОД ===== */
  code {
    background: #263238; color: #ffcdd2; padding: 2px 8px;
    border-radius: 4px; font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: 9.5pt;
  }
  pre {
    background: #263238; color: #e0e0e0; padding: 16px 20px;
    border-radius: 8px; overflow-x: auto; font-size: 9.5pt;
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    line-height: 1.5; box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }

  /* ===== СПИСКИ ===== */
  ul, ol { margin: 10px 0; padding-left: 24px; }
  li { margin: 4px 0; }
  ul li::marker { color: #1565c0; }

  /* ===== РАЗДЕЛИТЕЛИ ===== */
  hr {
    border: none; height: 2px;
    background: linear-gradient(90deg, transparent, #1565c0, transparent);
    margin: 30px 0;
  }

  /* ===== ССЫЛКИ ===== */
  a { color: #1565c0; text-decoration: none; font-weight: 500; }
  a:hover { text-decoration: underline; }

  /* ===== ОГЛАВЛЕНИЕ ===== */
  .toc { page-break-after: always; padding: 20px 0; }
  .toc h1 { background: none; border-left: none; padding: 0; color: #1a237e; font-size: 22pt; margin-bottom: 20px; }
  .toc ul { list-style: none; padding: 0; font-size: 11pt; columns: 2; column-gap: 30px; }
  .toc li { padding: 2px 0; break-inside: avoid; }
  .toc a {
    display: block; padding: 6px 12px; border-radius: 6px; margin: 2px 0;
    transition: all 0.2s; border-left: 3px solid transparent;
  }
  .toc a:hover { background: #e3f2fd; border-left-color: #1565c0; text-decoration: none; }
  .toc .toc-level {
    display: inline-block; padding: 1px 8px; border-radius: 10px;
    font-size: 8pt; font-weight: 700; color: white; margin-right: 6px;
  }
  .toc .toc-level.A1 { background: #2e7d32; }
  .toc .toc-level.A2 { background: #00796b; }
  .toc .toc-level.B1 { background: #1565c0; }
  .toc .toc-level.B2 { background: #6a1b9a; }
  .toc .toc-level.C1 { background: #e65100; }
  .toc .toc-level.other { background: #3949ab; }

  /* ===== КАРТОЧКИ ДЛЯ УПРАЖНЕНИЙ ===== */
  .exercise-box {
    background: linear-gradient(135deg, #f5f7fa, #eef1f5);
    border: 1px solid #e0e0e0; border-radius: 10px;
    padding: 16px 20px; margin: 16px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  }
  .exercise-box h4 { margin-top: 0; color: #1565c0; }

  /* ===== ПРОГРЕСС-БАРЫ ===== */
  .progress-bar {
    height: 8px; background: #e0e0e0; border-radius: 4px;
    margin: 6px 0; overflow: hidden;
  }
  .progress-fill {
    height: 100%; border-radius: 4px;
    background: linear-gradient(90deg, #43a047, #66bb6a);
  }

  /* ===== УРОВНИ ДЛЯ СТАТЕЙ ===== */
  .level-tag {
    display: inline-block; padding: 2px 10px; border-radius: 12px;
    font-size: 8pt; font-weight: 700; color: white; margin: 0 4px;
  }

  /* ===== КОНТЕЙНЕР ДИАЛОГА ===== */
  .dialogue {
    background: #fafafa; border: 1px solid #e0e0e0;
    border-radius: 10px; padding: 16px 20px; margin: 16px 0;
    font-family: 'Georgia', serif; font-style: italic;
  }
  .dialogue .speaker { font-weight: 700; color: #1565c0; font-style: normal; }

  /* ===== ПОДСКАЗКИ ===== */
  .tip {
    background: linear-gradient(135deg, #fff8e1, #ffecb3); border: 1px solid #ffe082;
    border-radius: 8px; padding: 12px 16px; margin: 12px 0;
  }
  .tip::before { content: "💡 "; font-size: 14pt; }

  /* ===== ТАБЛИЦА ЧЕКБОКСОВ ===== */
  .task-checkbox { font-size: 14pt; margin-right: 6px; }

  /* ===== ФУТЕР ===== */
  .footer {
    text-align: center; color: #999; font-size: 9pt;
    margin-top: 40px; padding-top: 16px;
    border-top: 1px solid #e0e0e0;
  }

  /* ===== ПЕЧАТЬ ===== */
  @media print {
    body { padding: 0; background: white; }
    h1 { page-break-before: always; }
    h1:first-of-type { page-break-before: avoid; }
    h2 { page-break-after: avoid; }
    h3 { page-break-after: avoid; }
    table { page-break-inside: avoid; }
    pre { page-break-inside: avoid; }
    blockquote { page-break-inside: avoid; }
    .toc ul { columns: 2; }
    .cover { border-radius: 0; min-height: auto; padding: 40px; }
  }
</style>
</head>
<body>
<div class="cover">
  <div class="bg-stripe"></div>
  <div class="bg-stripe"></div>
  <div class="bg-stripe"></div>
  <div class="bg-stripe"></div>
  <div class="deco-circle"></div>
  <div class="deco-circle"></div>
  <div class="deco-circle"></div>
  <div class="cover-inner">
    <div class="badge">✦ Uus: E nagu Eesti ✦</div>
    <div class="flag-row">
      <div class="flag-item">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 54">
          <rect width="80" height="18" fill="#0072ce"/>
          <rect y="18" width="80" height="18" fill="#000"/>
          <rect y="36" width="80" height="18" fill="#fff"/>
        </svg>
        <span class="flag-label">Eesti</span>
      </div>
      <div class="flag-divider"></div>
      <div class="flag-item">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 54">
          <rect width="80" height="54" fill="#039"/>
          <defs><polygon id="star" points="0,-4 1,-1.2 4.2,-1.4 1.6,0.6 2.6,3.8 0,1.8 -2.6,3.8 -1.6,0.6 -4.2,-1.4 -1,-1.2" fill="#fc0"/></defs>
          <use href="#star" x="40" y="9"/>
          <use href="#star" x="50" y="11.5"/>
          <use href="#star" x="56" y="19"/>
          <use href="#star" x="54" y="28"/>
          <use href="#star" x="46" y="33"/>
          <use href="#star" x="34" y="33"/>
          <use href="#star" x="26" y="28"/>
          <use href="#star" x="24" y="19"/>
          <use href="#star" x="30" y="11.5"/>
        </svg>
        <span class="flag-label">Euroopa</span>
      </div>
    </div>
    <h1>Eesti Keele<br>Kursus</h1>
    <p class="subtitle">Täielik õppematerjalide kogu A1–C1</p>
    <p class="subtitle-em">"E nagu Eesti" ja palju muud</p>
    <div class="estonia-bar">
      <span class="blue"></span>
      <span class="black"></span>
      <span class="white"></span>
    </div>
    <div class="stats">
      <div class="stat"><div class="stat-num">26</div><div class="stat-label">Õppematerjali</div></div>
      <div class="stat"><div class="stat-num">15 000+</div><div class="stat-label">Rida teksti</div></div>
      <div class="stat stat-highlight"><div class="stat-num">UUS</div><div class="stat-label">E nagu Eesti</div></div>
      <div class="stat"><div class="stat-num">A1–C1</div><div class="stat-label">Kõik tasemed</div></div>
    </div>
    <a href="#ROADMAP" class="start-btn">Alusta siit <span class="start-btn-arrow">→</span></a>
    <p class="meta">Loodud: mai 2026 · 26 faili · 15 000+ rida · Kõik materjalid on originaalsed</p>
  </div>
</div>
<div class="search-no-print">
  <div class="search-container">
    <span class="search-icon">🔍</span>
    <input type="text" id="searchInput" placeholder="Otsi kogu kursusest..." autocomplete="off">
    <span class="search-clear" id="searchClear">✕</span>
    <span class="search-count" id="searchCount"></span>
  </div>
  <div class="search-hint">Otsi vähemalt 2 tähte</div>
  <div style="display:flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-top: 8px;">
    <div class="level-filter no-print" id="levelFilter">
      <button class="level-filter-btn active-all" data-level="all">Kõik</button>
      <button class="level-filter-btn" data-level="A1">A1</button>
      <button class="level-filter-btn" data-level="A2">A2</button>
      <button class="level-filter-btn" data-level="B1">B1</button>
      <button class="level-filter-btn" data-level="B2">B2</button>
      <button class="level-filter-btn" data-level="C1">C1</button>
    </div>
    <button class="trans-toggle no-print" id="transToggle">👁 Näita tõlget</button>
    <div class="font-controls no-print">
      <button class="font-btn" id="fontDec" title="Vähenda teksti">A−</button>
      <span class="font-size-label" id="fontLabel">100%</span>
      <button class="font-btn" id="fontInc" title="Suurenda teksti">A+</button>
    </div>
  </div>
  <div id="noResults" class="search-no-results">😕 Midagi ei leitud. Proovi teist sõna.</div>
</div>

<div class="toc">
<h1>Sisukord</h1>
<ul>
"""

INTERACTIVE_CSS = """
<style>
/* ===== INTERACTIVE SEARCH ===== */
.search-no-print { margin: 12px 0; }
.search-container { display: flex; align-items: center; gap: 10px; background: white; border: 2px solid #e0e0e0; border-radius: 10px; padding: 8px 16px; transition: all 0.3s; }
.search-container:focus-within { border-color: #1565c0; box-shadow: 0 0 0 3px rgba(21,101,192,0.15); }
.search-container input { flex: 1; border: none; outline: none; font-size: 11pt; padding: 4px 0; background: transparent; }
.search-container .search-icon { color: #999; font-size: 14pt; }
.search-container .search-clear { cursor: pointer; color: #999; font-size: 14pt; display: none; }
.search-container .search-clear.visible { display: inline; }
.search-match { background: #fff176; padding: 0 2px; border-radius: 2px; }
.search-no-results { text-align: center; padding: 40px; color: #999; font-size: 12pt; display: none; }
.search-count { font-size: 9pt; color: #1565c0; white-space: nowrap; }
.search-hint { font-size: 8pt; color: #999; margin: 2px 0 6px; }
body.dark-mode .search-count { color: #64b5f6; }
body.dark-mode .search-hint { color: #666; }

/* ===== SIDEBAR ===== */
.nav-sidebar { position: fixed; top: 0; left: 0; width: 280px; height: 100%; z-index: 2000; overflow-y: auto; padding: 20px; box-shadow: 2px 0 24px rgba(0,0,0,0.2); transform: translateX(-100%); transition: transform 0.3s; }
.nav-sidebar.open { transform: translateX(0); }

/* ===== DARK MODE ===== */
body.dark-mode { background: #121212; color: #e0e0e0; }
body.dark-mode .content-section { background: #1e1e1e; }
body.dark-mode h2 { color: #90caf9; border-bottom-color: #333; }
body.dark-mode h3 { color: #ccc; }
body.dark-mode h4 { color: #aaa; }
body.dark-mode h1.section-other { background: linear-gradient(135deg, #263238, #37474f); color: #b0bec5; border-left-color: #546e7a; }
body.dark-mode h1.section-A1 { background: linear-gradient(135deg, #1b3d1b, #2e5c2e); color: #a5d6a7; }
body.dark-mode h1.section-A2 { background: linear-gradient(135deg, #00363a, #005a5f); color: #80cbc4; }
body.dark-mode h1.section-B1 { background: linear-gradient(135deg, #0d213f, #1a3a5c); color: #90caf9; }
body.dark-mode h1.section-B2 { background: linear-gradient(135deg, #2a0f3d, #421a5c); color: #ce93d8; }
body.dark-mode h1.section-C1 { background: linear-gradient(135deg, #3d1a00, #5c2e00); color: #ffab91; }
body.dark-mode table { box-shadow: none; }
body.dark-mode th { background: linear-gradient(180deg, #37474f, #263238); }
body.dark-mode td { border-bottom-color: #333; }
body.dark-mode tr:nth-child(even) { background: #2a2a2a; }
body.dark-mode tr:hover { background: #333; }
body.dark-mode blockquote { background: linear-gradient(135deg, #1e1e1e, #2a2a2a); border-left-color: #42a5f5; color: #ccc; }
body.dark-mode pre { background: #0d0d0d; }
body.dark-mode code { background: #0d0d0d; }
body.dark-mode .toc a:hover { background: #333; }
body.dark-mode .exercise-box { background: linear-gradient(135deg, #1e1e1e, #2a2a2a); }
body.dark-mode .dialogue { background: #1e1e1e; }
body.dark-mode a { color: #64b5f6; }
body.dark-mode .search-container { background: #1e1e1e; border-color: #333; }
body.dark-mode .search-container input { color: #e0e0e0; }
body.dark-mode .search-container input::placeholder { color: #666; }

/* ===== FLOATING CONTROLS ===== */
.floating-controls { position: fixed; bottom: 24px; right: 24px; display: flex; flex-direction: column; gap: 8px; z-index: 1000; }
.floating-btn { width: 44px; height: 44px; border-radius: 50%; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 16pt; box-shadow: 0 2px 12px rgba(0,0,0,0.25); transition: all 0.2s; background: #1565c0; color: white; }
.floating-btn:hover { transform: scale(1.1); box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
.floating-btn.dark-btn { background: #333; }
body.dark-mode .floating-btn.dark-btn { background: #ffcc02; color: #333; }
.floating-btn.top-btn { display: none; }
.floating-btn.top-btn.visible { display: flex; }

/* ===== INLINE AUDIO PLAYER ===== */
.audio-play-btn { display: inline-flex; align-items: center; gap: 4px; cursor: pointer; color: #1565c0; font-size: 9pt; padding: 2px 10px; border-radius: 12px; border: 1px solid #1565c0; background: transparent; transition: all 0.2s; margin: 0 4px; }
.audio-play-btn:hover { background: #1565c0; color: white; }
.audio-play-btn.playing { background: #e65100; border-color: #e65100; color: white; }
body.dark-mode .audio-play-btn { color: #64b5f6; border-color: #64b5f6; }
body.dark-mode .audio-play-btn:hover { background: #64b5f6; color: #121212; }
.mini-player { position: fixed; bottom: 80px; right: 24px; background: white; border-radius: 12px; box-shadow: 0 4px 24px rgba(0,0,0,0.2); padding: 12px 16px; display: none; z-index: 999; min-width: 260px; }
.mini-player.visible { display: block; }
.mini-player .track-name { font-size: 9pt; color: #666; margin-bottom: 6px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.mini-player audio { width: 100%; height: 36px; }
body.dark-mode .mini-player { background: #1e1e1e; }
body.dark-mode .mini-player .track-name { color: #aaa; }

/* ===== FLASHCARDS ===== */
.flashcard-container { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; margin: 16px 0; }
.flashcard { perspective: 800px; cursor: pointer; height: 120px; }
.flashcard-inner { position: relative; width: 100%; height: 100%; transition: transform 0.5s; transform-style: preserve-3d; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.flashcard.flipped .flashcard-inner { transform: rotateX(180deg); }
.flashcard-front, .flashcard-back { position: absolute; width: 100%; height: 100%; backface-visibility: hidden; display: flex; align-items: center; justify-content: center; padding: 12px; border-radius: 10px; font-size: 10pt; text-align: center; }
.flashcard-front { background: linear-gradient(135deg, #e3f2fd, #bbdefb); color: #0d47a1; font-weight: 600; }
.flashcard-back { background: linear-gradient(135deg, #e8f5e9, #c8e6c9); color: #1b5e20; font-weight: 600; transform: rotateX(180deg); }
body.dark-mode .flashcard-front { background: linear-gradient(135deg, #1a3a5c, #0d213f); color: #90caf9; }
body.dark-mode .flashcard-back { background: linear-gradient(135deg, #1b3d1b, #2e5c2e); color: #a5d6a7; }
body.dark-mode .flashcard-inner { box-shadow: 0 2px 8px rgba(0,0,0,0.3); }
.flashcard-hint { font-size: 8pt; color: #999; text-align: center; margin: 4px 0 12px; }

/* ===== PROGRESS CHECKBOXES ===== */
.progress-checkbox { cursor: pointer; font-size: 14pt; user-select: none; margin-right: 8px; }
.progress-checkbox.done { opacity: 0.5; text-decoration: line-through; }

/* ===== COLLAPSIBLE SECTIONS ===== */
.content-section.collapsed h1 ~ * { display: none; }
.content-section .section-toggle { cursor: pointer; user-select: none; font-size: 12pt; margin-left: 8px; opacity: 0.5; transition: transform 0.2s; display: inline-block; }
.content-section.collapsed .section-toggle { transform: rotate(-90deg); }
.content-section .section-toggle:hover { opacity: 1; }

/* ===== LEVEL FILTER ===== */
.level-filter { display: flex; gap: 6px; flex-wrap: wrap; margin: 8px 0; }
.level-filter-btn { padding: 4px 14px; border-radius: 20px; border: 2px solid #e0e0e0; background: transparent; cursor: pointer; font-size: 9pt; font-weight: 700; transition: all 0.2s; color: #666; }
.level-filter-btn:hover { transform: scale(1.05); }
.level-filter-btn.active-a1 { background: #2e7d32; color: white; border-color: #2e7d32; }
.level-filter-btn.active-a2 { background: #00796b; color: white; border-color: #00796b; }
.level-filter-btn.active-b1 { background: #1565c0; color: white; border-color: #1565c0; }
.level-filter-btn.active-b2 { background: #6a1b9a; color: white; border-color: #6a1b9a; }
.level-filter-btn.active-c1 { background: #e65100; color: white; border-color: #e65100; }
.level-filter-btn.active-all { background: #37474f; color: white; border-color: #37474f; }
body.dark-mode .level-filter-btn { border-color: #444; color: #aaa; }
body.dark-mode .level-filter-btn.active-all { background: #546e7a; border-color: #546e7a; }

/* ===== VOCAB TABLE TRANSLATION TOGGLE ===== */
.vocab-table.hide-translation th:nth-child(2),
.vocab-table.hide-translation td:nth-child(2) { display: none; }
.trans-toggle { cursor: pointer; font-size: 9pt; padding: 4px 14px; border-radius: 20px; border: 2px solid #e0e0e0; background: transparent; color: #666; font-weight: 600; transition: all 0.2s; }
.trans-toggle:hover { border-color: #1565c0; color: #1565c0; }
.trans-toggle.active { background: #1565c0; color: white; border-color: #1565c0; }
body.dark-mode .trans-toggle { border-color: #444; color: #aaa; }
body.dark-mode .trans-toggle.active { background: #1565c0; color: white; border-color: #1565c0; }

/* ===== COPY BUTTON ===== */
.copy-btn { position: absolute; top: 6px; right: 6px; padding: 3px 10px; border-radius: 6px; border: 1px solid #e0e0e0; background: white; cursor: pointer; font-size: 8pt; color: #999; opacity: 0; transition: all 0.2s; }
pre:hover .copy-btn, .dialogue:hover .copy-btn { opacity: 1; }
.copy-btn:hover { background: #e3f2fd; color: #1565c0; border-color: #1565c0; }
.copy-btn.copied { background: #e8f5e9; color: #2e7d32; border-color: #2e7d32; opacity: 1; }
pre { position: relative; }
.dialogue { position: relative; }
body.dark-mode .copy-btn { background: #333; border-color: #444; color: #888; }
body.dark-mode .copy-btn:hover { background: #1a3a5c; color: #64b5f6; }
body.dark-mode .copy-btn.copied { background: #1b3d1b; color: #a5d6a7; }

/* ===== FONT SIZE ===== */
.font-controls { display: flex; gap: 6px; align-items: center; }
.font-btn { width: 32px; height: 32px; border-radius: 50%; border: 1px solid #e0e0e0; background: transparent; cursor: pointer; font-size: 12pt; font-weight: 700; display: flex; align-items: center; justify-content: center; color: #666; transition: all 0.2s; }
.font-btn:hover { background: #e3f2fd; border-color: #1565c0; color: #1565c0; }
.font-size-label { font-size: 8pt; color: #999; min-width: 32px; text-align: center; }
body.dark-mode .font-btn { border-color: #444; color: #aaa; }
body.dark-mode .font-btn:hover { background: #1a3a5c; color: #64b5f6; }

/* ===== AUDIO SPEED ===== */
.speed-controls { display: flex; gap: 4px; margin-top: 6px; }
.speed-btn { padding: 2px 8px; border-radius: 10px; border: 1px solid #ddd; background: transparent; cursor: pointer; font-size: 8pt; color: #999; transition: all 0.2s; }
.speed-btn:hover { background: #e3f2fd; border-color: #1565c0; }
.speed-btn.active { background: #1565c0; color: white; border-color: #1565c0; }
body.dark-mode .speed-btn { border-color: #444; color: #888; }
body.dark-mode .speed-btn.active { background: #1565c0; color: white; }
@media (max-width: 768px) {
  body { padding: 10px 14px; font-size: 10pt; }
  .cover { padding: 40px 20px; min-height: auto; border-radius: 10px; }
  .cover h1 { font-size: 28pt; }
  .cover .subtitle { font-size: 13pt; }
  .cover .flag-row svg { width: 64px; height: 43px; }
  .cover .flag-row { gap: 14px; }
  .cover .stat { min-width: 70px; padding: 12px 14px; }
  .cover .stat-num { font-size: 18pt; }
  .cover .start-btn { padding: 10px 28px; font-size: 10pt; }
  .toc ul { columns: 1; }
  .toc h1 { font-size: 18pt; }
  .search-container { padding: 6px 12px; }
  .level-filter-btn { padding: 3px 10px; font-size: 8pt; }
  h1 { font-size: 16pt; padding: 12px 14px; }
  h2 { font-size: 13pt; }
  h3 { font-size: 11pt; }
  table { font-size: 9pt; display: block; overflow-x: auto; white-space: nowrap; }
  th, td { padding: 6px 8px; }
  .floating-controls { bottom: 14px; right: 14px; gap: 6px; }
  .floating-btn { width: 38px; height: 38px; font-size: 14pt; }
  .mini-player { bottom: 66px; right: 14px; min-width: 220px; }
  .flashcard-container { grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); }
  .flashcard { height: 90px; }
  .cover .estonia-bar { width: 140px; }
  .section-toggle { font-size: 9pt; }
  /* Mobile sidebar: bottom sheet */
  .nav-sidebar { width: 100% !important; height: 75% !important; top: auto !important; bottom: 0 !important; left: 0 !important; border-radius: 20px 20px 0 0 !important; transform: translateY(100%) !important; padding: 16px !important; }
  .nav-sidebar.open { transform: translateY(0) !important; }
}
}
@media (max-width: 480px) {
  body { padding: 8px 10px; font-size: 9.5pt; }
  .cover { padding: 30px 16px; }
  .cover h1 { font-size: 22pt; }
  .cover .subtitle { font-size: 11pt; }
  .cover .flag-row svg { width: 50px; height: 34px; }
  .cover .flag-row { gap: 10px; }
  .cover .flag-divider { height: 28px; }
  .cover .stats { gap: 8px; }
  .cover .stat { min-width: 60px; padding: 8px 10px; }
  .cover .stat-num { font-size: 14pt; }
  .cover .stat-label { font-size: 7pt; letter-spacing: 1px; }
  .cover .start-btn { padding: 8px 22px; font-size: 9pt; margin-top: 20px; }
  .cover .meta { font-size: 8pt; }
  .cover .estonia-bar { width: 100px; height: 3px; }
  h1 { font-size: 14pt; padding: 10px 12px; }
  h2 { font-size: 12pt; }
  table { font-size: 8pt; }
  .floating-btn { width: 34px; height: 34px; font-size: 12pt; }
  .mini-player { min-width: 180px; right: 10px; bottom: 58px; }
  .mini-player .track-name { font-size: 8pt; }
  .speed-btn { padding: 1px 6px; font-size: 7pt; }
  .flashcard-container { grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); }
  .flashcard { height: 70px; }
  .flashcard-front, .flashcard-back { font-size: 8pt; padding: 8px; }
  .toc ul { font-size: 10pt; }
  .toc li { padding: 1px 0; }
  .toc a { padding: 4px 8px; }
  .level-filter-btn { padding: 2px 8px; font-size: 7pt; }
  .search-container input { font-size: 10pt; }
  .audio-play-btn { font-size: 8pt; padding: 1px 8px; }
  .copy-btn { font-size: 8pt; padding: 2px 10px; }
  .font-btn { min-width: 26px; font-size: 11pt; }
}
/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) {
  body { padding: 20px 24px; }
  .cover h1 { font-size: 32pt; }
  .toc ul { columns: 2; }
  h1 { font-size: 18pt; }
} .cover h1 { font-size: 24pt; } .cover { padding: 30px 20px; } }

/* ===== PRINT OVERRIDES ===== */
@media print { .no-print, .floating-controls, .mini-player, .audio-play-btn, .search-container, .level-filter, .trans-toggle, .font-controls, .copy-btn, .section-toggle { display: none !important; } .search-no-print { display: none !important; } .flashcard-container { display: table; } .flashcard { display: table-row; } .flashcard-inner { transform: none !important; } .flashcard-back { display: none; } .content-section.collapsed h1 ~ * { display: block !important; } }
</style>
"""

INTERACTIVE_JS = """
<div class="mini-player no-print" id="miniPlayer">
  <div class="track-name" id="trackName">—</div>
  <audio id="miniAudio" controls preload="none"></audio>
  <div class="speed-controls" id="speedControls">
    <button class="speed-btn" data-speed="0.5">0.5x</button>
    <button class="speed-btn" data-speed="0.75">0.75x</button>
    <button class="speed-btn active" data-speed="1">1x</button>
    <button class="speed-btn" data-speed="1.25">1.25x</button>
    <button class="speed-btn" data-speed="1.5">1.5x</button>
  </div>
</div>

<div class="floating-controls no-print">
  <button class="floating-btn" id="navBtn" title="Navigatsioon">☰</button>
  <button class="floating-btn dark-btn" id="darkBtn" title="Tume/režiim">🌙</button>
  <button class="floating-btn top-btn" id="topBtn" title="Üles">↑</button>
</div>

<script>
(function() {
  'use strict';

  // Clear stale localStorage from old versions
  var VERSION = '2';
  if (localStorage.getItem('eesti_version') !== VERSION) {
    Object.keys(localStorage).forEach(function(k) {
      if (k.startsWith('eesti_')) localStorage.removeItem(k);
    });
    localStorage.setItem('eesti_version', VERSION);
  }

  // ===== DARK MODE =====
  function initDarkMode() {
    var saved = localStorage.getItem('eesti_dark');
    if (saved === 'true') document.body.classList.add('dark-mode');
  }
  function toggleDark() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('eesti_dark', document.body.classList.contains('dark-mode'));
  }

  // ===== SCROLL TO TOP =====
  function initScrollTop() {
    var btn = document.getElementById('topBtn');
    if (!btn) return;
    window.addEventListener('scroll', function() {
      btn.classList.toggle('visible', window.scrollY > 400);
    });
    btn.addEventListener('click', function() { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  }

  // ===== SEARCH =====
  function initSearch() {
    var input = document.getElementById('searchInput');
    var clear = document.getElementById('searchClear');
    var noResults = document.getElementById('noResults');
    var matchCount = document.getElementById('searchCount');
    if (!input) return;

    input.addEventListener('input', function() {
      var q = this.value.toLowerCase().trim();
      clear.style.display = q.length > 0 ? 'inline' : 'none';

      // Remove old highlights
      document.querySelectorAll('.search-match').forEach(function(m) {
        var parent = m.parentNode;
        parent.replaceChild(document.createTextNode(m.textContent), m);
        parent.normalize();
      });

      if (q.length < 2) {
        document.querySelectorAll('.content-section').forEach(function(s) { s.style.display = ''; });
        if (noResults) noResults.style.display = 'none';
        if (matchCount) matchCount.textContent = '';
        return;
      }

      var visibleCount = 0;
      document.querySelectorAll('.content-section').forEach(function(section) {
        var text = section.textContent.toLowerCase();
        var match = text.indexOf(q) !== -1;
        section.style.display = match ? '' : 'none';
        if (match) visibleCount++;

        // Highlight matches
        if (match) {
          var regex = new RegExp('(' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
          var els = section.querySelectorAll('p, li, td, dd, h1, h2, h3, h4, h5, h6, blockquote');
          els.forEach(function(el) {
            if (el.querySelector('script, style, .search-match')) return;
            if (el.children.length > 0) return; // skip complex elements
            var html = el.innerHTML;
            if (regex.test(html)) {
              el.innerHTML = html.replace(regex, '<span class="search-match">$1</span>');
            }
          });
        }
      });

      if (noResults) noResults.style.display = visibleCount === 0 ? 'block' : 'none';
      if (matchCount) matchCount.textContent = visibleCount > 0 ? visibleCount + ' tulemust' : '';
    });

    if (clear) {
      clear.addEventListener('click', function() {
        input.value = '';
        input.dispatchEvent(new Event('input'));
        input.focus();
      });
    }
  }

  // ===== AUDIO PLAYER =====
  function initAudioPlayer() {
    var audios = document.querySelectorAll('audio');
    audios.forEach(function(a) { a.preload = 'metadata'; });
    // Add play buttons next to audio file references in tables/paragraphs
    var re = /([\\w\\- ]+\\.mp3)/gi;
    document.querySelectorAll('td, p, li').forEach(function(el) {
      if (el.querySelector('.audio-play-btn') || el.closest('.mini-player') || el.closest('.floating-controls')) return;
      var html = el.innerHTML;
      var matched = html.match(re);
      if (!matched) return;
      matched.forEach(function(fname) {
        var path = findAudioFile(fname.trim());
        if (path) {
          var btn = '<button class="audio-play-btn" data-src="' + path + '" onclick="window.__playAudio(this)">▶ ' + fname.trim() + '</button>';
          html = html.replace(fname, btn);
        }
      });
      if (html !== el.innerHTML) el.innerHTML = html;
    });
  }

  window.__playAudio = function(btn) {
    var player = document.getElementById('miniPlayer');
    var audioEl = document.getElementById('miniAudio');
    var trackName = document.getElementById('trackName');
    if (!player || !audioEl) return;

    var src = btn.getAttribute('data-src');
    // Stop all other playing buttons
    document.querySelectorAll('.audio-play-btn.playing').forEach(function(b) { b.classList.remove('playing'); b.textContent = '▶ ' + b.textContent.slice(2); });

    if (audioEl.getAttribute('data-src') === src && !audioEl.paused) {
      audioEl.pause();
      player.classList.remove('visible');
      return;
    }

    audioEl.src = src;
    audioEl.setAttribute('data-src', src);
    trackName.textContent = btn.textContent.slice(2);
    audioEl.play();
    player.classList.add('visible');
    btn.classList.add('playing');
    btn.textContent = '⏸ ' + btn.textContent.slice(2);

    audioEl.onended = function() {
      btn.classList.remove('playing');
      btn.textContent = '▶ ' + btn.textContent.slice(2);
      player.classList.remove('visible');
    };
  };

  function findAudioFile(fname) {
    // Look for audio files in the audio/ directory
    var known = [
      // A2
      "audio/A2/teema1/A2_T1_s6nastik+treening.mp3",
      "audio/A2/teema1/A2_T1_s6nastik.mp3",
      "audio/A2/teema1/A2_T1_tere p2evast.mp3",
      "audio/A2/teema1/A2_T1_treening.mp3",
      "audio/A2/teema2/A2_T2_Liis ja Allar.mp3",
      "audio/A2/teema2/A2_T2_Sonastik+treening.mp3",
      "audio/A2/teema2/A2_T2_s6nastik 2.osa.mp3",
      "audio/A2/teema3/A2_T3_dialoog.mp3",
      "audio/A2/teema3/A2_T3_s6nastik 13.10.10.mp3",
      "audio/A2/teema3/A2_T3_s6nastik 2 osa 19.10.10.mp3",
      "audio/A2/teema3/A2_T3_treening.mp3",
      "audio/A2/teema4/A2- 4 - synasti II osa.mp3",
      "audio/A2/teema4/A2 - 4.synastik III osa.mp3",
      "audio/A2/teema4/A2 - 4.synastik IV osa.mp3",
      "audio/A2/teema4/A2 - 4.treening mp3.mp3",
      "audio/A2/teema4/A2_T4_mida ma selga panen dialoog.mp3",
      // B1
      "audio/B1/teema1/B1_T1 s6nastik.mp3",
      "audio/B1/teema1/B1_T1_1 klienditeenindaja -1.lugu.mp3",
      "audio/B1/teema1/B1_T1_2 arsti juures - 2.lugu.mp3",
      "audio/B1/teema1/B1_T1_3 Irinat pole kohal - 3.lugu.mp3",
      "audio/B1/teema1/B1_T1_4 piletikassas - 4.lugu.mp3",
      "audio/B1/teema1/B1_T1_5 spordiklubis - 5.lugu.mp3",
      "audio/B1/teema1/B1_T1_6 treening.mp3",
      "audio/B1/teema2/B1_T2_esimene jupp- Kus on 17a.mp3",
      "audio/B1/teema2/B1_T2_kolmas jupp-Hambaravi.mp3",
      "audio/B1/teema2/B1_T2_neljas jupp-Prillitoos.mp3",
      "audio/B1/teema2/B1_T2_s6nastic.mp3",
      "audio/B1/teema2/B1_T2_teine jupp-Firmast helistatakse.mp3",
      "audio/B1/teema3/B1-T3-lähme koos poodi -1.jupp.mp3",
      "audio/B1/teema3/B1_T3_2_jupp-džempri ostmine.mp3",
      "audio/B1/teema3/B1_T3_3_jupp-tige mutt.mp3",
      "audio/B1/teema3/B1_T3_4_jupp-hulgimüügi esindaja.mp3",
      "audio/B1/teema3/B1_T3_5_jupp.mp3",
      "audio/B1/teema3/B1_T3_Treening_2variant.mp3",
      "audio/B1/teema3/B1_T3_s6nastik-pooleli.mp3",
      "audio/B1/teema3/B1_T3_treening_1variant.mp3",
      "audio/B1/teema4/B1_T4_esimene jupp.mp3",
      "audio/B1/teema4/B1_T4_kolmas jupp.mp3",
      "audio/B1/teema4/B1_T4_s6nastik.mp3",
      "audio/B1/teema4/B1_T4_teine jupp.mp3",
      "audio/B1/teema4/B1_T4_treening.mp3",
      // UUS A2-B1
      "audio/UUS_A2-B1/Musike - VALMIS.mp3",
      "audio/UUS_A2-B1/Musike - sõnastik - tegusõnad.mp3",
      "audio/UUS_A2-B1/Musike - sõnastiku teine osa.mp3",
      "audio/UUS_A2-B1/oleme vist tuttavad VALMIS.mp3",
      "audio/UUS_A2-B1/oleme vist tuttavad.mp3",
      "audio/UUS_A2-B1/spordiklubi.mp3",
      "audio/UUS_A2-B1/tädi Mare ja Kreeka - sõnastiku saba.mp3",
      "audio/UUS_A2-B1/tädi Mare ja Kreeka - tegusõnad.mp3",
      "audio/UUS_A2-B1/tädi Mare ja Kreeka - treening.mp3",
      "audio/UUS_A2-B1/tädi mare VALMIS.mp3",
    ];
    var lower = fname.toLowerCase();
    for (var i = 0; i < known.length; i++) {
      if (known[i].toLowerCase().indexOf(lower) !== -1) return known[i];
    }
    return null;
  }

  // ===== FLASHCARDS =====
  function initFlashcards() {
    document.querySelectorAll('.flashcard').forEach(function(card) {
      card.addEventListener('click', function() {
        this.classList.toggle('flipped');
      });
    });
  }

  // ===== PROGRESS CHECKBOXES =====
  function initProgress() {
    document.querySelectorAll('.task-checkbox').forEach(function(el) {
      el.addEventListener('click', function() {
        this.classList.toggle('done');
        var key = 'eesti_progress_' + encodeURIComponent(this.textContent.trim());
        localStorage.setItem(key, this.classList.contains('done') ? '1' : '0');
      });
      // Restore saved state
      var key = 'eesti_progress_' + encodeURIComponent(el.textContent.trim());
      if (localStorage.getItem(key) === '1') el.classList.add('done');
    });
  }

  // ===== NAV SIDEBAR =====
  function initNav() {
    var btn = document.getElementById('navBtn');
    if (!btn) return;
    var expanded = false;
    var sidebar = null;
    var overlay = null;

    function closeSidebar() {
      expanded = false;
      if (sidebar) {
        sidebar.classList.remove('open');
        setTimeout(function() { if (sidebar) { sidebar.remove(); sidebar = null; } }, 300);
      }
      if (overlay) { overlay.remove(); overlay = null; }
    }

    function createSidebar() {
      sidebar = document.createElement('div');
      sidebar.id = 'navSidebar';
      sidebar.className = 'nav-sidebar';
      var isDark = document.body.classList.contains('dark-mode');
      var bgColor = isDark ? '#1e1e1e' : 'white';
      var textColor = isDark ? '#64b5f6' : '#1565c0';
      var hoverBg = isDark ? '#333' : '#f0f0f0';
      sidebar.style.background = bgColor;
      // Close button
      var header = document.createElement('div');
      header.style.cssText = 'display:flex;justify-content:space-between;align-items:center;margin-bottom:16px;';
      var title = document.createElement('span');
      title.textContent = '📖 Sisukord';
      title.style.cssText = 'font-size:14pt;font-weight:700;color:' + (isDark ? '#e0e0e0' : '#333') + ';';
      header.appendChild(title);
      var closeBtn = document.createElement('button');
      closeBtn.textContent = '✕';
      closeBtn.style.cssText = 'border:none;background:none;font-size:18pt;cursor:pointer;color:inherit;padding:4px 8px;';
      closeBtn.addEventListener('click', closeSidebar);
      header.appendChild(closeBtn);
      sidebar.appendChild(header);
      // Search in sidebar
      var searchInput = document.createElement('input');
      searchInput.type = 'text';
      searchInput.placeholder = '🔍 Filtreeri...';
      searchInput.style.cssText = 'width:100%;padding:8px 12px;border:1px solid ' + (isDark ? '#444' : '#ddd') + ';border-radius:8px;font-size:10pt;background:transparent;color:inherit;margin-bottom:12px;box-sizing:border-box;';
      sidebar.appendChild(searchInput);
      // List
      var list = document.createElement('ul');
      list.style.cssText = 'list-style:none;padding:0;margin:0;';
      function buildList(filter) {
        list.innerHTML = '';
        document.querySelectorAll('.content-section').forEach(function(s) {
          var title = s.getAttribute('data-title') || 'Section';
          var level = s.getAttribute('data-level') || '';
          var text = (level !== 'other' ? '[' + level + '] ' : '') + title;
          if (filter && text.toLowerCase().indexOf(filter.toLowerCase()) === -1) return;
          var li = document.createElement('li');
          var a = document.createElement('a');
          a.textContent = text;
          a.href = '#' + s.id.replace('section-', '');
          a.setAttribute('data-target', s.id.replace('section-', ''));
          a.style.cssText = 'display:block;padding:8px 12px;border-radius:6px;color:' + textColor + ';text-decoration:none;font-size:10pt;margin:2px 0;';
          a.addEventListener('mouseenter', function() { this.style.background = hoverBg; });
          a.addEventListener('mouseleave', function() { this.style.background = 'transparent'; });
          a.addEventListener('click', function(e) { e.preventDefault(); var target = this.getAttribute('data-target'); closeSidebar(); if (target) document.getElementById(target)?.scrollIntoView({ behavior: 'smooth' }); });
          li.appendChild(a);
          list.appendChild(li);
        });
      }
      buildList('');
      sidebar.appendChild(list);
      // Filter
      searchInput.addEventListener('input', function() { buildList(this.value); });
      // Overlay
      overlay = document.createElement('div');
      overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.3);z-index:1999;';
      overlay.addEventListener('click', closeSidebar);
      document.body.appendChild(overlay);
      document.body.appendChild(sidebar);
      setTimeout(function() { if (sidebar) { sidebar.classList.add('open'); } }, 10);
      // Observe dark mode
      var obs = new MutationObserver(function() {
        if (!sidebar) return;
        var isDarkMode = document.body.classList.contains('dark-mode');
        sidebar.style.background = isDarkMode ? '#1e1e1e' : 'white';
        sidebar.querySelectorAll('a').forEach(function(a) { a.style.color = isDarkMode ? '#64b5f6' : '#1565c0'; });
        sidebar.querySelectorAll('a').forEach(function(a) {
          a.addEventListener('mouseenter', function() { this.style.background = isDarkMode ? '#333' : '#f0f0f0'; });
          a.addEventListener('mouseleave', function() { this.style.background = 'transparent'; });
        });
      });
      obs.observe(document.body, { attributes: true, attributeFilter: ['class'] });
    }

    btn.addEventListener('click', function() {
      expanded = !expanded;
      if (expanded) { if (!sidebar) createSidebar(); }
      else { closeSidebar(); }
    });
  }

  // ===== COLLAPSE SECTIONS =====
  function initCollapse() {
    document.querySelectorAll('.content-section').forEach(function(section) {
      var h = section.querySelector('h1');
      if (!h) return;
      // Skip TOC heading
      if (section.querySelector('.toc')) return;
      var toggle = document.createElement('span');
      toggle.className = 'section-toggle no-print';
      toggle.textContent = '▼';
      toggle.title = 'Vajuta, et peita/näita sisu';
      h.appendChild(toggle);
      h.style.cursor = 'pointer';
      h.addEventListener('click', function(e) {
        // Ignore clicks on links inside h1
        if (e.target.tagName === 'A') return;
        section.classList.toggle('collapsed');
      });
    });
  }

  // ===== LEVEL FILTER =====
  function initLevelFilter() {
    var filter = document.getElementById('levelFilter');
    if (!filter) return;
    filter.querySelectorAll('.level-filter-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        var level = this.getAttribute('data-level');
        filter.querySelectorAll('.level-filter-btn').forEach(function(b) { b.className = 'level-filter-btn'; });
        this.classList.add('active-' + (level === 'all' ? 'all' : level.toLowerCase()));
        document.querySelectorAll('.content-section').forEach(function(section) {
          if (level === 'all') { section.style.display = ''; return; }
          var sectionLevel = section.getAttribute('data-level');
          section.style.display = sectionLevel === level ? '' : 'none';
        });
        localStorage.setItem('eesti_level', level);
      });
    });
    var saved = localStorage.getItem('eesti_level');
    if (saved) {
      var btn = filter.querySelector('[data-level="' + saved + '"]');
      if (btn) btn.click();
    }
  }

  // ===== TRANSLATION TOGGLE =====
  function initTranslationToggle() {
    var btn = document.getElementById('transToggle');
    if (!btn) return;
    btn.addEventListener('click', function() {
      var hidden = document.body.classList.toggle('trans-hidden');
      btn.textContent = hidden ? '👁 Peida tõlge' : '👁 Näita tõlget';
      btn.classList.toggle('active', hidden);
      localStorage.setItem('eesti_trans_hidden', hidden ? '1' : '0');
      document.querySelectorAll('.vocab-table').forEach(function(t) {
        t.classList.toggle('hide-translation', hidden);
      });
    });
    if (localStorage.getItem('eesti_trans_hidden') === '1') {
      btn.click();
    }
  }

  // ===== COPY BUTTONS =====
  function initCopyButtons() {
    document.querySelectorAll('pre, .dialogue').forEach(function(el) {
      if (el.querySelector('.copy-btn')) return;
      var btn = document.createElement('button');
      btn.className = 'copy-btn no-print';
      btn.textContent = '📋 Kopeeri';
      btn.addEventListener('click', function() {
        var text = el.tagName === 'PRE' ? el.textContent : el.textContent;
        navigator.clipboard.writeText(text.trim()).then(function() {
          btn.textContent = '✓ Kopeeritud!';
          btn.classList.add('copied');
          setTimeout(function() { btn.textContent = '📋 Kopeeri'; btn.classList.remove('copied'); }, 2000);
        });
      });
      el.appendChild(btn);
    });
  }

  // ===== SPEED CONTROL =====
  function initSpeedControl() {
    var audio = document.getElementById('miniAudio');
    var controls = document.getElementById('speedControls');
    if (!audio || !controls) return;
    controls.querySelectorAll('.speed-btn').forEach(function(btn) {
      btn.addEventListener('click', function() {
        controls.querySelectorAll('.speed-btn').forEach(function(b) { b.classList.remove('active'); });
        this.classList.add('active');
        audio.playbackRate = parseFloat(this.getAttribute('data-speed'));
      });
    });
  }

  // ===== FONT SIZE =====
  function initFontSize() {
    var inc = document.getElementById('fontInc');
    var dec = document.getElementById('fontDec');
    var label = document.getElementById('fontLabel');
    if (!inc || !dec || !label) return;
    var size = parseInt(localStorage.getItem('eesti_font_size')) || 100;
    function apply(s) {
      size = Math.max(70, Math.min(150, s));
      document.body.style.fontSize = (11 * size / 100) + 'pt';
      label.textContent = size + '%';
      localStorage.setItem('eesti_font_size', size);
    }
    inc.addEventListener('click', function() { apply(size + 5); });
    dec.addEventListener('click', function() { apply(size - 5); });
    apply(size);
  }

  // ===== INIT =====
  function safeInit(fn, name) {
    try { fn(); } catch(e) { console.warn('eesti_kursus: ' + name + ' failed', e); }
  }
  safeInit(initDarkMode, 'darkMode');
  safeInit(initScrollTop, 'scrollTop');
  safeInit(initSearch, 'search');
  safeInit(initAudioPlayer, 'audioPlayer');
  safeInit(initFlashcards, 'flashcards');
  safeInit(initProgress, 'progress');
  safeInit(initNav, 'nav');
  safeInit(initCollapse, 'collapse');
  safeInit(initLevelFilter, 'levelFilter');
  safeInit(initTranslationToggle, 'translationToggle');
  safeInit(initCopyButtons, 'copyButtons');
  safeInit(initSpeedControl, 'speedControl');
  safeInit(initFontSize, 'fontSize');

  // Dark mode button
  var darkBtn = document.getElementById('darkBtn');
  if (darkBtn) darkBtn.addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('eesti_dark', document.body.classList.contains('dark-mode'));
  });
})();

// Register service worker for PWA (works when served via HTTP)
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('sw.js').catch(function() {});
}
</script>
"""

FOOTER = """
<div class="footer">
  <p>Eesti keele kursus A1-C1 — Generated May 2026</p>
</div>
</body>
</html>"""

def md_to_html(text):
    """Convert basic markdown to HTML."""
    lines = text.split('\n')
    html = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip separator lines
        if line.strip() == '---':
            html.append('<hr>')
            i += 1
            continue

        # Headings
        if line.startswith('###### '):
            html.append(f'<h6>{line[7:]}</h6>')
        elif line.startswith('##### '):
            html.append(f'<h5>{line[6:]}</h5>')
        elif line.startswith('#### '):
            html.append(f'<h4>{line[5:]}</h4>')
        elif line.startswith('### '):
            html.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('## '):
            html.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('# '):
            html.append(f'<h1>{line[2:]}</h1>')

        # Blockquote
        elif line.startswith('> '):
            quote_lines = []
            while i < len(lines) and lines[i].startswith('> '):
                quote_lines.append(lines[i][2:])
                i += 1
            br = '<br>'
            html.append(f'<blockquote>{br.join(quote_lines)}</blockquote>')
            continue

        # Unordered list
        elif line.strip().startswith('- ') or line.strip().startswith('* '):
            list_lines = []
            while i < len(lines) and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('* ') or lines[i].strip() == ''):
                if lines[i].strip().startswith('- ') or lines[i].strip().startswith('* '):
                    content = lines[i].strip()[2:]
                    # Check for sub-items
                    if lines[i].startswith('  '):
                        list_lines.append(f'<li style="margin-left:20px">{process_inline(content)}</li>')
                    else:
                        list_lines.append(f'<li>{process_inline(content)}</li>')
                i += 1
            html.append(f'<ul>{"".join(list_lines)}</ul>')
            continue

        # Ordered list
        elif re.match(r'^\s*\d+\.\s', line):
            list_lines = []
            while i < len(lines) and re.match(r'^\s*\d+\.\s', lines[i]):
                content = re.sub(r'^\s*\d+\.\s', '', lines[i])
                list_lines.append(f'<li>{process_inline(content)}</li>')
                i += 1
            html.append(f'<ol>{"".join(list_lines)}</ol>')
            continue

        # Table
        elif '|' in line and line.strip().startswith('|'):
            table_lines = []
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i])
                i += 1
            html.append(parse_table(table_lines))
            continue

        # Task checkbox
        elif '⬜' in line or '✅' in line or '🔄' in line:
            processed = line.replace('⬜', '<span class="task-checkbox">☐</span>')
            processed = processed.replace('✅', '<span class="task-checkbox">☑</span>')
            processed = processed.replace('🔄', '<span class="task-checkbox">⟳</span>')
            html.append(f'<p>{processed}</p>')

        # Code block
        elif line.strip().startswith('```'):
            lang = line.strip()[3:]
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            code_text = "\n".join(code_lines)
            html.append(f'<pre><code>{code_text}</code></pre>')

        # Empty line
        elif line.strip() == '':
            # Only add <br> if previous wasn't a block element
            if html and not html[-1].startswith('<'):
                pass  # skip empty lines

        # Regular paragraph
        else:
            para = process_inline(line)
            html.append(f'<p>{para}</p>')

        i += 1

    return '\n'.join(html)

def process_inline(text):
    """Process inline formatting."""
    # Links first (before bold/italic, in case links are inside bold markers)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<em>\1</em>', text)
    # Code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    return text

def parse_table(lines):
    """Parse markdown table."""
    rows = []
    is_vocab = False
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if i == 1 and re.match(r'^[\s|:-]+$', line):
            continue  # skip separator
        tag = 'th' if i == 0 else 'td'
        # Detect vocabulary tables (Eesti ↔ Русский / Vene)
        if i == 0:
            header_text = ' '.join(cells).lower()
            if 'vene' in header_text or 'русский' in header_text or 'eesti' in header_text or 'inglise' in header_text:
                is_vocab = True
        processed_cells = ''.join(f"<{tag}>{process_inline(c)}</{tag}>" for c in cells)
        row = f'<tr>{processed_cells}</tr>'
        rows.append(row)
    table_class = 'vocab-table' if is_vocab else ''
    return f'<table class="{table_class}">{"".join(rows)}</table>'

def clean_md_content(text, filename):
    """Clean up markdown content before conversion."""
    lines = text.split('\n')
    # Remove the first heading (duplicate — generator adds its own)
    if lines and lines[0].startswith('# '):
        lines = lines[1:]
    # Remove soft hyphens and special chars that break layout
    text = '\n'.join(lines)
    # Fix escaped characters
    text = text.replace('\u00ad', '')  # soft hyphen
    return text

def get_title_from_file(filename):
    """Extract a readable title from filename and its level."""
    titles = {
        "ROADMAP.md": ("Õppimise teekaart", "other"),
        "pronunciation_guide.md": ("Hääldusjuhend", "other"),
        "common_mistakes.md": ("Tüüpivead ja enesekontroll", "other"),
        "grammar_complete.md": ("Grammatika täielik ülevaade", "other"),
        "grammar_cheatsheets.md": ("Grammatika kiirviited", "other"),
        "flashcards_data.md": ("Flashcardid ja sõnavara", "other"),
        "phrases_idioms_tests.md": ("Fraasid, idioomid ja testid", "other"),
        "mini_stories.md": ("Minilood", "other"),
        "audio_resources.md": ("Audioressursid", "other"),
        "culture_guide.md": ("Eesti kultuur ja kombed", "other"),
        "estonian_holidays.md": ("Eesti pühad ja traditsioonid", "other"),
        "games.md": ("Mängud ja tegevused", "other"),
        "speaking_topics.md": ("Kõneteemad ja rollimängud", "other"),
        "pictures_and_video.md": ("Pildikirjeldused ja videod", "other"),
        "business_estonian.md": ("Ärieesti keel", "other"),
        "lesson_plans.md": ("Tunnikavad", "other"),
        "study_plans.md": ("Õppeplaanid", "other"),
        "materials_A1.md": ("Materjalid A1", "A1"),
        "materials_A2.md": ("Materjalid A2", "A2"),
        "materials_B1.md": ("Materjalid B1", "B1"),
        "materials_B2.md": ("Materjalid B2", "B2"),
        "materials_C1.md": ("Materjalid C1", "C1"),
        "practice_exams.md": ("Proovieksamid", "other"),
        "workbook.md": ("Töövihik", "other"),
        "progress_tracker.md": ("Edusammude jälgija", "other"),
        "e_nagu_eesti.md": ("E nagu Eesti 1-3", "A1"),
    }
    return titles.get(filename, (filename.replace('.md', '').replace('_', ' ').title(), "other"))

def main():
    toc_items = []
    all_html = []

    for fname in FILES_ORDER:
        fpath = os.path.join(FOLDER, fname)
        if not os.path.exists(fpath):
            continue

        title, level = get_title_from_file(fname)
        level_class = f'section-{level}' if level != 'other' else 'section-other'
        level_label = f'<span class="toc-level {level}">{level}</span>' if level != 'other' else ''

        toc_items.append(f'<li><a href="#{fname.replace(".md","")}">{level_label}{title}</a></li>')

        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        content = clean_md_content(content, fname)
        body = md_to_html(content)

        section_id = fname.replace(".md", "")
        all_html.append(f'<section class="content-section" id="section-{section_id}" data-title="{title}" data-level="{level}">')
        all_html.append(f'<h1 id="{section_id}" class="{level_class}">{title}</h1>')
        all_html.append(body)
        all_html.append('</section>')

    # Build TOC
    toc_html = '\n'.join(toc_items)

    # Write HTML output
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(HEADER)
        f.write(INTERACTIVE_CSS)
        f.write(toc_html)
        f.write('</ul></div>')
        f.write('\n'.join(all_html))
        f.write(INTERACTIVE_JS)
        f.write(FOOTER)

    # Write PWA manifest
    manifest = {
        "name": "Eesti Keele Kursus",
        "short_name": "Eesti Keele",
        "description": "Täielik õppematerjalide kogu eesti keele õppimiseks A1–C1",
        "id": "eesti-keele-kursus",
        "start_url": "/eesti-keele-kursus/",
        "scope": "/eesti-keele-kursus/",
        "display": "standalone",
        "orientation": "any",
        "background_color": "#0a1628",
        "theme_color": "#0a1628",
        "lang": "et",
        "categories": ["education", "language"],
        "icons": [
            {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable"}
        ]
    }
    with open(os.path.join(FOLDER, 'manifest.json'), 'w', encoding='utf-8') as f:
        import json
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    # Write PNG icons using Pillow
    try:
        from PIL import Image, ImageDraw, ImageFont
        def make_icon(size):
            img = Image.new('RGBA', (size, size), (10, 22, 40, 255))
            draw = ImageDraw.Draw(img)
            fs = int(size * 0.48)
            try:
                font = ImageFont.truetype('arial.ttf', fs)
            except:
                font = ImageFont.load_default()
            text = 'EE'
            bbox = draw.textbbox((0, 0), text, font=font)
            tw = bbox[2] - bbox[0]
            th = bbox[3] - bbox[1]
            x = (size - tw) // 2
            y = (size - th) // 2 - int(size * 0.05)
            draw.text((x, y), text, fill=(255,255,255,255), font=font)
            img.save(os.path.join(FOLDER, f'icon-{size}.png'), 'PNG')
        make_icon(192)
        make_icon(512)
        print("PNG ikoonid on loodud")
    except ImportError:
        print("Pillow puudub, PNG ikoone ei loodud")

    # Write service worker
    sw = """// Eesti Keele Kursus — Service Worker
const CACHE = 'eesti-keele-v1';
const URLS = [
  'eesti_keele_kursus.html',
  'manifest.json',
  'icon-192.png',
  'icon-512.png'
];

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE).then(function(cache) {
      return cache.addAll(URLS);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(keys.map(function(k) {
        if (k !== CACHE) return caches.delete(k);
      }));
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', function(e) {
  e.respondWith(
    caches.match(e.request).then(function(r) {
      return r || fetch(e.request).catch(function() { return r; });
    })
  );
});
"""
    with open(os.path.join(FOLDER, 'sw.js'), 'w', encoding='utf-8') as f:
        f.write(sw)

    print(f"HTML loodud: {OUTPUT}")
    print("PWA failid (manifest.json, sw.js, ikoonid) on lisatud.")
    print("Ava fail brauseris → installi nupp ilmub aadressiribale.")

if __name__ == '__main__':
    main()
