GET_ALL_SHOPS = """
SELECT *
FROM analytic_shop.shops
"""

GET_BY_ID_SHOP = """
SELECT *
FROM analytic_shop.shops
WHERE id=$1
"""

CREATE_SHOP = """
INSERT INTO analytic_shop.shops
(name, description, address, website, rating)
VALUES
($1, $2, $3, $4, $5)
RETURNING *
"""

UPDATE_BY_ID_SHOP = """
UPDATE analytic_shop.shops
SET name = $2, description = $3, address = $4, website = $5, rating = $6
WHERE id = $1
RETURNING *
"""

DELETE_BY_ID_SHOP = """
DELETE FROM analytic_shop.shops
WHERE id = $1
RETURNING *
"""
