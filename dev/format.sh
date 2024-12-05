#!/bin/bash
set -e
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"/../

taplo fmt

# Python
flwr-dev check-copyrights src/py/flwr
flwr-dev fix-init src/py/flwr
python -m isort --skip src/py/flwr/proto src/py
python -m black -q --exclude src/py/flwr/proto src/py
python -m docformatter -i -r src/py/flwr -e src/py/flwr/proto
python -m docformatter -i -r src/py/flwr_tool
python -m ruff check --fix src/py/flwr

# Protos
find src/proto/flwr/proto -name *.proto | grep "\.proto" | xargs clang-format -i

# Examples
python -m black -q examples
python -m docformatter -i -r examples

# Benchmarks
python -m isort benchmarks
python -m black -q benchmarks
python -m docformatter -i -r benchmarks

# E2E
python -m isort e2e
python -m black -q e2e
python -m docformatter -i -r e2e

# Notebooks
python -m black --ipynb -q doc/source/*.ipynb
KEYS="metadata.celltoolbar metadata.language_info metadata.toc metadata.notify_time metadata.varInspector metadata.accelerator metadata.vscode cell.metadata.id cell.metadata.heading_collapsed cell.metadata.hidden cell.metadata.code_folding cell.metadata.tags cell.metadata.init_cell cell.metadata.vscode cell.metadata.pycharm"
python -m nbstripout doc/source/*.ipynb --extra-keys "$KEYS"
python -m nbstripout examples/*/*.ipynb --extra-keys "$KEYS"

# Markdown
python -m mdformat --number doc/source examples

# RST
docstrfmt doc/source
