
clean:
	for d in `find picdump -type d`; do
	  case "$d" in
	    */__pycache__ ) rm -r $d ;;
		* ) 
