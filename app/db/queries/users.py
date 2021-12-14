GET_ALL_USERS = """
SELECT *
FROM analytic_shop.users
"""

GET_BY_ID_USER = """
SELECT *
FROM analytic_shop.users
WHERE id=$1
"""

CREATE_USER = """
INSERT INTO analytic_shop.users
(username, password, first_name, last_name, birth_date)
VALUES
($1, $2, $3, $4, $5)
RETURNING *
"""

UPDATE_BY_ID_USER = """
UPDATE analytic_shop.users
SET username = $2, password = $3, first_name = $4, last_name = $5, birth_date = $6
WHERE id = $1
RETURNING *
"""

DELETE_BY_ID_USER = """
DELETE FROM analytic_shop.users
WHERE id = $1
RETURNING *
"""
