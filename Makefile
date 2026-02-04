SHELL := /bin/bash

DOCS_ROOT ?= "$(HOME)/Documents/Obsidian\ Vault/Docusaurus"

.PHONY: sync git build deploy serve

# Sync Obsidian notes into the Docusaurus docs folder.
sync:
	@echo "Rsyncing Obsidian notes to Docusaurus docs directory..."
	rsync -av "$(DOCS_ROOT)/" "./docs/"

# Commit and push docs changes to GitHub (no-op if nothing changed).
git:
	@echo "Pushing changes to GitHub repository..."
	git add docs
	@if ! git commit -m "Notes synced from Obsidian" >/dev/null 2>&1; then \
		echo "No changes to commit."; \
	else \
		git push origin main; \
	fi

# Build the static site.
build:
	npm run build

# Run the local dev server with live reload.
serve:
	npm run start

# Full deploy: sync + commit/push + build + deploy.
deploy: sync git build
	@echo "Building and deploying Docusaurus site..."
	USE_SSH=true npm run deploy
