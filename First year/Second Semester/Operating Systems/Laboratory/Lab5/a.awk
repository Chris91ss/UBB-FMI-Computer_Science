BEGIN{
	print "START"
}
NR % 2 == 1{
	print $0
}
END{
	print "END"
}
