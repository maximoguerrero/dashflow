-- :name media_profit_by_type_filtered    :many
SELECT  mt.Name as label, strftime('%Y',InvoiceDate) as year  ,  printf("%.2f", sum(ii.UnitPrice ) )  as value
FROM `tracks` t
inner join `media_types` mt on mt.MediaTypeId = t.MediaTypeId
inner join `invoice_items` ii on ii.TrackId = t.TrackId
inner join `invoices` i on i.InvoiceId = ii.InvoiceId

where mt.Name like '%' || :kind || '%'

group by t.MediaTypeId, year
order by year
;