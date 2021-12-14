GET_ALL_ITEMS = """
SELECT *
FROM analytic_shop.items
"""

GET_BY_ID_ITEM = """
SELECT *
FROM analytic_shop.items
WHERE id=$1
"""

CREATE_ITEM = """
INSERT INTO analytic_shop.items
(product_id, shop_id, quantity, discount_percent, price)
VALUES
($1, $2, $3, $4, $5)
RETURNING *
"""

UPDATE_BY_ID_ITEM = """
UPDATE analytic_shop.items
SET product_id = $2, shop_id = $3, quantity = $4, discount_percent = $5, price = $6
WHERE id = $1
RETURNING *
"""

DELETE_BY_ID_ITEM = """
DELETE FROM analytic_shop.items
WHERE id = $1
RETURNING *
"""
