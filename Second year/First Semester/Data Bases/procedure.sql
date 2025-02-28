
create or alter procedure pr1 @cardnumber char(19)
as
begin
	delete 	
	from Transactions
	where Transactions.CardNumber Like @cardnumber
end
go






