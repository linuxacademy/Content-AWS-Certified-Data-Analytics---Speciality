# Spectrum Queries

## Number of rows in spectrum.sales
```SQL
select count(*) from spectrum.sales;
```

## First 10 rows from spectrum.sales
```SQL
select * from spectrum.sales limit 10;
```

## Top 15 events by ticket sales
```SQL
select top 15 event.eventname as event_name, sum(spectrum.sales.pricepaid) as gross_ticket_sales from spectrum.sales, event
where spectrum.sales.eventid = event.eventid
and spectrum.sales.pricepaid > 30
group by event.eventname
order by 2 desc;
```