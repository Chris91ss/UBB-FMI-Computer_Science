BEGIN{
	c = 0
}
$5~/- 91[0-9] - [A-Z]*AN /{
	c++	
}
END{
	print c
}
