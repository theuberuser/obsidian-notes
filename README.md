# Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Commands

```bash
# Sync Obsidian notes into ./docs only
make sync

# Commit + push docs changes only
make git

# Build the site only
make build

# Run the local dev server (live reload)
make serve

# Full workflow: sync -> git -> build -> deploy
make deploy
```

### Custom Obsidian Path

If your Obsidian vault lives somewhere else, override `DOCS_ROOT` when you run `make`:

```bash
make sync DOCS_ROOT="/path/to/your/Obsidian Vault/Docusaurus"
```

## Install Dependencies

```bash
npm install
```
