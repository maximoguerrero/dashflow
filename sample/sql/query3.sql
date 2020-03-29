-- :name most_sold :many
SELECT   a.Title, count(1) as 'Numbers Sold'
FROM `tracks` t
inner join `albums` a on a.AlbumId = t.AlbumId
inner join `invoice_items` ii on t.TrackId = ii.TrackId
group by t.AlbumId, a.Title
order by  count(1) DESC
limit 10;