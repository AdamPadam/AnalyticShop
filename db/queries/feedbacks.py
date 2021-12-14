GET_ALL_FEEDBACKS = """
SELECT *
FROM analytic_shop.feedbacks
"""

GET_BY_ID_FEEDBACK = """
SELECT *
FROM analytic_shop.feedbacks
WHERE id=$1
"""

CREATE_FEEDBACK = """
INSERT INTO analytic_shop.feedbacks
(title, positive_msg, negative_msg, message, user_id, product_id, shop_id)
VALUES
($1, $2, $3, $4, $5, $6, $7)
RETURNING *
"""

UPDATE_BY_ID_FEEDBACK = """
UPDATE analytic_shop.feedbacks
SET title = $2, positive_msg = $3, negative_msg = $4, message = $5
WHERE id = $1
RETURNING *
"""

DELETE_BY_ID_FEEDBACK = """
DELETE FROM analytic_shop.feedbacks
WHERE id = $1
RETURNING *
"""
