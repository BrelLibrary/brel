.ONESHELL:
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")

.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep


.PHONY: show
show:             ## Show the current environment.
	@echo "Current environment:"
	@echo "Running using $(ENV_PREFIX)"
	@$(ENV_PREFIX)python -V
	@$(ENV_PREFIX)python -m site

.PHONY: install
install:          ## Install the project in dev mode.
	@echo "Don't forget to run 'make virtualenv' if you got errors."
	$(ENV_PREFIX)pip install -e .[test]

.PHONY: remove
remove:           ## Remove the project.
	$(ENV_PREFIX)pip uninstall -y brel

.PHONY: fmt
fmt:              ## Format code using black & isort.
	$(ENV_PREFIX)black brel/
	$(ENV_PREFIX)black tests/

.PHONY: black-src
black-src:
	$(ENV_PREFIX)black --check brel/

.PHONY: black-test
black-test:
	$(ENV_PREFIX)black --check tests/

.PHONY: black
black:         ## Run pep8, black, mypy linters.
	make black-src
	make black-test

.PHONY: mypy-src
mypy-src:
	$(ENV_PREFIX)mypy --ignore-missing-imports brel/

.PHONY: mypy-test
mypy-test:
	$(ENV_PREFIX)mypy --ignore-missing-imports tests/

.PHONY: mypy
mypy:
	make mypy-src
	make mypy-test

.PHONY: lint-src
lint-src:
	make black-src
	make mypy-src

.PHONY: lint-test
lint-test:
	make black-test
	make mypy-test

.PHONY: lint
lint:
	make lint-src
	make lint-test

.PHONY: test-dev
test-dev:		 ## Run tests.
	$(ENV_PREFIX)pytest -v --cov=brel -l --tb=short
	$(ENV_PREFIX)coverage xml
	$(ENV_PREFIX)coverage html

.PHONY: test-ci
test-ci:
	cd.. && $(ENV_PREFIX)pytest --cov=brel --tb=line --maxfail=1

.PHONY: ci
ci:
	make install
	make lint
	make test
	make remove

.PHONY: watch
watch:            ## Run tests on every change.
	ls **/**.py | entr $(ENV_PREFIX)pytest -s -vvv -l --tb=long --maxfail=1 tests/

.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build

.PHONY: virtualenv
virtualenv:       ## Create a virtual environment.
	@echo "creating virtualenv ..."
	@rm -rf .venv
	@python3 -m venv .venv
	@./.venv/bin/pip install -U pip
	@./.venv/bin/pip install -e .[test]
	@echo
	@echo "!!! Please run 'source .venv/bin/activate' to enable the environment !!!"

.PHONY: release
release:          ## Create a new tag for release.
	@echo "WARNING: This operation will create s version tag and push to github"
	@read -p "Version? (provide the next x.y.z semver) : " TAG
	@echo "$${TAG}" > brel/VERSION
	@$(ENV_PREFIX)gitchangelog > HISTORY.md
	@git add brel/VERSION HISTORY.md
	@git commit -m "release: version $${TAG} 🚀"
	@echo "creating git tag : $${TAG}"
	@git tag $${TAG}
	@git push -u origin HEAD --tags
	@echo "Github Actions will detect the new tag and release the new version."

.PHONY: docs
docs:             ## Build the documentation.
	@echo "building documentation ..."
	@$(ENV_PREFIX)pydoc-markdown
	@$(ENV_PREFIX)mkdocs build -f docs/mkdocs.yml -d ../site

.PHONY: docs-deploy
docs-deploy:       ## Serve the documentation.
	make docs
	@$(ENV_PREFIX)mkdocs gh-deploy -f docs/mkdocs.yml -d ../site

.PHONY: init
init:             ## Initialize the project based on an application template.
	@./.github/init.sh

