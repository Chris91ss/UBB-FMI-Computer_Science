BEGIN{
	counter = 0
}
NR == 0 && $0 ~/[aeiouAEIOU]{2,}/{
	counter += 1
}
END{
	print counter
}
