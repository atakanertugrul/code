# AI Ürün Açıklaması Oluşturucu

Yapay zeka destekli, otomatik ürün açıklaması oluşturan web uygulaması. OpenAI GPT modeli kullanarak profesyonel, çekici ve detaylı ürün açıklamaları saniyeler içinde oluşturur.

## Özellikler

- 🤖 **AI Destekli**: OpenAI GPT-4 ile profesyonel açıklamalar
- 🎨 **Özelleştirilebilir Ton**: Profesyonel, samimi, lüks, teknik veya arkadaşça
- 🌍 **Çoklu Dil**: Türkçe ve İngilizce desteği
- ⚡ **Hızlı ve Kolay**: Basit form ile anında sonuç
- 📋 **Tek Tıkla Kopyala**: Oluşturulan açıklamayı kolayca kopyalayın
- 📱 **Responsive Tasarım**: Mobil ve masaüstü uyumlu

## Ekran Görüntüsü

Uygulama modern ve kullanıcı dostu bir arayüze sahiptir:

- **Sol Panel**: Ürün bilgilerini girdiğiniz form
- **Sağ Panel**: AI tarafından oluşturulan açıklama

## Kurulum

### 1. Gereksinimler

- Python 3.8 veya üzeri
- OpenAI API anahtarı ([buradan](https://platform.openai.com/api-keys) alabilirsiniz)

### 2. Proje Kurulumu

```bash
# Proje dizinine gidin
cd product_description_app

# Virtual environment oluşturun
python -m venv venv

# Virtual environment'ı aktifleştirin
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### 3. Çevre Değişkenleri

`.env.example` dosyasını `.env` olarak kopyalayın ve OpenAI API anahtarınızı ekleyin:

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
MODEL_NAME=gpt-4-turbo-preview
```

## Kullanım

### Uygulamayı Başlatma

```bash
python app.py
```

Uygulama başlatıldıktan sonra tarayıcınızda şu adresi açın:

```
http://localhost:5000
```

### Ürün Açıklaması Oluşturma

1. **Ürün Adı**: Ürününüzün adını girin (zorunlu)
2. **Kategori**: Ürün kategorisini belirtin (opsiyonel)
3. **Özellikler**: Ürünün özelliklerini listeleyin (opsiyonel)
4. **Hedef Kitle**: Kimlere hitap ettiğini yazın (opsiyonel)
5. **Ton**: Açıklamanın tonunu seçin (profesyonel, samimi, lüks, vb.)
6. **Dil**: Türkçe veya İngilizce seçin
7. **"✨ Açıklama Oluştur"** butonuna tıklayın

AI, saniyeler içinde:
- Çekici bir başlık
- 2-3 paragraflık ana açıklama
- Önemli özellikler listesi
- Kullanım alanları
- Neden tercih edilmeli açıklaması

oluşturacaktır.

## Örnek Kullanım

### Örnek Girdi

```
Ürün Adı: Premium Deri Cüzdan
Kategori: Aksesuar
Özellikler: Gerçek deri, RFID koruması, 8 kart bölmesi, el yapımı
Hedef Kitle: Genç profesyoneller
Ton: Lüks
Dil: Türkçe
```

### Örnek Çıktı

AI, yukarıdaki bilgilere göre profesyonel bir ürün açıklaması oluşturacaktır.

## API Endpoint'leri

### POST /generate

Ürün açıklaması oluşturur.

**İstek (Request):**
```json
{
  "product_name": "Premium Deri Cüzdan",
  "category": "Aksesuar",
  "features": "Gerçek deri, RFID koruması",
  "target_audience": "Genç profesyoneller",
  "tone": "luxury",
  "language": "Turkish"
}
```

**Yanıt (Response):**
```json
{
  "success": true,
  "description": "Oluşturulan açıklama metni...",
  "product_info": {
    "name": "Premium Deri Cüzdan",
    ...
  }
}
```

### GET /health

Sistem sağlık kontrolü.

**Yanıt:**
```json
{
  "status": "healthy"
}
```

## Proje Yapısı

```
product_description_app/
├── app.py                  # Flask uygulaması (backend)
├── requirements.txt        # Python bağımlılıkları
├── .env.example           # Çevre değişkenleri örneği
├── README.md              # Bu dosya
├── static/                # Statik dosyalar
│   ├── style.css         # CSS stilleri
│   └── script.js         # JavaScript kodları
└── templates/            # HTML şablonları
    └── index.html        # Ana sayfa
```

## Teknolojiler

### Backend
- **Flask**: Python web framework
- **OpenAI API**: GPT-4 ile metin oluşturma
- **Flask-CORS**: Cross-Origin Resource Sharing

### Frontend
- **HTML5**: Semantik yapı
- **CSS3**: Modern tasarım ve animasyonlar
- **Vanilla JavaScript**: Form yönetimi ve API iletişimi

## Özelleştirme

### Farklı Ton Seçenekleri Ekleme

`templates/index.html` dosyasında tone select elementine yeni seçenekler ekleyebilirsiniz:

```html
<select id="tone" name="tone">
    <option value="professional">Profesyonel</option>
    <option value="yeni-ton">Yeni Ton</option>
</select>
```

### Farklı AI Modeli Kullanma

`.env` dosyasında MODEL_NAME değişkenini değiştirin:

```env
MODEL_NAME=gpt-4
# veya
MODEL_NAME=gpt-3.5-turbo
```

## Güvenlik

- API anahtarınızı asla paylaşmayın
- `.env` dosyasını git'e commit etmeyin (`.gitignore`'a ekleyin)
- Production ortamında `debug=False` kullanın

## Sorun Giderme

### "OPENAI_API_KEY not found" Hatası

`.env` dosyasını oluşturup API anahtarınızı eklediğinizden emin olun.

### "Module not found" Hatası

Tüm bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

### Port 5000 Kullanımda

`app.py` dosyasındaki port numarasını değiştirin:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik eklendi'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## Lisans

MIT License

## İletişim

Sorular ve öneriler için issue açabilirsiniz.

---

**Not**: Bu uygulama OpenAI API kullandığı için API kullanım ücretleri uygulanır. Detaylar için [OpenAI fiyatlandırma](https://openai.com/pricing) sayfasını ziyaret edin.
