"""
W Collection için toplu ürün açıklaması üretici
"""
import os
import json
from pathlib import Path
from typing import List, Dict
from tqdm import tqdm
from florence_product_description import ProductDescriptionGenerator
import pandas as pd


class BatchProductDescriptionGenerator:
    def __init__(self):
        self.generator = ProductDescriptionGenerator()

    def process_folder(
        self,
        input_folder: str,
        output_file: str = "product_descriptions.json",
        product_category: str = "fashion",
        brand_voice: str = "premium ve şık"
    ) -> List[Dict]:
        """
        Klasördeki tüm görseller için açıklama üret

        Args:
            input_folder: Ürün görsellerinin bulunduğu klasör
            output_file: Çıktı dosyası (JSON veya CSV)
            product_category: Ürün kategorisi
            brand_voice: Marka tonu

        Returns:
            Ürün açıklamaları listesi
        """
        image_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        image_files = [
            f for f in Path(input_folder).iterdir()
            if f.suffix.lower() in image_extensions
        ]

        print(f"Toplam {len(image_files)} görsel bulundu.")

        results = []

        for image_path in tqdm(image_files, desc="Açıklamalar üretiliyor"):
            try:
                description, analysis = self.generator.generate_product_description(
                    image_path=str(image_path),
                    product_category=product_category,
                    brand_voice=brand_voice
                )

                result = {
                    "image_name": image_path.name,
                    "image_path": str(image_path),
                    "description": description,
                    "visual_analysis": analysis,
                    "status": "success"
                }

                results.append(result)

                print(f"✓ {image_path.name} tamamlandı")

            except Exception as e:
                print(f"✗ {image_path.name} işlenirken hata: {str(e)}")
                results.append({
                    "image_name": image_path.name,
                    "image_path": str(image_path),
                    "error": str(e),
                    "status": "failed"
                })

        # Sonuçları kaydet
        self._save_results(results, output_file)

        return results

    def process_with_metadata(
        self,
        metadata_file: str,
        image_folder: str,
        output_file: str = "product_descriptions_with_metadata.json"
    ) -> List[Dict]:
        """
        Metadata dosyası ile birlikte işle (CSV veya JSON)

        Metadata dosyası formatı:
        - image_name: Görsel dosya adı
        - category: Ürün kategorisi (opsiyonel)
        - brand_voice: Marka tonu (opsiyonel)
        - additional_context: Ek bilgiler (renk, malzeme vb.)
        """
        # Metadata oku
        if metadata_file.endswith('.csv'):
            metadata_df = pd.read_csv(metadata_file)
            metadata = metadata_df.to_dict('records')
        else:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

        results = []

        for item in tqdm(metadata, desc="Açıklamalar üretiliyor"):
            image_name = item['image_name']
            image_path = os.path.join(image_folder, image_name)

            if not os.path.exists(image_path):
                print(f"✗ {image_name} bulunamadı, atlanıyor...")
                continue

            try:
                description, analysis = self.generator.generate_product_description(
                    image_path=image_path,
                    product_category=item.get('category', 'fashion'),
                    brand_voice=item.get('brand_voice', 'premium ve şık'),
                    additional_context=item.get('additional_context')
                )

                result = {
                    **item,  # Orijinal metadata
                    "description": description,
                    "visual_analysis": analysis,
                    "status": "success"
                }

                results.append(result)
                print(f"✓ {image_name} tamamlandı")

            except Exception as e:
                print(f"✗ {image_name} işlenirken hata: {str(e)}")
                results.append({
                    **item,
                    "error": str(e),
                    "status": "failed"
                })

        # Sonuçları kaydet
        self._save_results(results, output_file)

        return results

    def _save_results(self, results: List[Dict], output_file: str):
        """Sonuçları kaydet"""
        if output_file.endswith('.csv'):
            # CSV için visual_analysis'i JSON string yap
            df_results = []
            for r in results:
                r_copy = r.copy()
                if 'visual_analysis' in r_copy:
                    r_copy['visual_analysis'] = json.dumps(
                        r_copy['visual_analysis'],
                        ensure_ascii=False
                    )
                df_results.append(r_copy)

            df = pd.DataFrame(df_results)
            df.to_csv(output_file, index=False, encoding='utf-8')
        else:
            # JSON olarak kaydet
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Sonuçlar kaydedildi: {output_file}")


# Kullanım örnekleri
if __name__ == "__main__":
    batch_generator = BatchProductDescriptionGenerator()

    # Örnek 1: Sadece klasör ile toplu işlem
    print("=" * 80)
    print("ÖRNEK 1: Klasördeki tüm görseller için açıklama üret")
    print("=" * 80)

    results = batch_generator.process_folder(
        input_folder="./product_images",
        output_file="w_collection_descriptions.json",
        product_category="kadın giyim",
        brand_voice="modern, şık ve özgüvenli"
    )

    print(f"\nToplam {len(results)} ürün işlendi")
    success_count = sum(1 for r in results if r['status'] == 'success')
    print(f"Başarılı: {success_count}/{len(results)}")

    # Örnek 2: Metadata dosyası ile toplu işlem
    print("\n" + "=" * 80)
    print("ÖRNEK 2: Metadata dosyası ile toplu işlem")
    print("=" * 80)

    # Önce örnek metadata oluştur
    example_metadata = [
        {
            "image_name": "product_001.jpg",
            "category": "elbise",
            "brand_voice": "zarif ve kadınsı",
            "additional_context": "Siyah, midi boy, kolsuz, akşam etkinlikleri için"
        },
        {
            "image_name": "product_002.jpg",
            "category": "bluz",
            "brand_voice": "modern ve rahat",
            "additional_context": "Beyaz, pamuklu, günlük kullanım"
        }
    ]

    with open("product_metadata.json", 'w', encoding='utf-8') as f:
        json.dump(example_metadata, f, ensure_ascii=False, indent=2)

    print("Örnek metadata dosyası oluşturuldu: product_metadata.json")

    # Metadata ile işle
    # results = batch_generator.process_with_metadata(
    #     metadata_file="product_metadata.json",
    #     image_folder="./product_images",
    #     output_file="w_collection_with_metadata.json"
    # )
