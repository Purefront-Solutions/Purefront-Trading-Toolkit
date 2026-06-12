# Historical Data Collector

A command-line tool for collecting historical data.

## Setup

### Create a virtual environment (recommended)

Create the virtual environment (first time setup)
```bash
python -m venv .venv
```

Activate the virtual environment
```bash
source .venv/bin/activate
```

### Install

```bash
pip install -e .
```

This installs the `ttk` command into the virtual environment.

### Install test dependencies

```bash
pip install -r test/requirements.txt
```

## Configuration

### HDC_SECRET

`HDC_SECRET` is a required environment variable used to encrypt sensitive credentials (database passwords, API secrets) stored in the configuration. You must set it before adding or using any database or datasource.

Generate a strong secret and export it in your shell:

```bash
export HDC_SECRET="your-strong-secret-here"
```

To make it permanent, add the export to your shell profile (e.g. `~/.bashrc`, `~/.zshrc`):

```bash
echo 'export HDC_SECRET="your-strong-secret-here"' >> ~/.bashrc
source ~/.bashrc
```

Alternatively, store it in a `.env` file at the project root (this file is gitignored):

```
HDC_SECRET=your-strong-secret-here
```

`ttk` loads `.env` automatically on startup.

> **Important:** Use the same `HDC_SECRET` value every time. If it changes, previously stored credentials will not be decryptable and you will need to remove and re-add your databases and datasources.

## Usage

```bash
ttk <command>
```

### Commands

**datasource** — manage datasources

```bash
ttk datasource add --name <name> --type alpaca --apiKey <key> --apiSecret <secret>

ttk datasource update --name <name> [--type alpaca] [--apiKey <key>] [--apiSecret <secret>]

ttk datasource list

ttk datasource test --name <name>

ttk datasource remove --name <name>
```

**database** — manage databases

```bash
ttk database add --name <name> --type <type> --username <user> \
    --password <pass> --host <host> --port <port> --dbname <dbname>

ttk database update --name <name> [--type <type>] [--username <user>] \
    [--password <pass>] [--host <host>] [--port <port>] [--dbname <dbname>]

ttk database list

ttk database remove --name <name>

ttk database test --name <name>
```

**collection** — manage collections

```bash
ttk collection add --name <name> --database <db> --datasource <ds> --query <query> \
    --type historical-bars --start <ISO8601> [--frequency 1m|1d] [--end <ISO8601>] \
    [--symbols <sym1,sym2,...>]

ttk collection update --name <name> [--database <db>] [--datasource <ds>] \
    [--query <query>] [--type historical-bars] [--start <ISO8601>] \
    [--frequency 1m|1d] [--end <ISO8601>] [--symbols <sym1,sym2,...>]

ttk collection list

ttk collection remove --name <name>

ttk collection init --name <name>

ttk collection run --name <name>
```

**query** — manage queries

```bash
ttk query add --name <name> --type <type> --symbols <sym1,sym2,...> --frequency <1d|1m> [--start <ISO8601>] [--end <ISO8601>]

ttk query update --name <name> [--symbols <sym1,sym2,...>] [--frequency <1d|1m>] [--start <ISO8601>] [--end <ISO8601>]

ttk query list

ttk query remove --name <name>
```

Available query types (configured in `.config/system.config.yaml`):

| Type | Required fields | Optional fields |
|------|----------------|-----------------|
| `historical-bars` | `--symbols`, `--frequency` | `--start`, `--end` |

**version** — show the current version

```bash
ttk --version
```

## Help

```bash
ttk --help
ttk <command> --help
```
