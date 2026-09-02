CREATE OR REPLACE FUNCTION update_item(
    p_item_id UUID,
    p_sku VARCHAR,
    p_name VARCHAR,
    p_description TEXT,
    p_unit_of_measure VARCHAR,
    p_reorder_level NUMERIC,
    p_category_id UUID,
    p_performed_by UUID
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE
    v_old_item items%ROWTYPE;
BEGIN

    -- Get the current item before updating
    SELECT *
    INTO v_old_item
    FROM items
    WHERE id = p_item_id;

    -- Make sure the item exists
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Item not found.';
    END IF;


    -- Update the item
    UPDATE items
    SET
        sku = p_sku,
        name = p_name,
        description = p_description,
        unit_of_measure = p_unit_of_measure,
        reorder_level = p_reorder_level,
        category_id = p_category_id
    WHERE id = p_item_id;


    -- Record SKU change
    IF v_old_item.sku IS DISTINCT FROM p_sku THEN
        INSERT INTO item_history (
            item_id,
            event_type,
            field_name,
            old_value,
            new_value,
            performed_by
        )
        VALUES (
            p_item_id,
            'updated',
            'sku',
            to_jsonb(v_old_item.sku),
            to_jsonb(p_sku),
            p_performed_by
        );
    END IF;


    -- Record name change
    IF v_old_item.name IS DISTINCT FROM p_name THEN
        INSERT INTO item_history (
            item_id,
            event_type,
            field_name,
            old_value,
            new_value,
            performed_by
        )
        VALUES (
            p_item_id,
            'updated',
            'name',
            to_jsonb(v_old_item.name),
            to_jsonb(p_name),
            p_performed_by
        );
    END IF;


    -- Record description change
    IF v_old_item.description IS DISTINCT FROM p_description THEN
        INSERT INTO item_history (
            item_id,
            event_type,
            field_name,
            old_value,
            new_value,
            performed_by
        )
        VALUES (
            p_item_id,
            'updated',
            'description',
            to_jsonb(v_old_item.description),
            to_jsonb(p_description),
            p_performed_by
        );
    END IF;


    -- Record unit of measure change
    IF v_old_item.unit_of_measure IS DISTINCT FROM p_unit_of_measure THEN
        INSERT INTO item_history (
            item_id,
            event_type,
            field_name,
            old_value,
            new_value,
            performed_by
        )
        VALUES (
            p_item_id,
            'updated',
            'unit_of_measure',
            to_jsonb(v_old_item.unit_of_measure),
            to_jsonb(p_unit_of_measure),
            p_performed_by
        );
    END IF;


    -- Record reorder level change
    IF v_old_item.reorder_level IS DISTINCT FROM p_reorder_level THEN
        INSERT INTO item_history (
            item_id,
            event_type,
            field_name,
            old_value,
            new_value,
            performed_by
        )
        VALUES (
            p_item_id,
            'updated',
            'reorder_level',
            to_jsonb(v_old_item.reorder_level),
            to_jsonb(p_reorder_level),
            p_performed_by
        );
    END IF;


    -- Record category change
    IF v_old_item.category_id IS DISTINCT FROM p_category_id THEN
        INSERT INTO item_history (
            item_id,
            event_type,
            field_name,
            old_value,
            new_value,
            performed_by
        )
        VALUES (
            p_item_id,
            'updated',
            'category_id',
            to_jsonb(v_old_item.category_id),
            to_jsonb(p_category_id),
            p_performed_by
        );
    END IF;

END;
$$;



CREATE OR REPLACE FUNCTION prevent_negative_stock()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    available_stock NUMERIC(12, 2);
    stock_location_id UUID;
BEGIN

    -- ISSUE OR DECREASE ADJUSTMENT
    IF NEW.movement_type = 'issue'
       OR (
           NEW.movement_type = 'adjustment'
           AND NEW.adjustment_direction = 'decrease'
       ) THEN

        stock_location_id := NEW.location_id;

    -- TRANSFER: CHECK THE SOURCE LOCATION
    ELSIF NEW.movement_type = 'transfer' THEN

        stock_location_id := NEW.source_location_id;

    -- RECEIPT AND INCREASE ADJUSTMENT DO NOT REDUCE STOCK
    ELSE
        RETURN NEW;

    END IF;


    -- GET CURRENT STOCK AT THE RELEVANT LOCATION
    SELECT COALESCE(quantity_on_hand, 0)
    INTO available_stock
    FROM current_stock_by_location
    WHERE item_id = NEW.item_id
      AND location_id = stock_location_id;


    -- PREVENT NEGATIVE STOCK
    IF NEW.quantity > COALESCE(available_stock, 0) THEN
        RAISE EXCEPTION
            'Insufficient stock. Available: %, Requested: %',
            COALESCE(available_stock, 0),
            NEW.quantity;
    END IF;

    RETURN NEW;
END;
$$;




CREATE OR REPLACE FUNCTION validate_user_location_access()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN

    -- RECEIPT, ISSUE, OR ADJUSTMENT
    IF NEW.movement_type IN ('receipt', 'issue', 'adjustment') THEN

        IF NOT EXISTS (
            SELECT 1
            FROM user_locations
            WHERE user_id = NEW.recorded_by
              AND location_id = NEW.location_id
        ) THEN
            RAISE EXCEPTION
                'User does not have access to this location.';
        END IF;

    -- TRANSFER
    ELSIF NEW.movement_type = 'transfer' THEN

        IF NOT EXISTS (
            SELECT 1
            FROM user_locations
            WHERE user_id = NEW.recorded_by
              AND location_id = NEW.source_location_id
        ) THEN
            RAISE EXCEPTION
                'User does not have access to the source location.';
        END IF;

        IF NOT EXISTS (
            SELECT 1
            FROM user_locations
            WHERE user_id = NEW.recorded_by
              AND location_id = NEW.destination_location_id
        ) THEN
            RAISE EXCEPTION
                'User does not have access to the destination location.';
        END IF;

    END IF;

    RETURN NEW;
END;
$$;


CREATE OR REPLACE FUNCTION prevent_item_history_changes()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE EXCEPTION
        'Item history is immutable and cannot be modified or deleted.';
END;
$$;



CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;



CREATE OR REPLACE FUNCTION prevent_stock_movement_changes()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    RAISE EXCEPTION
        'Stock movements are immutable. Create a new corrective movement instead.';
END;
$$;