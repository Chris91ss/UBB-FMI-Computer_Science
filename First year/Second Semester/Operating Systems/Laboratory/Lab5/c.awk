BEGIN{
	c = 0
}
$5 ~/- 91[0-9] -/{
	c++	
}
END{
	print c
}
