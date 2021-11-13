compile_requirements:
	pip-compile requirements/prod.in
	pip-compile requirements/dev.in

remove_migration_files:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
