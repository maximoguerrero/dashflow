-- :name most_genre_sold :many
SELECT  g.name as label, count(1) as value
FROM `tracks` t
inner join `genres` g on g.genreid = t.genreid
group by g.genreid, g.name
order by  count(1) DESC
limit 5;