CREATE TYPE user_role AS ENUM('manager','staff');

CREATE TYPE movement_type AS ENUM( 'receipt','issue','transfer','adjustment');

CREATE TYPE adjustment_direction AS ENUM ('increase', 'decrease');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'staff',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);



CREATE TABLE locations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE user_locations (
    user_id UUID NOT NULL REFERENCES users(id),
    location_id UUID NOT NULL REFERENCES locations(id),

    PRIMARY KEY (user_id, location_id)
);


CREATE TABLE items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    sku VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,

    unit_of_measure VARCHAR(50) NOT NULL,

    reorder_level NUMERIC(12, 2) NOT NULL DEFAULT 0
        CHECK (reorder_level >= 0),

    category_id UUID REFERENCES categories(id),

    is_archived BOOLEAN NOT NULL DEFAULT FALSE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE stock_movements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    item_id UUID NOT NULL
        REFERENCES items(id),

    movement_type movement_type NOT NULL,

    quantity NUMERIC(12, 2) NOT NULL
        CHECK (quantity > 0),

    location_id UUID
        REFERENCES locations(id),

    source_location_id UUID
        REFERENCES locations(id),

    destination_location_id UUID
        REFERENCES locations(id),

    adjustment_reason TEXT,
    adjustment_direction adjustment_direction,

    recorded_by UUID NOT NULL
        REFERENCES users(id),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CHECK (
        (
            movement_type IN ('receipt', 'issue', 'adjustment')
            AND location_id IS NOT NULL
            AND source_location_id IS NULL
            AND destination_location_id IS NULL
        )

        OR

        (
            movement_type = 'transfer'
            AND location_id IS NULL
            AND source_location_id IS NOT NULL
            AND destination_location_id IS NOT NULL
            AND source_location_id <> destination_location_id
        )
    ),

    CHECK (
    (
        movement_type = 'adjustment'
        AND adjustment_reason IS NOT NULL
        AND adjustment_direction IS NOT NULL
    )
    OR
    (
        movement_type <> 'adjustment'
        AND adjustment_reason IS NULL
        AND adjustment_direction IS NULL
    )
)
);


CREATE TABLE item_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    item_id UUID NOT NULL
        REFERENCES items(id),

    event_type VARCHAR(50) NOT NULL,

    field_name VARCHAR(100),

    old_value JSONB,
    new_value JSONB,

    note TEXT,

    performed_by UUID NOT NULL
        REFERENCES users(id),

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


CREATE TABLE low_stock_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    item_id UUID NOT NULL
        REFERENCES items(id),

    location_id UUID NOT NULL
        REFERENCES locations(id),

    is_dismissed BOOLEAN NOT NULL DEFAULT FALSE,

    dismissed_by UUID
        REFERENCES users(id),

    dismissed_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (item_id, location_id)
);


CREATE VIEW current_stock_by_location AS

WITH movement_effects AS (

    
    SELECT
        item_id,
        location_id,
        CASE
    WHEN movement_type = 'receipt' THEN quantity
    WHEN movement_type = 'issue' THEN -quantity
    WHEN movement_type = 'adjustment'
         AND adjustment_direction = 'increase'
    THEN quantity
    WHEN movement_type = 'adjustment'
         AND adjustment_direction = 'decrease'
    THEN -quantity
  END AS quantity_change
    FROM stock_movements
    WHERE movement_type IN ('receipt', 'issue', 'adjustment')

    UNION ALL

    -- TRANSFER REMOVES STOCK FROM SOURCE
    SELECT
        item_id,
        source_location_id AS location_id,
        -quantity AS quantity_change
    FROM stock_movements
    WHERE movement_type = 'transfer'

    UNION ALL

    -- TRANSFER ADDS STOCK TO DESTINATION
    SELECT
        item_id,
        destination_location_id AS location_id,
        quantity AS quantity_change
    FROM stock_movements
    WHERE movement_type = 'transfer'
)

SELECT
    item_id,
    location_id,
    SUM(quantity_change) AS quantity_on_hand

FROM movement_effects

GROUP BY item_id, location_id;