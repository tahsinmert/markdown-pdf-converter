#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown to PDF Converter
MD dosyalarını PDF'e çeviren program
"""

import os
import sys
import argparse
from pathlib import Path
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration


def get_default_css():
    """Varsayılan CSS stilini döndürür"""
    return """
    @page {
        size: A4;
        margin: 2cm;
        @top-right {
            content: counter(page) " / " counter(pages);
            font-size: 10pt;
            color: #666;
        }
    }
    
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #333;
        max-width: 100%;
    }
    
    h1 {
        font-size: 24pt;
        font-weight: bold;
        margin-top: 1em;
        margin-bottom: 0.5em;
        color: #2c3e50;
        border-bottom: 3px solid #3498db;
        padding-bottom: 0.3em;
    }
    
    h2 {
        font-size: 20pt;
        font-weight: bold;
        margin-top: 0.8em;
        margin-bottom: 0.4em;
        color: #34495e;
        border-bottom: 2px solid #95a5a6;
        padding-bottom: 0.2em;
    }
    
    h3 {
        font-size: 16pt;
        font-weight: bold;
        margin-top: 0.6em;
        margin-bottom: 0.3em;
        color: #34495e;
    }
    
    h4, h5, h6 {
        font-size: 14pt;
        font-weight: bold;
        margin-top: 0.5em;
        margin-bottom: 0.3em;
        color: #34495e;
    }
    
    p {
        margin-top: 0.5em;
        margin-bottom: 0.5em;
        text-align: justify;
    }
    
    code {
        font-family: "SF Mono", Monaco, "Cascadia Code", "Roboto Mono", Consolas, "Courier New", monospace;
        font-size: 0.9em;
        background-color: #f4f4f4;
        padding: 0.2em 0.4em;
        border-radius: 3px;
        color: #e83e8c;
    }
    
    pre {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 5px;
        padding: 1em;
        overflow-x: auto;
        margin: 1em 0;
    }
    
    pre code {
        background-color: transparent;
        padding: 0;
        color: #333;
        font-size: 0.85em;
    }
    
    blockquote {
        border-left: 4px solid #3498db;
        margin: 1em 0;
        padding-left: 1em;
        padding-right: 1em;
        color: #555;
        font-style: italic;
        background-color: #f8f9fa;
    }
    
    ul, ol {
        margin: 0.5em 0;
        padding-left: 2em;
    }
    
    li {
        margin: 0.3em 0;
    }
    
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 1em 0;
    }
    
    th, td {
        border: 1px solid #ddd;
        padding: 0.5em;
        text-align: left;
    }
    
    th {
        background-color: #3498db;
        color: white;
        font-weight: bold;
    }
    
    tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    
    a {
        color: #3498db;
        text-decoration: none;
    }
    
    a:hover {
        text-decoration: underline;
    }
    
    img {
        max-width: 100%;
        height: auto;
        margin: 1em 0;
        border-radius: 5px;
    }
    
    hr {
        border: none;
        border-top: 2px solid #e9ecef;
        margin: 2em 0;
    }
    
    /* Emoji desteği için */
    .emoji {
        font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", "EmojiOne Color", "Android Emoji", sans-serif;
    }
    
    /* Print optimizasyonları */
    @media print {
        body {
            print-color-adjust: exact;
            -webkit-print-color-adjust: exact;
        }
    }
    """


def convert_md_to_pdf(md_file_path, output_path=None, css_file_path=None, css_string=None):
    """
    Markdown dosyasını PDF'e çevirir
    
    Args:
        md_file_path: Markdown dosyasının yolu
        output_path: Çıktı PDF dosyasının yolu (None ise otomatik oluşturulur)
        css_file_path: Custom CSS dosyasının yolu (opsiyonel)
        css_string: CSS kodunu string olarak (opsiyonel, css_file_path'ten önceliklidir)
    """
    md_path = Path(md_file_path)
    
    if not md_path.exists():
        raise FileNotFoundError(f"Markdown dosyası bulunamadı: {md_file_path}")
    
    # Çıktı dosyası yolu belirlenir
    if output_path is None:
        output_path = md_path.with_suffix('.pdf')
    else:
        output_path = Path(output_path)
    
    # Markdown dosyasını oku
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except Exception as e:
        raise IOError(f"Markdown dosyası okunamadı: {e}")
    
    # Markdown'ı HTML'e çevir
    # Emoji ve diğer özellikler için extension'lar ekle
    extensions = [
        'extra',           # Tables, fenced code blocks, etc.
        'codehilite',      # Syntax highlighting
        'tables',          # Table support
        'nl2br',           # Newline to break
        'sane_lists',      # Better list handling
        'toc',             # Table of contents
        'fenced_code',     # Fenced code blocks
    ]
    
    md = markdown.Markdown(extensions=extensions)
    html_content = md.convert(md_content)
    
    # HTML wrapper ekle (emoji desteği için meta tag'ler)
    html_wrapper = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{md_path.stem}</title>
</head>
<body>
{html_content}
</body>
</html>"""
    
    # CSS dosyasını oku veya varsayılan CSS'i kullan
    if css_string:
        # CSS string olarak verilmişse direkt kullan
        custom_css = css_string
    elif css_file_path and Path(css_file_path).exists():
        try:
            with open(css_file_path, 'r', encoding='utf-8') as f:
                custom_css = f.read()
        except Exception as e:
            print(f"Uyarı: CSS dosyası okunamadı, varsayılan CSS kullanılıyor: {e}")
            custom_css = get_default_css()
    else:
        custom_css = get_default_css()
    
    # PDF oluştur
    try:
        font_config = FontConfiguration()
        html_doc = HTML(string=html_wrapper)
        css_doc = CSS(string=custom_css, font_config=font_config)
        
        html_doc.write_pdf(
            output_path,
            stylesheets=[css_doc],
            font_config=font_config
        )
        
        print(f"✓ PDF başarıyla oluşturuldu: {output_path}")
        return output_path
        
    except Exception as e:
        raise RuntimeError(f"PDF oluşturulurken hata oluştu: {e}")


def main():
    """Ana fonksiyon - komut satırı arayüzü"""
    parser = argparse.ArgumentParser(
        description='Markdown dosyalarını PDF\'e çevirir',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  %(prog)s dosya.md
  %(prog)s dosya.md -o cikti.pdf
  %(prog)s dosya.md -c custom.css
  %(prog)s *.md
        """
    )
    
    parser.add_argument(
        'input',
        nargs='+',
        help='Markdown dosyası(ları) (wildcard desteklenir)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Çıktı PDF dosyasının yolu (tek dosya için)'
    )
    
    parser.add_argument(
        '-c', '--css',
        help='Custom CSS dosyasının yolu'
    )
    
    args = parser.parse_args()
    
    # Dosya listesini oluştur
    md_files = []
    for pattern in args.input:
        path = Path(pattern)
        if path.is_file():
            md_files.append(path)
        elif '*' in pattern:
            # Wildcard desteği
            import glob
            md_files.extend([Path(f) for f in glob.glob(pattern) if f.endswith('.md')])
        else:
            print(f"Uyarı: Dosya bulunamadı: {pattern}")
    
    if not md_files:
        print("Hata: İşlenecek markdown dosyası bulunamadı!")
        sys.exit(1)
    
    # Her dosyayı işle
    for md_file in md_files:
        try:
            output = args.output if len(md_files) == 1 else None
            convert_md_to_pdf(md_file, output, args.css)
        except Exception as e:
            print(f"✗ Hata ({md_file}): {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()

