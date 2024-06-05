import 'files/quarto.just'

default:
  just --list

ensure_env:
  pre-commit install

publish: pypi-publish quarto-publish

pypi-publish: export
  pdm publish