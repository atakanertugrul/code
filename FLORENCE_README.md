# W Collection - Florence-2 ile Ürün Açıklaması Üretici

Florence-2 vision model ve Claude kullanarak otomatik ürün açıklaması oluşturma sistemi.

## 🎯 Özellikler

- ✅ Florence-2 ile detaylı görsel analizi
- ✅ Claude ile profesyonel ürün açıklamaları
- ✅ Toplu işlem desteği (batch processing)
- ✅ Metadata dosyası desteği
- ✅ Özelleştirilebilir marka tonu
- ✅ SEO-uyumlu çıktılar

## 📦 Kurulum

```bash
pip install -r requirements_florence.txt
```

## 🔑 API Key Ayarları

Claude API key'inizi environment variable olarak ayarlayın:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Veya `.env` dosyası kullanın:
```
ANTHROPIC_API_KEY=your-api-key-here
```

## 🚀 Kullanım

### 1. Tek Görsel İçin

```python
from florence_product_description import ProductDescriptionGenerator

generator = ProductDescriptionGenerator()

description, analysis = generator.generate_product_description(
    image_path="product.jpg",
    product_category="kadın giyim",
    brand_voice="modern ve şık",
    additional_context="2024 İlkbahar/Yaz koleksiyonu, pamuklu kumaş"
)

print(description)
```

### 2. Toplu İşlem (Klasör)

```python
from batch_product_description import BatchProductDescriptionGenerator

batch_gen = BatchProductDescriptionGenerator()

results = batch_gen.process_folder(
    input_folder="./product_images",
    output_file="descriptions.json",
    product_category="kadın giyim",
    brand_voice="zarif ve kadınsı"
)
```

### 3. Metadata Dosyası ile Toplu İşlem

Önce `product_metadata.json` oluşturun:

```json
[
  {
    "image_name": "dress_001.jpg",
    "category": "elbise",
    "brand_voice": "zarif ve kadınsı",
    "additional_context": "Siyah, midi boy, akşam etkinlikleri için"
  },
  {
    "image_name": "blouse_002.jpg",
    "category": "bluz",
    "brand_voice": "modern ve rahat",
    "additional_context": "Beyaz, pamuklu, günlük kullanım"
  }
]
```

Sonra toplu işlem yapın:

```python
from batch_product_description import BatchProductDescriptionGenerator

batch_gen = BatchProductDescriptionGenerator()

results = batch_gen.process_with_metadata(
    metadata_file="product_metadata.json",
    image_folder="./product_images",
    output_file="descriptions_with_metadata.json"
)
```

## 🎨 Florence-2'den Elde Edilen Bilgiler

Her görsel için şu bilgiler çıkarılır:

1. **Detailed Caption**: Görselin detaylı açıklaması
2. **Object Detection**: Tespit edilen nesneler ve konumları
3. **Dense Region Caption**: Bölgesel detaylı açıklamalar
4. **OCR**: Görsel üzerindeki yazılar (logo, etiket vb.)

Bu bilgiler Claude'a gönderilir ve profesyonel bir ürün açıklamasına dönüştürülür.

## 💡 Best Practices - Agent'a Ne Vermeli?

### Florence-2 Çıktıları:
✅ **Detaylı görsel açıklaması** - Genel kompozisyon ve ana öğeler
✅ **Nesne listesi** - Kıyafet parçaları, aksesuarlar
✅ **Bölgesel detaylar** - Desen, kesim, detay özellikleri
✅ **OCR metni** - Marka logoları, etiketler

### Ek Context Bilgileri:
✅ **Kategori** - Elbise, bluz, pantolon vb.
✅ **Marka tonu** - Premium, casual, sporty vb.
✅ **Malzeme bilgisi** - Eğer biliyorsanız (pamuk, ipek vb.)
✅ **Sezon/Koleksiyon** - 2024 İlkbahar, Sonbahar vb.
✅ **Hedef kitle** - Genç, profesyonel, casual vb.

## 📊 Çıktı Formatı

```json
{
  "image_name": "product_001.jpg",
  "description": "Modern ve şık bir tasarıma sahip bu midi boy elbise...",
  "visual_analysis": {
    "detailed_caption": "A black sleeveless midi dress...",
    "objects": "dress, zipper, fabric...",
    "dense_captions": "Region 1: elegant neckline...",
    "ocr_text": "W Collection"
  },
  "status": "success"
}
```

## ⚡ Performans İpuçları

1. **GPU Kullanımı**: CUDA varsa otomatik kullanılır (çok daha hızlı)
2. **Batch Size**: Aynı anda 10-20 görsel işlemek ideal
3. **Model Seçimi**:
   - `microsoft/Florence-2-base` - Hızlı, iyi performans
   - `microsoft/Florence-2-large` - Daha detaylı, daha yavaş

## 🔧 Özelleştirme

### Prompt'u Değiştirme

`florence_product_description.py` içinde `_build_description_prompt` metodunu düzenleyerek prompt'u özelleştirebilirsiniz.

### Farklı LLM Kullanma

OpenAI GPT kullanmak isterseniz:

```python
from openai import OpenAI

client = OpenAI(api_key="your-key")

response = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "user", "content": prompt}
    ]
)
```

## 🎯 W Collection için Özel Ayarlar

```python
# W Collection için optimize edilmiş ayarlar
description, analysis = generator.generate_product_description(
    image_path="product.jpg",
    product_category="kadın giyim",
    brand_voice="zarif, modern ve özgüvenli - W Collection'ın şık ve kaliteli duruşunu yansıtan",
    additional_context="Premium kalite, şık tasarım, özel koleksiyon"
)
```

## 📝 Örnek Çıktı

**Görsel:** Siyah midi elbise

**Üretilen Açıklama:**
```
Zarif Siyah Midi Elbise - W Collection

W Collection'ın sofistike tasarım anlayışıyla hazırlanan bu siyah midi elbise,
modern kadının zarafetini ve özgüvenini yansıtıyor. Kolsuz kesimi ve midi boyu
ile hem iş toplantılarında hem de akşam etkinliklerinde rahatlıkla tercih
edebileceğiniz bu elbise, zamansız bir şıklık sunuyor.

Minimalist çizgileriyle dikkat çeken tasarım, vücudu sararak kadınsı bir siluet
oluşturuyor. Premium kalite kumaşı sayesinde gün boyu konfor sağlarken, sade
ancak etkileyici duruşu gardırobunuzun vazgeçilmez parçası olmaya aday.

Öne Çıkan Özellikler:
• Zamansız siyah renk - Her tarzla uyumlu
• Midi boy kesim - Şık ve sofistike görünüm
• Kolsuz tasarım - Mevsimlik kulanım rahatlığı
• Vücut sarmalayan fit - Kadınsı siluet
• Premium kumaş kalitesi - Konforlu kullanım
• W Collection kalite garantisi
```

## 🤝 Katkı

Sorularınız için issue açabilir veya PR gönderebilirsiniz.

## 📄 Lisans

MIT License
