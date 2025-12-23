# Markdown to PDF Converter 📄

A Python program that converts Markdown files to professional PDFs. Includes custom CSS support and emoji support.

## Features ✨

- 🖥️ **Graphical Interface (GUI)**: User-friendly graphical interface
- 💻 **Command Line**: Use from terminal
- 🎨 **Custom CSS Support**: Use your own CSS file
- 😊 **Emoji Support**: Emojis display properly in PDF
- 📝 **Rich Markdown Support**: Tables, code blocks, syntax highlighting
- 🔢 **Page Numbering**: Automatic page numbers
- 📊 **Table Support**: Markdown tables look great
- 💻 **Code Blocks**: Code blocks with syntax highlighting
- 🎯 **Wildcard Support**: Process multiple files at once
- 📊 **Progress Tracking**: Process status and logs in GUI

## Installation 🚀

1. Install required packages:

```bash
pip install -r requirements.txt
```

**Note**: WeasyPrint may require some system dependencies:

- **macOS**: `brew install cairo pango gdk-pixbuf libffi`
- **Ubuntu/Debian**: `sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0`
- **Windows**: Usually installs automatically

## Usage 📖

### Graphical Interface (GUI) 🖥️

You can use the graphical interface for the easiest usage:

**Open with a single command:**
```bash
./md2pdf
```

or

```bash
python md_to_pdf_gui.py
```

**Add to PATH for access from anywhere:**
```bash
# For macOS/Linux, add to ~/.zshrc or ~/.bashrc file:
export PATH="$PATH:/Users/tahsinmert/Desktop/md_to_pdf"

# Then you can run from anywhere:
md2pdf
```

GUI features:
- 📁 File selection dialogs
- 🎨 CSS file selection (optional)
- 📄 Output PDF file specification
- 📊 Progress bar
- 📝 Process logs
- ✅ Success/error messages
- 🚀 One-click conversion

### Command Line Usage 💻

#### Basic Usage

```bash
python md_to_pdf.py file.md
```

This command creates `file.pdf`.

#### Specify Output File

```bash
python md_to_pdf.py file.md -o output.pdf
```

#### Using Custom CSS

```bash
python md_to_pdf.py file.md -c custom.css
```

#### Processing Multiple Files

```bash
python md_to_pdf.py file1.md file2.md file3.md
```

or using wildcards:

```bash
python md_to_pdf.py *.md
```

## Example Markdown File

You can use the `ornek.md` file to test the program:

```bash
python md_to_pdf.py ornek.md
```

## Custom CSS Customization 🎨

You can fully customize your PDF's appearance by editing the `custom.css` file. An example CSS file is available in the project.

### CSS Features

- Page size and margins
- Font families and sizes
- Colors and backgrounds
- Table styles
- Code block styles
- Header and footer areas

## Supported Markdown Features

- ✅ Headings (H1-H6)
- ✅ Paragraphs
- ✅ **Bold** and *italic* text
- ✅ Code blocks and inline code
- ✅ Syntax highlighting
- ✅ Tables
- ✅ Lists (ordered and unordered)
- ✅ Blockquotes
- ✅ Links
- ✅ Images
- ✅ Horizontal rules
- ✅ Emojis 😊 🎉 ✨

## Troubleshooting 🔧

### WeasyPrint Installation Issues

If you're having trouble installing WeasyPrint:

**macOS:**
```bash
brew install cairo pango gdk-pixbuf libffi
pip install weasyprint
```

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0
pip install weasyprint
```

### Emojis Not Displaying

For emojis to display properly, emoji fonts must be installed on your system. They are usually installed on macOS and modern Linux distributions.

## License 📜

This project is free to use.

## Contributing 🤝

Feel free to open an issue for your suggestions and contributions!
