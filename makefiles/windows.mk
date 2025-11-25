# Makefile extensions for windows.

# -----------------------------------------------------------------------------
# Variables
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# OS specific targets
# -----------------------------------------------------------------------------

.PHONY: clean-osarch-specific
clean-osarch-specific:
	del /F /S /Q $(DIST_DIRECTORY)
	del /F /S /Q $(MAKEFILE_DIRECTORY)/.coverage
	del /F /S /Q $(MAKEFILE_DIRECTORY)/.mypy_cache
	del /F /S /Q $(MAKEFILE_DIRECTORY)/.pytest_cache
	del /F /S /Q $(MAKEFILE_DIRECTORY)/__pycache__
	del /F /S /Q $(MAKEFILE_DIRECTORY)/coverage.xml
	del /F /S /Q $(MAKEFILE_DIRECTORY)/dist
	del /F /S /Q $(MAKEFILE_DIRECTORY)/docs/build
	del /F /S /Q $(MAKEFILE_DIRECTORY)/htmlcov
	del /F /S /Q $(TARGET_DIRECTORY)


.PHONY: dependencies-for-development-osarch-specific
dependencies-for-development-osarch-specific:


.PHONY: dependencies-osarch-specific
dependencies-osarch-specific:
	python3 -m pip install --upgrade pip
	pip install psutil pytest pytest-cov pytest-schema


.PHONY: hello-world-osarch-specific
hello-world-osarch-specific:
	$(info Hello World, from windows.)


.PHONY: setup-osarch-specific
setup-osarch-specific:
	$(info No setup required.)


.PHONY: venv-osarch-specific
venv-osarch-specific:
	@python -m venv .venv

# -----------------------------------------------------------------------------
# Makefile targets supported only by this platform.
# -----------------------------------------------------------------------------

.PHONY: only-windows
only-windows:
	$(info Only windows has this Makefile target.)
