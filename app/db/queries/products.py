GET_ALL_PRODUCTS = """
SELECT *
FROM analytic_shop.products
"""

GET_BY_ID_PRODUCT = """
SELECT *
FROM analytic_shop.products
WHERE id=$1
"""

CREATE_PRODUCT = """
INSERT INTO analytic_shop.products
(name, description, code, characteristic, rating, category)
VALUES
($1, $2, $3, $4, $5, $6)
RETURNING *
"""

UPDATE_BY_ID_PRODUCT = """
UPDATE analytic_shop.products
SET name = $2, description = $3, code = $4, characteristic = $5, rating = $6, category = $7
WHERE id = $1
RETURNING *
"""

DELETE_BY_ID_PRODUCT = """
DELETE FROM analytic_shop.products
WHERE id = $1
RETURNING *
"""
