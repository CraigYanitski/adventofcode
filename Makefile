#!/bin/zsh

ifeq (year,$(firstword $(MAKECMDGOALS)))
  YEAR := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(YEAR):;@:)
endif

.PHONY: help year run

help:
	@echo "Use this makefile to start a new year or run a previous year"
	@echo "year _: create a new calendar folder and initialize git for VC"
	@echo "run: use this while within a calendar folder to run the entire year"

year:
	@mkdir $(YEAR)
	@cp ./.gitignore ./$(YEAR)
	@cd ./$(YEAR) && git init && \
		git add .gitignore && \
		git commit -m "ignore files"

run:
	echo solution_{1..25}.py | xargs -n 1
