"""
Florence-2 Model - Tüm Task'lar ve Kullanım Örnekleri
Microsoft Florence-2 ile yapabileceğiniz tüm görsel analiz görevleri
"""

from PIL import Image
import torch
from transformers import AutoModelForCausalLM, AutoProcessor


class Florence2TaskReference:
    """Florence-2'nin tüm yetenekleri için referans"""

    TASKS = {
        # CAPTION TASKS
        "<CAPTION>": {
            "description": "Basit görsel açıklaması",
            "use_case": "Hızlı, kısa görsel özetleri",
            "example_output": "A woman wearing a black dress"
        },
        "<DETAILED_CAPTION>": {
            "description": "Detaylı görsel açıklaması",
            "use_case": "Daha kapsamlı görsel açıklamaları",
            "example_output": "A young woman wearing an elegant black midi dress standing in a studio setting"
        },
        "<MORE_DETAILED_CAPTION>": {
            "description": "Çok detaylı görsel açıklaması",
            "use_case": "En kapsamlı görsel analizi - ÜRÜN AÇIKLAMALARI İÇİN İDEAL",
            "example_output": "A professional photograph of a woman modeling a black sleeveless midi dress with a fitted silhouette, standing against a white background in a studio setting. The dress features clean lines and a sophisticated cut."
        },

        # OBJECT DETECTION
        "<OD>": {
            "description": "Object Detection - Nesne tespiti",
            "use_case": "Görseldeki nesneleri tespit etme",
            "example_output": "dress, person, zipper, fabric"
        },
        "<DENSE_REGION_CAPTION>": {
            "description": "Bölgesel detaylı açıklamalar",
            "use_case": "Görselin farklı bölgeleri için ayrı açıklamalar",
            "example_output": "Region 1: elegant neckline, Region 2: fitted waist, Region 3: flowing skirt"
        },
        "<REGION_PROPOSAL>": {
            "description": "İlgi bölgesi önerileri",
            "use_case": "Önemli bölgelerin konumlarını bulma",
            "example_output": "Bounding box coordinates for regions of interest"
        },

        # OCR TASKS
        "<OCR>": {
            "description": "OCR - Metin okuma",
            "use_case": "Görseldeki yazıları okuma (logo, etiket vb.)",
            "example_output": "W Collection, Size: M, 100% Cotton"
        },
        "<OCR_WITH_REGION>": {
            "description": "Konumlu OCR",
            "use_case": "Metinleri ve konumlarını bulma",
            "example_output": "Text with bounding box coordinates"
        },

        # REFERRING TASKS
        "<CAPTION_TO_PHRASE_GROUNDING>": {
            "description": "Açıklamayı bölgelere bağlama",
            "use_case": "Belirli ifadelerin görselde nerede olduğunu bulma",
            "input_example": "the dress",
            "example_output": "Bounding box for 'dress' in the image"
        },
        "<REFERRING_EXPRESSION_SEGMENTATION>": {
            "description": "İfade bazlı segmentasyon",
            "use_case": "Açıklamaya göre nesne segmentasyonu",
            "input_example": "the black dress",
            "example_output": "Segmentation mask for the dress"
        },

        # REGION TASKS
        "<REGION_TO_SEGMENTATION>": {
            "description": "Bölgeyi segmentlere ayırma",
            "use_case": "Belirli bir bölgedeki nesneleri ayırma",
            "example_output": "Segmentation mask for specified region"
        },
        "<REGION_TO_CATEGORY>": {
            "description": "Bölge kategorizasyonu",
            "use_case": "Belirli bir bölgedeki nesnenin kategorisini bulma",
            "example_output": "clothing, dress"
        },
        "<REGION_TO_DESCRIPTION>": {
            "description": "Bölge açıklaması",
            "use_case": "Belirli bir bölgeyi detaylı açıklama",
            "example_output": "A fitted black dress with elegant design"
        }
    }

    def __init__(self, model_id="microsoft/Florence-2-base"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if self.device == "cuda" else torch.float32

        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype=self.torch_dtype,
            trust_remote_code=True,
        ).to(self.device)

        self.processor = AutoProcessor.from_pretrained(
            model_id,
            trust_remote_code=True,
        )

    def run_task(self, image_path: str, task: str, text_input: str = None):
        """
        Florence-2 task'ını çalıştır

        Args:
            image_path: Görsel yolu
            task: Task kodu (örn: "<MORE_DETAILED_CAPTION>")
            text_input: Bazı task'lar için ek metin girişi

        Returns:
            Task çıktısı
        """
        image = Image.open(image_path).convert("RGB")

        # Prompt oluştur
        if text_input:
            prompt = task + text_input
        else:
            prompt = task

        inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(
            self.device, self.torch_dtype
        )

        generated_ids = self.model.generate(
            input_ids=inputs["input_ids"],
            pixel_values=inputs["pixel_values"],
            max_new_tokens=1024,
            num_beams=3,
        )

        result = self.processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

        return self._clean_output(result)

    def _clean_output(self, output: str) -> str:
        """Çıktıyı temizle"""
        return output.replace("</s>", "").strip()

    def print_all_tasks(self):
        """Tüm task'ları listele"""
        print("=" * 80)
        print("FLORENCE-2 TÜM TASK'LAR")
        print("=" * 80)

        for task, info in self.TASKS.items():
            print(f"\n📌 {task}")
            print(f"   Açıklama: {info['description']}")
            print(f"   Kullanım: {info['use_case']}")
            print(f"   Örnek Çıktı: {info['example_output']}")
            if 'input_example' in info:
                print(f"   Örnek Girdi: {info['input_example']}")

    def demo_all_tasks(self, image_path: str):
        """Tüm task'ları bir görsel üzerinde dene"""
        print(f"\n🖼️  Görsel: {image_path}\n")

        # Caption tasks
        print("\n" + "=" * 80)
        print("CAPTION TASKS")
        print("=" * 80)

        for task in ["<CAPTION>", "<DETAILED_CAPTION>", "<MORE_DETAILED_CAPTION>"]:
            result = self.run_task(image_path, task)
            print(f"\n{task}:")
            print(f"→ {result}")

        # Object detection
        print("\n" + "=" * 80)
        print("OBJECT DETECTION")
        print("=" * 80)

        result = self.run_task(image_path, "<OD>")
        print(f"\n<OD>:")
        print(f"→ {result}")

        # Dense captions
        print("\n" + "=" * 80)
        print("DENSE REGION CAPTIONS")
        print("=" * 80)

        result = self.run_task(image_path, "<DENSE_REGION_CAPTION>")
        print(f"\n<DENSE_REGION_CAPTION>:")
        print(f"→ {result}")

        # OCR
        print("\n" + "=" * 80)
        print("OCR (Metin Okuma)")
        print("=" * 80)

        result = self.run_task(image_path, "<OCR>")
        print(f"\n<OCR>:")
        print(f"→ {result}")


# ÜRÜN AÇIKLAMASI İÇİN BEST PRACTICE KOMBINASYON
def best_practice_for_product_description(image_path: str):
    """
    Ürün açıklaması için en iyi task kombinasyonu
    """
    florence = Florence2TaskReference()

    print("\n" + "=" * 80)
    print("ÜRÜN AÇIKLAMASI İÇİN BEST PRACTICE TASK'LAR")
    print("=" * 80)

    # 1. En detaylı caption
    print("\n1️⃣  MORE DETAILED CAPTION (Detaylı görsel açıklaması)")
    detailed = florence.run_task(image_path, "<MORE_DETAILED_CAPTION>")
    print(f"→ {detailed}")

    # 2. Object detection
    print("\n2️⃣  OBJECT DETECTION (Nesneleri tespit et)")
    objects = florence.run_task(image_path, "<OD>")
    print(f"→ {objects}")

    # 3. Dense captions
    print("\n3️⃣  DENSE REGION CAPTION (Bölgesel detaylar)")
    regions = florence.run_task(image_path, "<DENSE_REGION_CAPTION>")
    print(f"→ {regions}")

    # 4. OCR
    print("\n4️⃣  OCR (Logo, etiket, yazılar)")
    ocr = florence.run_task(image_path, "<OCR>")
    print(f"→ {ocr}")

    print("\n" + "=" * 80)
    print("💡 Bu 4 bilgiyi Claude/GPT'ye göndererek profesyonel açıklama oluşturun!")
    print("=" * 80)

    return {
        "detailed_caption": detailed,
        "objects": objects,
        "dense_regions": regions,
        "ocr_text": ocr
    }


if __name__ == "__main__":
    # Task'ları listele
    florence = Florence2TaskReference()
    florence.print_all_tasks()

    # Bir görsel üzerinde tüm task'ları dene
    # florence.demo_all_tasks("product_image.jpg")

    # Best practice kombinasyon
    # best_practice_for_product_description("product_image.jpg")
