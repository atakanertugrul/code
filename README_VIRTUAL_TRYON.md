# 👕 Virtual Try-On Uygulaması

Bu proje, bir model resmine istediğiniz kıyafeti sanal olarak giydirmenizi sağlar. Python ve en güncel yapay zeka modelleri kullanılarak geliştirilmiştir.

## 🎯 Özellikler

- ✅ **Gerçekçi Sonuçlar**: Kıyafetler vücuda doğal bir şekilde oturur
- ✅ **Kolay Kullanım**: Google Colab'da tek tıkla çalışır
- ✅ **Hızlı İşlem**: HuggingFace API ile dakikalar içinde sonuç
- ✅ **Ücretsiz**: Tamamen açık kaynak ve ücretsiz kullanım

## 🚀 Hızlı Başlangıç

### 1️⃣ Google Colab'da Açın

1. `virtual_try_on.ipynb` dosyasını Google Colab'a yükleyin
2. Veya şu linkten direkt açın: [Google Colab'da Aç](https://colab.research.google.com/)

### 2️⃣ Resimlerinizi Hazırlayın

**İhtiyacınız Olan:**
- 📸 **Model Resmi**: Kıyafeti giydirmek istediğiniz kişinin fotoğrafı
- 👔 **Kıyafet Resmi**: Giydirmek istediğiniz kıyafet

**En İyi Sonuçlar İçin:**
- Model resmi: Dik duruş, düz arka plan, tam vücut görünür
- Kıyafet resmi: Düz zemin, iyi aydınlatma, kıyafet tam görünür

### 3️⃣ Notebook'u Çalıştırın

1. Runtime → Run all (Ctrl+F9)
2. Resimlerinizi Colab'a yükleyin
3. Resim yollarını kod hücresine yazın
4. Son hücreyi çalıştırıp sonucu görün!

## 📖 Kullanım Örneği

```python
# Model ve kıyafet resimlerinizin yollarını yazın
PERSON_IMAGE = "/content/model.jpg"      # Sizin model resminiz
GARMENT_IMAGE = "/content/tshirt.jpg"    # Sizin kıyafet resminiz
GARMENT_DESC = "mavi tişört"             # Opsiyonel açıklama

# Virtual try-on işlemini başlat
result = virtual_try_on(PERSON_IMAGE, GARMENT_IMAGE, GARMENT_DESC)

# Sonuçları görüntüle
show_results(PERSON_IMAGE, GARMENT_IMAGE, result)
```

## 🛠️ Teknik Detaylar

**Kullanılan Teknolojiler:**
- **Model**: IDM-VTON (Image-based Virtual Try-On Network)
- **Framework**: PyTorch, Diffusers
- **API**: HuggingFace Spaces (Gradio)

**Sistem Gereksinimleri:**
- Google Colab ücretsiz tier yeterli
- GPU: T4 (Colab'da otomatik sağlanır)
- RAM: 12GB (Colab'da mevcut)

## 💡 İpuçları

### ✅ Desteklenen Kıyafet Türleri:
- T-shirt, Gömlek
- Kazak, Sweatshirt
- Ceket, Blazer
- Üst giyim genel

### ⚠️ Sınırlı Destek:
- Pantolon (model üst giyim için optimize)
- Tam elbise (bazı durumlarda çalışabilir)
- Aksesuarlar

### 🎨 Kaliteli Sonuç İçin:
1. **Aydınlatma**: Hem model hem kıyafet iyi aydınlatılmış olmalı
2. **Arka Plan**: Düz, tek renkli arka plan tercih edin
3. **Çözünürlük**: Minimum 512x512 piksel kullanın
4. **Pozisyon**: Model dik durmalı, kollar görünür olmalı

## 🔧 Sorun Giderme

### Problem: "API hatası alıyorum"
**Çözüm**:
- İnternet bağlantınızı kontrol edin
- Birkaç dakika bekleyip tekrar deneyin
- HuggingFace API bazen meşgul olabilir

### Problem: "Kıyafet doğru oturmuyor"
**Çözüm**:
- Model resminde kişinin tam vücudu görünür olmalı
- Farklı bir model resmi deneyin
- Kod içinde `denoising_steps` değerini 30'dan 50'ye çıkarın

### Problem: "Sonuç bulanık çıkıyor"
**Çözüm**:
- Daha yüksek çözünürlüklü resimler kullanın
- Resimlerin iyi aydınlatılmış olduğundan emin olun
- Farklı `seed` değerleri deneyin

## 📚 Ek Kaynaklar

- [IDM-VTON Paper](https://arxiv.org/abs/2403.05139)
- [HuggingFace Model](https://huggingface.co/spaces/yisol/IDM-VTON)
- [Virtual Try-On Teknolojisi Hakkında](https://github.com/minar09/awesome-virtual-try-on)

## 🤝 Katkıda Bulunma

Bu proje açık kaynaklıdır. Geliştirmeler için PR göndermekten çekinmeyin!

## 📝 Lisans

MIT License - Özgürce kullanabilirsiniz.

## ⭐ Teşekkürler

- IDM-VTON ekibine harika model için
- HuggingFace ekibine API desteği için

---

**Sorularınız için:** GitHub Issues bölümünü kullanabilirsiniz.

**İyi eğlenceler! 🎉**
