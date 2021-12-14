GET_ALL_WISHLISTS = """
SELECT *
FROM analytic_shop.wishlist_items
"""

GET_BY_ID_WISHLIST = """
SELECT *
FROM analytic_shop.feedbacks
WHERE id=$1
"""

CREATE_WISHLIST = """
INSERT INTO analytic_shop.wishlist_items
(user_id, product_id)
VALUES
($1, $2)
RETURNING *
"""

UPDATE_BY_ID_WISHLIST = """
UPDATE analytic_shop.wishlist_items
SET user_id = $2, product_id = $3
WHERE id = $1
RETURNING *
"""

DELETE_BY_ID_WISHLIST = """
DELETE FROM analytic_shop.wishlist_items
WHERE id = $1
RETURNING *
"""
