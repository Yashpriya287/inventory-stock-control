
-- STOCK MOVEMENT VALIDATION
CREATE TRIGGER check_user_location_access
BEFORE INSERT ON stock_movements
FOR EACH ROW
EXECUTE FUNCTION validate_user_location_access();


CREATE TRIGGER check_negative_stock
BEFORE INSERT ON stock_movements
FOR EACH ROW
EXECUTE FUNCTION prevent_negative_stock();

-- ITEM HISTORY IMMUTABILITY

CREATE TRIGGER prevent_item_history_update
BEFORE UPDATE ON item_history
FOR EACH ROW
EXECUTE FUNCTION prevent_item_history_changes();

CREATE TRIGGER prevent_item_history_delete
BEFORE DELETE ON item_history
FOR EACH ROW
EXECUTE FUNCTION prevent_item_history_changes();

-- STOCK MOVEMENT IMMUTABILITY

CREATE TRIGGER prevent_stock_movement_update
BEFORE UPDATE ON stock_movements
FOR EACH ROW
EXECUTE FUNCTION prevent_stock_movement_changes();

CREATE TRIGGER prevent_stock_movement_delete
BEFORE DELETE ON stock_movements
FOR EACH ROW
EXECUTE FUNCTION prevent_stock_movement_changes();

-- AUTOMATIC UPDATED_AT TIMESTAMPS

CREATE TRIGGER items_set_updated_at
BEFORE UPDATE ON items
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();


CREATE TRIGGER low_stock_alerts_set_updated_at
BEFORE UPDATE ON low_stock_alerts
FOR EACH ROW
EXECUTE FUNCTION set_updated_at();