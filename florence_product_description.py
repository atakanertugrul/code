import torch
from transformers import AutoModelForCausalLM, AutoProcessor
from PIL import Image
import anthropic
import os
from typing import Dict, List

class ProductDescriptionGenerator:
    def __init__(self, model_id: str = "microsoft/Florence-2-base"):
        """Florence-2 ve Claude ile ürün açıklaması üretici"""

        # Florence-2 setup
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if self.device == "cuda" else torch.float32

        print(f"Device: {self.device} | dtype: {self.torch_dtype}")
        print("Florence-2 model yükleniyor...")

        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=self.torch_dtype,
            trust_remote_code=True,
        ).to(self.device)

        self.processor = AutoProcessor.from_pretrained(
            model_id,
            trust_remote_code=True,
        )

        # Claude setup (veya OpenAI kullanabilirsiniz)
        self.claude_client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )

        print("Model ve processor hazır.")

    def analyze_image_with_florence(self, image_path: str) -> Dict[str, any]:
        """
        Florence-2 ile görseli analiz et ve kapsamlı bilgi çıkar

        Returns:
            Dict containing:
            - detailed_caption: Detaylı görsel açıklaması
            - objects: Tespit edilen nesneler
            - dense_captions: Bölgesel detaylı açıklamalar
            - ocr_text: Görsel üzerindeki yazılar (varsa)
        """
        image = Image.open(image_path).convert("RGB")

        results = {}

        # 1. Detailed Caption - Genel görsel açıklaması
        prompt = "<MORE_DETAILED_CAPTION>"
        inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(
            self.device, self.torch_dtype
        )

        generated_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            num_beams=3,
        )

        detailed_caption = self.processor.batch_decode(
            generated_ids, skip_special_tokens=False
        )[0]
        results["detailed_caption"] = self._clean_florence_output(detailed_caption)

        # 2. Object Detection - Nesneleri tespit et
        prompt = "<OD>"  # Object Detection
        inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(
            self.device, self.torch_dtype
        )

        generated_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            num_beams=3,
        )

        objects_output = self.processor.batch_decode(
            generated_ids, skip_special_tokens=False
        )[0]
        results["objects"] = self._clean_florence_output(objects_output)

        # 3. Dense Region Caption - Bölgesel detaylı açıklamalar
        prompt = "<DENSE_REGION_CAPTION>"
        inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(
            self.device, self.torch_dtype
        )

        generated_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            num_beams=3,
        )

        dense_caption = self.processor.batch_decode(
            generated_ids, skip_special_tokens=False
        )[0]
        results["dense_captions"] = self._clean_florence_output(dense_caption)

        # 4. OCR - Metin tespiti (etiket, logo vb. için önemli)
        prompt = "<OCR>"
        inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(
            self.device, self.torch_dtype
        )

        generated_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            num_beams=3,
        )

        ocr_output = self.processor.batch_decode(
            generated_ids, skip_special_tokens=False
        )[0]
        results["ocr_text"] = self._clean_florence_output(ocr_output)

        return results

    def _clean_florence_output(self, output: str) -> str:
        """Florence-2 çıktısını temizle"""
        # Florence-2 special token'ları temizle
        output = output.replace("</s>", "").strip()
        return output

    def generate_product_description(
        self,
        image_path: str,
        product_category: str = "fashion",
        brand_voice: str = "premium ve şık",
        additional_context: str = None
    ) -> str:
        """
        Görsel analizi yapıp, Claude ile profesyonel ürün açıklaması oluştur

        Args:
            image_path: Ürün görseli yolu
            product_category: Ürün kategorisi (fashion, electronics, vb.)
            brand_voice: Marka tonu (premium, casual, sporty vb.)
            additional_context: Ek bilgi (renk, malzeme vb.)

        Returns:
            Ürün açıklaması
        """
        print(f"Görsel analiz ediliyor: {image_path}")

        # Florence-2 ile görsel analizi
        visual_analysis = self.analyze_image_with_florence(image_path)

        print("Görsel analizi tamamlandı, açıklama üretiliyor...")

        # Claude ile açıklama üret
        prompt = self._build_description_prompt(
            visual_analysis,
            product_category,
            brand_voice,
            additional_context
        )

        response = self.claude_client.messages.create(
            model="claude-sonnet-4-0",  # veya claude-opus-4-0
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        description = response.content[0].text

        return description, visual_analysis

    def _build_description_prompt(
        self,
        visual_analysis: Dict,
        product_category: str,
        brand_voice: str,
        additional_context: str
    ) -> str:
        """Claude için prompt oluştur"""

        prompt = f"""Sen profesyonel bir e-ticaret içerik yazarısın. Aşağıdaki görsel analiz verilerine dayanarak, {brand_voice} tonunda bir ürün açıklaması oluştur.

## Görsel Analiz Verileri:

### Detaylı Görsel Açıklaması:
{visual_analysis['detailed_caption']}

### Tespit Edilen Nesneler:
{visual_analysis['objects']}

### Bölgesel Detaylar:
{visual_analysis['dense_captions']}

### Görsel Üzerindeki Yazılar:
{visual_analysis['ocr_text']}

## Ürün Bilgileri:
- Kategori: {product_category}
- Marka Tonu: {brand_voice}
{f"- Ek Bilgi: {additional_context}" if additional_context else ""}

## Görev:
W Collection için çekici, detaylı ve SEO-uyumlu bir ürün açıklaması yaz. Açıklama şunları içermeli:

1. **Başlık/Özet** (1-2 cümle): Ürünün ana özelliği ve çekiciliği
2. **Detaylı Açıklama** (2-3 paragraf):
   - Görsel özellikleri (renk, desen, kesim, stil)
   - Malzeme ve kalite ipuçları (görsel analizden çıkarım yaparak)
   - Kullanım senaryoları ve stil önerileri
3. **Öne Çıkan Özellikler** (bullet points)

Türkçe yaz ve ürün açıklaması doğal, akıcı ve satış odaklı olsun.
"""

        return prompt


# Kullanım örneği
if __name__ == "__main__":
    # Generator'ı başlat
    generator = ProductDescriptionGenerator()

    # Örnek kullanım
    image_path = "product_image.jpg"  # Ürün görseli yolu

    description, analysis = generator.generate_product_description(
        image_path=image_path,
        product_category="kadın giyim",
        brand_voice="modern ve şık",
        additional_context="2024 İlkbahar/Yaz koleksiyonu"
    )

    print("\n" + "="*80)
    print("ÜRÜN AÇIKLAMASI:")
    print("="*80)
    print(description)
    print("\n" + "="*80)
    print("GÖRSEL ANALİZ DETAYLARI:")
    print("="*80)
    for key, value in analysis.items():
        print(f"\n{key.upper()}:")
        print(value)
