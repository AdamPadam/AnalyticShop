GET_ALL_GROUPS = """
SELECT *
FROM analytic_shop.groups
"""

GET_BY_ID_GROUP = """
SELECT *
FROM analytic_shop.groups
WHERE id=$1
"""

CREATE_GROUP = """
INSERT INTO analytic_shop.groups
(name, permission_type)
VALUES
($1, $2)
RETURNING *
"""

UPDATE_BY_ID_GROUP = """
UPDATE analytic_shop.groups
SET name = $2, permission_type = $3
WHERE id = $1
RETURNING *
"""

DELETE_BY_ID_GROUP = """
DELETE FROM analytic_shop.groups
WHERE id = $1
RETURNING *
"""
