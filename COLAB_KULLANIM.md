# 🚀 Google Colab Kullanım Kılavuzu

W Collection için Florence-2 + LLM ile ürün açıklaması üretimi

## 📋 Hızlı Başlangıç (5 Dakika)

### 1. Notebook'u Aç
Colab'da `W_Collection_Product_Description.ipynb` dosyasını açın

### 2. API Key Ayarla

**Önerilen: Google Gemini (Colab'da ücretsiz!)**

1. [Google AI Studio](https://makersuite.google.com/app/apikey)'ya git
2. API key oluştur
3. Colab'da: Sol menü → 🔑 Secrets → Add new secret
   - Name: `GEMINI_API_KEY`
   - Value: `your-api-key-here`

**Alternatif: Claude veya OpenAI**
- Claude: [console.anthropic.com](https://console.anthropic.com) → `ANTHROPIC_API_KEY`
- OpenAI: [platform.openai.com](https://platform.openai.com) → `OPENAI_API_KEY`

### 3. Hücreleri Çalıştır

```python
# 1. Kurulum
!pip install -q transformers pillow google-generativeai

# 2. Florence-2 yükle
# Cell'i çalıştır

# 3. Ürün görseli yükle
from google.colab import files
uploaded = files.upload()

# 4. Açıklama üret
quick_describe(
    image_path,
    Kategori="kazak",
    Malzeme="%100 pamuk",
    Renk="kahverengi"
)
```

### 4. Sonuç

```
✨ ÜRÜN AÇIKLAMASI
================================================================================

Yüzde yüz pamuk kumaştan üretilen kahve renkli W Collection kazak;
düğmeli polo yakaya sahiptir. Günlük kullanım için rahat ve şık bir
seçenek sunan bu kazak, klasik kesimi ile gardırobunuzun vazgeçilmezi olacak.
```

---

## 🎯 Kullanım Senaryoları

### Senaryo 1: Tek Ürün (Upload)

```python
# Görseli yükle
from google.colab import files
uploaded = files.upload()
image_path = list(uploaded.keys())[0]

# Analiz + Açıklama
visual_analysis, image = analyze_product_image(image_path)
description = generate_product_description(
    visual_analysis,
    product_info={
        "Kategori": "elbise",
        "Malzeme": "%100 polyester",
        "Renk": "siyah"
    }
)

print(description)
```

### Senaryo 2: URL'den Ürün

```python
# Direkt URL kullan
image_url = "https://example.com/product.jpg"

desc = quick_describe(
    image_url,
    Kategori="bluz",
    Malzeme="pamuklu",
    Renk="beyaz"
)
```

### Senaryo 3: Google Drive'dan Toplu İşlem

```python
# Google Drive'ı bağla
from google.colab import drive
drive.mount('/content/drive')

# Klasördeki tüm ürünler
image_folder = "/content/drive/MyDrive/w_collection_products"
results = process_multiple_products(image_folder)

# Sonuçları indir
from google.colab import files
files.download('product_descriptions.json')
```

---

## 🎨 Özelleştirme

### Farklı Çıktı Stilleri

Prompt'u değiştirerek farklı stiller elde edebilirsiniz:

**Kısa ve öz:**
```python
# generate_product_description fonksiyonunda prompt'u şu şekilde değiştirin:
\"\"\"2-3 cümlelik, kısa ve öz bir açıklama yaz.\"\"\"
```

**Detaylı ve satış odaklı:**
```python
\"\"\"4-5 cümlelik, detaylı ve satış odaklı bir açıklama yaz.
Ürünün avantajlarını ve kullanım alanlarını vurgula.\"\"\"
```

**Sadece teknik özellikler:**
```python
\"\"\"Sadece teknik özellikleri listele: malzeme, renk, kesim, detaylar.\"\"\"
```

### Marka Tonu Ayarlama

```python
prompt += \"\"\"
## Marka Tonu:
W Collection için yazıyorsun. Ton: zarif, modern, premium kalite vurgusu.
Hedef kitle: 25-45 yaş arası, şık ve kaliteli ürünleri tercih eden kadınlar.
\"\"\"
```

---

## 📊 Çıktı Formatları

### JSON Çıktısı

```json
{
  "image_name": "product_001.jpg",
  "description": "Yüzde yüz pamuk kumaştan üretilen...",
  "visual_analysis": {
    "detailed_caption": "A brown sweater with buttons...",
    "objects": "sweater, buttons, collar",
    "dense_captions": "Region 1: polo collar...",
    "ocr_text": "W Collection"
  },
  "status": "success"
}
```

### CSV Export

```python
import pandas as pd

# JSON'dan DataFrame oluştur
df = pd.DataFrame(results)
df.to_csv('products.csv', index=False, encoding='utf-8')

# İndir
files.download('products.csv')
```

---

## 🔧 Troubleshooting

### GPU Yok / Yavaş

```python
# Colab'da: Runtime → Change runtime type → GPU (T4)
# Ücretsiz kullanıcılar günde ~4 saat GPU kullanabilir
```

### API Rate Limit

```python
# Toplu işlemde delay ekle
import time

for image in images:
    # İşle
    time.sleep(2)  # API rate limit için bekleme
```

### Görsel Yükleme Hatası

```python
# Görseli resize et
from PIL import Image

image = Image.open(image_path)
if image.size[0] > 1024:
    image.thumbnail((1024, 1024))
    image.save('resized.jpg')
```

---

## 💡 Pro İpuçları

### 1. Batch Processing için Optimize

```python
# Aynı model instance'ını kullan (her seferinde yeniden yükleme)
for i in range(0, len(images), 10):
    batch = images[i:i+10]
    # Process batch
```

### 2. Sonuçları Cache'le

```python
import pickle

# Görsel analizini kaydet
with open('analysis_cache.pkl', 'wb') as f:
    pickle.dump(visual_analysis, f)

# Daha sonra yükle
with open('analysis_cache.pkl', 'rb') as f:
    visual_analysis = pickle.load(f)
```

### 3. Farklı LLM'leri Karşılaştır

```python
# Aynı görsel için 3 farklı LLM dene
for llm in ['gemini', 'claude', 'openai']:
    LLM_PROVIDER = llm
    desc = generate_product_description(visual_analysis)
    print(f"\n{llm.upper()}: {desc}")
```

---

## 📞 Destek

Sorun yaşarsanız:
1. Runtime'ı restart edin: Runtime → Restart runtime
2. GPU'yu kontrol edin: Runtime → Change runtime type
3. API key'i kontrol edin: Secrets bölümünden

---

## 🎓 Örnekler

### Örnek 1: Kazak

**Girdi:**
- Görsel: Kahverengi polo yaka kazak
- Kategori: kazak
- Malzeme: %100 pamuk
- Renk: kahverengi

**Çıktı:**
> "Yüzde yüz pamuk kumaştan üretilen kahve renkli W Collection kazak; düğmeli polo yakaya sahiptir. Rahat kesimiyle günlük kullanıma uygun olan bu kazak, klasik ve şık bir görünüm sunar."

### Örnek 2: Elbise

**Girdi:**
- Görsel: Siyah midi elbise
- Kategori: elbise
- Malzeme: %100 polyester
- Renk: siyah

**Çıktı:**
> "W Collection'ın zarif tasarımlarından siyah midi elbise, yüzde yüz polyester kumaştan üretilmiştir. Kolsuz kesimi ve vücudu saran silueti ile hem ofis ortamında hem de özel davetlerde rahatlıkla tercih edilebilir."

---

Başarılar! 🚀
