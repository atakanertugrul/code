-- Sales Database Schema (Turkish Retail Sales Data)

CREATE TABLE IF NOT EXISTS sales (
    -- Transaction identifiers
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,

    -- Time dimensions
    yearmonth TEXT NOT NULL,          -- Format: 'YYYYMM' (e.g., '202501')
    tx_date DATE NOT NULL,             -- Transaction date: YYYY-MM-DD

    -- Financial data
    net_amount DECIMAL(10, 2) NOT NULL,  -- Net transaction amount in TL
    discount_rate DECIMAL(5, 4),         -- Discount rate (0-1 or percentage)

    -- Discount information
    season_discount TEXT,                -- Discount type: 'Discount', 'No Discount', etc.
    season_statues TEXT,                 -- Season status: 'Season', 'OffSeason', etc.

    -- Store and channel information
    store_name TEXT,                     -- Store name (e.g., 'V.Butik GAZİANTEP PRIME MALL')
    f_online_tx INTEGER DEFAULT 0,      -- 0 = offline (store), 1 = online transaction
    tx_city TEXT,                        -- Transaction city

    -- Product information
    product_brand_name TEXT,             -- Product brand: 'VAKKO', 'VAKKORAMA', etc.
    product_type TEXT,                   -- Product type: 'Kazak', 'Gömlek', 'Pantolon', etc.
    product_category TEXT,               -- Category: 'Giyim', 'Aksesuar', etc.
    product_subcategory TEXT,            -- Subcategory: 'Üst Giyim', 'Alt Giyim', etc.
    product_class TEXT,                  -- Product class: 'Normal', 'Outlet', etc.
    material TEXT,                       -- Material: 'Modal', 'Cotton', 'Silk', etc.
    sap_mal_grubu_tanim TEXT,           -- SAP material group definition

    -- Customer information
    customer_age_segment TEXT,           -- Age segment: '18-24', '25-34', etc.
    customer_gender TEXT,                -- Gender: 'Male', 'Female', etc.
    customer_segment TEXT                -- Brand segment: 'Vakko', 'Vakko Butik', etc.
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_customer_id ON sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_yearmonth ON sales(yearmonth);
CREATE INDEX IF NOT EXISTS idx_tx_date ON sales(tx_date);
CREATE INDEX IF NOT EXISTS idx_store_name ON sales(store_name);
CREATE INDEX IF NOT EXISTS idx_product_brand ON sales(product_brand_name);
CREATE INDEX IF NOT EXISTS idx_online_tx ON sales(f_online_tx);
CREATE INDEX IF NOT EXISTS idx_tx_city ON sales(tx_city);
