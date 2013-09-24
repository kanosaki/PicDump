test:
	python -m unittest
run:
	./bin/picdumpd
clean:
	for d in `find picdump -type d`; do \
	  case "$$d" in \
	    */__pycache__ ) rm -r $$d ;; \
		* ) rm $$d/*.pyc ;; \
	  esac \
	done
