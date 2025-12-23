# Markdown to PDF Converter 📄

Markdown dosyalarını profesyonel PDF'lere çeviren Python programı. Custom CSS desteği ve emoji desteği içerir.

## Özellikler ✨

- 🖥️ **Grafik Arayüz (GUI)**: Kullanıcı dostu grafik arayüz
- 💻 **Komut Satırı**: Terminal üzerinden kullanım
- 🎨 **Custom CSS Desteği**: Kendi CSS dosyanızı kullanabilirsiniz
- 😊 **Emoji Desteği**: Emojiler PDF'de düzgün görüntülenir
- 📝 **Zengin Markdown Desteği**: Tablolar, kod blokları, syntax highlighting
- 🔢 **Sayfa Numaralandırma**: Otomatik sayfa numaraları
- 📊 **Tablo Desteği**: Markdown tabloları güzel görünür
- 💻 **Kod Blokları**: Syntax highlighting ile kod blokları
- 🎯 **Wildcard Desteği**: Birden fazla dosyayı tek seferde işleyebilirsiniz
- 📊 **İlerleme Takibi**: GUI'de işlem durumu ve loglar

## Kurulum 🚀

1. Gerekli paketleri yükleyin:

```bash
pip install -r requirements.txt
```

**Not**: WeasyPrint bazı sistem bağımlılıkları gerektirebilir:

- **macOS**: `brew install cairo pango gdk-pixbuf libffi`
- **Ubuntu/Debian**: `sudo apt-get install python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0`
- **Windows**: Genellikle otomatik kurulur

## Kullanım 📖

### Grafik Arayüz (GUI) 🖥️

En kolay kullanım için grafik arayüzü kullanabilirsiniz:

**Tek komut ile açmak:**
```bash
./md2pdf
```

veya

```bash
python md_to_pdf_gui.py
```

**Her yerden erişmek için PATH'e ekleyin:**
```bash
# macOS/Linux için ~/.zshrc veya ~/.bashrc dosyasına ekleyin:
export PATH="$PATH:/Users/tahsinmert/Desktop/md_to_pdf"

# Sonra her yerden çalıştırabilirsiniz:
md2pdf
```

GUI özellikleri:
- 📁 Dosya seçme diyalogları
- 🎨 CSS dosyası seçme (opsiyonel)
- 📄 Çıktı PDF dosyası belirleme
- 📊 İlerleme çubuğu
- 📝 İşlem logları
- ✅ Başarı/hata mesajları
- 🚀 Tek tıkla dönüştürme

### Komut Satırı Kullanımı 💻

#### Temel Kullanım

```bash
python md_to_pdf.py dosya.md
```

Bu komut `dosya.pdf` dosyasını oluşturur.

#### Çıktı Dosyası Belirtme

```bash
python md_to_pdf.py dosya.md -o cikti.pdf
```

#### Custom CSS Kullanma

```bash
python md_to_pdf.py dosya.md -c custom.css
```

#### Birden Fazla Dosya İşleme

```bash
python md_to_pdf.py dosya1.md dosya2.md dosya3.md
```

veya wildcard kullanarak:

```bash
python md_to_pdf.py *.md
```

## Örnek Markdown Dosyası

Programı test etmek için `ornek.md` dosyasını kullanabilirsiniz:

```bash
python md_to_pdf.py ornek.md
```

## Custom CSS Özelleştirme 🎨

`custom.css` dosyasını düzenleyerek PDF'inizin görünümünü tamamen özelleştirebilirsiniz. Örnek bir CSS dosyası projede mevcuttur.

### CSS Özellikleri

- Sayfa boyutu ve kenar boşlukları
- Font aileleri ve boyutları
- Renkler ve arka planlar
- Tablo stilleri
- Kod blokları stilleri
- Başlık ve alt bilgi alanları

## Desteklenen Markdown Özellikleri

- ✅ Başlıklar (H1-H6)
- ✅ Paragraflar
- ✅ **Kalın** ve *italik* metin
- ✅ Kod blokları ve inline kod
- ✅ Syntax highlighting
- ✅ Tablolar
- ✅ Listeler (sıralı ve sırasız)
- ✅ Alıntılar (blockquotes)
- ✅ Linkler
- ✅ Resimler
- ✅ Yatay çizgiler
- ✅ Emojiler 😊 🎉 ✨

## Sorun Giderme 🔧

### WeasyPrint Kurulum Sorunları

Eğer WeasyPrint kurulumunda sorun yaşıyorsanız:

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

### Emoji Görünmüyor

Emojilerin düzgün görünmesi için sisteminizde emoji fontları yüklü olmalıdır. macOS ve modern Linux dağıtımlarında genellikle yüklüdür.

## Lisans 📜

Bu proje özgürce kullanılabilir.

## Katkıda Bulunma 🤝

Önerileriniz ve katkılarınız için issue açabilirsiniz!

