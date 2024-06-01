import 'files/quarto.just'

default:
   just --list

publish: pypi-publish quarto-publish

pypi-publish: export
  pdm publish