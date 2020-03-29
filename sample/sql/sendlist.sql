-- :name send_list :many
SELECT  LastName || ', ' || FirstName as name, email as email
FROM `employees`;