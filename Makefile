.PHONY : test
.PHONY : test_all
test:
	nosetests --rednose -a '!slow'

test_all:
	nosetests --rednose -a 'slow'

run:
	./bin/picdumpd

clean:
	for d in `find picdump -type d`; do \
	  case "$$d" in \
	    */__pycache__ ) rm -r $$d ;; \
		* ) rm $$d/*.pyc ;; \
	  esac \
	done
	rm *.log
	rm -r cache
	rm -r default

setup:
	bin/setupenv.sh

update_requirements:
	pip freeze > requirements.txt
