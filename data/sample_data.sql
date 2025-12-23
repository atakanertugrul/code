-- Sample Sales Data (Turkish Retail)
-- This data represents realistic sales transactions for a Turkish retail company

INSERT INTO sales (
    customer_id, yearmonth, tx_date, net_amount, discount_rate, season_discount, season_statues,
    store_name, f_online_tx, tx_city, product_brand_name, product_type, product_category,
    product_subcategory, product_class, material, sap_mal_grubu_tanim, customer_age_segment,
    customer_gender, customer_segment
) VALUES
-- January 2025 Sales
(1001, '202501', '2025-01-05', 1250.00, 0.0, 'No Discount', 'Season', 'VAKKO İSTANBUL NİŞANTAŞI', 0, 'İstanbul', 'VAKKO', 'Gömlek', 'Giyim', 'Üst Giyim', 'Normal', 'Cotton', 'Erkek Gömlek', '35-44', 'Male', 'Vakko'),
(1002, '202501', '2025-01-06', 890.00, 0.15, 'Discount', 'Season', 'VAKKO ANKARA ARMADA', 0, 'Ankara', 'VAKKO', 'Pantolon', 'Giyim', 'Alt Giyim', 'Normal', 'Wool', 'Erkek Pantolon', '45-54', 'Male', 'Vakko'),
(1003, '202501', '2025-01-08', 2340.00, 0.0, 'No Discount', 'Season', 'VAKKORAMA İZMİR OPTIMUM', 0, 'İzmir', 'VAKKORAMA', 'Elbise', 'Giyim', 'Elbise', 'Normal', 'Silk', 'Kadın Elbise', '25-34', 'Female', 'Vakko'),
(1004, '202501', '2025-01-10', 670.00, 0.20, 'Discount', 'OffSeason', 'V.Butik GAZİANTEP PRIME MALL', 0, 'Gaziantep', 'VAKKO', 'Kazak', 'Giyim', 'Üst Giyim', 'Outlet', 'Modal', 'Kadın Kazak', '18-24', 'Female', 'Vakko Butik'),
(1005, '202501', '2025-01-12', 1890.00, 0.0, 'No Discount', 'Season', 'VAKKO ONLINE', 1, 'İstanbul', 'VAKKO', 'Ceket', 'Giyim', 'Üst Giyim', 'Normal', 'Leather', 'Erkek Ceket', '35-44', 'Male', 'Vakko'),
(1006, '202501', '2025-01-15', 450.00, 0.10, 'Discount', 'Season', 'VAKKO BURSA ZAFER PLAZA', 0, 'Bursa', 'VAKKORAMA', 'Bluz', 'Giyim', 'Üst Giyim', 'Normal', 'Cotton', 'Kadın Bluz', '25-34', 'Female', 'Vakko'),
(1001, '202501', '2025-01-18', 3200.00, 0.0, 'No Discount', 'Season', 'VAKKO İSTANBUL NİŞANTAŞI', 0, 'İstanbul', 'VAKKO', 'Takım Elbise', 'Giyim', 'Takım', 'Normal', 'Wool', 'Erkek Takım', '35-44', 'Male', 'Vakko'),
(1007, '202501', '2025-01-20', 560.00, 0.25, 'Discount', 'OffSeason', 'V.Butik ANTALYA MIGROS', 0, 'Antalya', 'VAKKO', 'Şapka', 'Aksesuar', 'Aksesuar', 'Outlet', 'Cotton', 'Aksesuar', '45-54', 'Male', 'Vakko Butik'),
(1008, '202501', '2025-01-22', 1120.00, 0.0, 'No Discount', 'Season', 'VAKKO ONLINE', 1, 'Ankara', 'VAKKORAMA', 'Etek', 'Giyim', 'Alt Giyim', 'Normal', 'Polyester', 'Kadın Etek', '25-34', 'Female', 'Vakko'),
(1009, '202501', '2025-01-25', 780.00, 0.15, 'Discount', 'Season', 'VAKKO ADANA OPTIMUM', 0, 'Adana', 'VAKKO', 'Gömlek', 'Giyim', 'Üst Giyim', 'Normal', 'Cotton', 'Erkek Gömlek', '35-44', 'Male', 'Vakko'),

-- February 2025 Sales
(1002, '202502', '2025-02-01', 2100.00, 0.0, 'No Discount', 'Season', 'VAKKO ANKARA ARMADA', 0, 'Ankara', 'VAKKO', 'Palto', 'Giyim', 'Üst Giyim', 'Normal', 'Cashmere', 'Erkek Palto', '45-54', 'Male', 'Vakko'),
(1010, '202502', '2025-02-03', 890.00, 0.20, 'Discount', 'Season', 'VAKKORAMA İSTANBUL ZORLU', 0, 'İstanbul', 'VAKKORAMA', 'Triko', 'Giyim', 'Üst Giyim', 'Normal', 'Wool', 'Kadın Triko', '25-34', 'Female', 'Vakko'),
(1003, '202502', '2025-02-05', 1450.00, 0.0, 'No Discount', 'Season', 'VAKKO ONLINE', 1, 'İzmir', 'VAKKO', 'Ayakkabı', 'Aksesuar', 'Ayakkabı', 'Normal', 'Leather', 'Erkek Ayakkabı', '35-44', 'Male', 'Vakko'),
(1011, '202502', '2025-02-08', 670.00, 0.30, 'Discount', 'OffSeason', 'V.Butik KONYA M1', 0, 'Konya', 'VAKKO', 'Şort', 'Giyim', 'Alt Giyim', 'Outlet', 'Cotton', 'Erkek Şort', '18-24', 'Male', 'Vakko Butik'),
(1012, '202502', '2025-02-10', 1780.00, 0.0, 'No Discount', 'Season', 'VAKKO İZMİR ALSANCAK', 0, 'İzmir', 'VAKKORAMA', 'Elbise', 'Giyim', 'Elbise', 'Normal', 'Silk', 'Kadın Elbise', '25-34', 'Female', 'Vakko'),
(1004, '202502', '2025-02-12', 920.00, 0.10, 'Discount', 'Season', 'VAKKO ONLINE', 1, 'Gaziantep', 'VAKKO', 'Kazak', 'Giyim', 'Üst Giyim', 'Normal', 'Modal', 'Kadın Kazak', '18-24', 'Female', 'Vakko'),
(1013, '202502', '2025-02-15', 3400.00, 0.0, 'No Discount', 'Season', 'VAKKO İSTANBUL İSTİNYE PARK', 0, 'İstanbul', 'VAKKO', 'Takım Elbise', 'Giyim', 'Takım', 'Normal', 'Wool', 'Erkek Takım', '45-54', 'Male', 'Vakko'),
(1014, '202502', '2025-02-18', 1230.00, 0.15, 'Discount', 'Season', 'VAKKORAMA ANKARA CEPA', 0, 'Ankara', 'VAKKORAMA', 'Ceket', 'Giyim', 'Üst Giyim', 'Normal', 'Polyester', 'Kadın Ceket', '35-44', 'Female', 'Vakko'),
(1015, '202502', '2025-02-20', 560.00, 0.25, 'Discount', 'OffSeason', 'V.Butik İZMİR FORUM BORNOVA', 0, 'İzmir', 'VAKKO', 'Kemer', 'Aksesuar', 'Aksesuar', 'Outlet', 'Leather', 'Aksesuar', '25-34', 'Male', 'Vakko Butik'),
(1005, '202502', '2025-02-22', 1890.00, 0.0, 'No Discount', 'Season', 'VAKKO BURSA ZAFER PLAZA', 0, 'Bursa', 'VAKKO', 'Gömlek', 'Giyim', 'Üst Giyim', 'Normal', 'Cotton', 'Erkek Gömlek', '35-44', 'Male', 'Vakko'),

-- March 2025 Sales
(1016, '202503', '2025-03-01', 2340.00, 0.0, 'No Discount', 'Season', 'VAKKO ONLINE', 1, 'İstanbul', 'VAKKORAMA', 'Elbise', 'Giyim', 'Elbise', 'Normal', 'Silk', 'Kadın Elbise', '25-34', 'Female', 'Vakko'),
(1017, '202503', '2025-03-03', 780.00, 0.20, 'Discount', 'Season', 'VAKKO ANTALYA 5M MIGROS', 0, 'Antalya', 'VAKKO', 'Pantolon', 'Giyim', 'Alt Giyim', 'Normal', 'Cotton', 'Erkek Pantolon', '35-44', 'Male', 'Vakko'),
(1006, '202503', '2025-03-05', 1120.00, 0.0, 'No Discount', 'Season', 'VAKKORAMA İZMİR OPTIMUM', 0, 'İzmir', 'VAKKORAMA', 'Bluz', 'Giyim', 'Üst Giyim', 'Normal', 'Silk', 'Kadın Bluz', '25-34', 'Female', 'Vakko'),
(1018, '202503', '2025-03-08', 450.00, 0.30, 'Discount', 'OffSeason', 'V.Butik ADANA OPTIMUM', 0, 'Adana', 'VAKKO', 'Tişört', 'Giyim', 'Üst Giyim', 'Outlet', 'Cotton', 'Erkek Tişört', '18-24', 'Male', 'Vakko Butik'),
(1019, '202503', '2025-03-10', 1670.00, 0.0, 'No Discount', 'Season', 'VAKKO ANKARA ARMADA', 0, 'Ankara', 'VAKKO', 'Ceket', 'Giyim', 'Üst Giyim', 'Normal', 'Leather', 'Kadın Ceket', '35-44', 'Female', 'Vakko'),
(1020, '202503', '2025-03-12', 890.00, 0.15, 'Discount', 'Season', 'VAKKO ONLINE', 1, 'İzmir', 'VAKKORAMA', 'Etek', 'Giyim', 'Alt Giyim', 'Normal', 'Polyester', 'Kadın Etek', '25-34', 'Female', 'Vakko'),
(1007, '202503', '2025-03-15', 3200.00, 0.0, 'No Discount', 'Season', 'VAKKO İSTANBUL NİŞANTAŞI', 0, 'İstanbul', 'VAKKO', 'Takım Elbise', 'Giyim', 'Takım', 'Normal', 'Wool', 'Erkek Takım', '45-54', 'Male', 'Vakko'),
(1021, '202503', '2025-03-18', 1450.00, 0.10, 'Discount', 'Season', 'VAKKORAMA ANKARA CEPA', 0, 'Ankara', 'VAKKORAMA', 'Triko', 'Giyim', 'Üst Giyim', 'Normal', 'Wool', 'Kadın Triko', '25-34', 'Female', 'Vakko'),
(1008, '202503', '2025-03-20', 670.00, 0.25, 'Discount', 'OffSeason', 'V.Butik BURSA CARREFOUR', 0, 'Bursa', 'VAKKO', 'Çanta', 'Aksesuar', 'Aksesuar', 'Outlet', 'Leather', 'Aksesuar', '35-44', 'Female', 'Vakko Butik'),
(1022, '202503', '2025-03-22', 2100.00, 0.0, 'No Discount', 'Season', 'VAKKO İZMİR ALSANCAK', 0, 'İzmir', 'VAKKO', 'Palto', 'Giyim', 'Üst Giyim', 'Normal', 'Cashmere', 'Kadın Palto', '45-54', 'Female', 'Vakko'),

-- April 2025 Sales
(1009, '202504', '2025-04-01', 560.00, 0.20, 'Discount', 'Season', 'VAKKO ONLINE', 1, 'Adana', 'VAKKO', 'Gömlek', 'Giyim', 'Üst Giyim', 'Normal', 'Cotton', 'Erkek Gömlek', '35-44', 'Male', 'Vakko'),
(1023, '202504', '2025-04-03', 1890.00, 0.0, 'No Discount', 'Season', 'VAKKORAMA İSTANBUL ZORLU', 0, 'İstanbul', 'VAKKORAMA', 'Elbise', 'Giyim', 'Elbise', 'Normal', 'Silk', 'Kadın Elbise', '25-34', 'Female', 'Vakko'),
(1010, '202504', '2025-04-05', 1230.00, 0.15, 'Discount', 'Season', 'VAKKO ANKARA ARMADA', 0, 'Ankara', 'VAKKO', 'Pantolon', 'Giyim', 'Alt Giyim', 'Normal', 'Wool', 'Erkek Pantolon', '45-54', 'Male', 'Vakko'),
(1024, '202504', '2025-04-08', 450.00, 0.30, 'Discount', 'OffSeason', 'V.Butik GAZİANTEP PRIME MALL', 0, 'Gaziantep', 'VAKKO', 'Kazak', 'Giyim', 'Üst Giyim', 'Outlet', 'Modal', 'Kadın Kazak', '18-24', 'Female', 'Vakko Butik'),
(1025, '202504', '2025-04-10', 3400.00, 0.0, 'No Discount', 'Season', 'VAKKO İSTANBUL İSTİNYE PARK', 0, 'İstanbul', 'VAKKO', 'Takım Elbise', 'Giyim', 'Takım', 'Normal', 'Wool', 'Erkek Takım', '35-44', 'Male', 'Vakko'),
(1011, '202504', '2025-04-12', 780.00, 0.10, 'Discount', 'Season', 'VAKKO ONLINE', 1, 'Konya', 'VAKKORAMA', 'Bluz', 'Giyim', 'Üst Giyim', 'Normal', 'Cotton', 'Kadın Bluz', '25-34', 'Female', 'Vakko'),
(1026, '202504', '2025-04-15', 1670.00, 0.0, 'No Discount', 'Season', 'VAKKO BURSA ZAFER PLAZA', 0, 'Bursa', 'VAKKO', 'Ceket', 'Giyim', 'Üst Giyim', 'Normal', 'Leather', 'Erkek Ceket', '45-54', 'Male', 'Vakko'),
(1012, '202504', '2025-04-18', 890.00, 0.20, 'Discount', 'Season', 'VAKKORAMA İZMİR OPTIMUM', 0, 'İzmir', 'VAKKORAMA', 'Etek', 'Giyim', 'Alt Giyim', 'Normal', 'Polyester', 'Kadın Etek', '25-34', 'Female', 'Vakko'),
(1027, '202504', '2025-04-20', 1120.00, 0.15, 'Discount', 'Season', 'VAKKO ADANA OPTIMUM', 0, 'Adana', 'VAKKO', 'Gömlek', 'Giyim', 'Üst Giyim', 'Normal', 'Cotton', 'Erkek Gömlek', '35-44', 'Male', 'Vakko'),
(1028, '202504', '2025-04-22', 2340.00, 0.0, 'No Discount', 'Season', 'VAKKO ONLINE', 1, 'Ankara', 'VAKKORAMA', 'Elbise', 'Giyim', 'Elbise', 'Normal', 'Silk', 'Kadın Elbise', '25-34', 'Female', 'Vakko');
