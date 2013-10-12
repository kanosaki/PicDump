test:
	nosetests --rednose

test_all:
	UNITTEST_MODE=full nosetests --rednose

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

setup:
	pip install -r requirements.txt

update_requirements:
	pip freeze > requirements.txt
