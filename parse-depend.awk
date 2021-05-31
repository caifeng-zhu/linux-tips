BEGIN 	{ RS = "\\\n" }
	{ for (i = 1; i < NF; i++) if ($i !~ /.*:/ && files[$i]++ == 0) print $i }
#END	{ for (f in files) print f }
