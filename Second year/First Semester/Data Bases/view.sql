
create or alter view view1 
as
	select sq.CardNumber
	from (    
		SELECT distinct t.CardNumber, t.AtmId
		FROM Transactions t
	) as sq
	GROUP BY sq.CardNumber
	HAVING COUNT(*) = (SELECT COUNT(*) FROM ATM)
GO







