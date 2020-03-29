-- :name total_amt :many
select cast(sum(total) as int) as total_amt from invoices limit 1