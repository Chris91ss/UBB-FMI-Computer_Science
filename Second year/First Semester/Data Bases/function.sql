
create or alter function fun1 (@sum int)
returns table
as
return 
	select c.CardNumber, c.Cvv
	from Cards c
	inner join Transactions t on c.CardNumber=t.CardNumber 
	GROUP BY C.cardnumber, C.CVV 
	HAVING SUM(t.Balance) > @sum
go











