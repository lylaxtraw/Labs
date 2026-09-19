#!/usr/bin/env bash

set -euo pipefail

PORT="${1:-}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="${PROJECT_ROOT}/src"

if [[ -z "${PORT}" ]]; then
	printf 'Uso: %s <puerto-serie>\n' "$0" >&2
	printf 'Ejemplo: %s /dev/cu.usbmodemXXXX\n' "$0" >&2
	exit 2
fi

if ! command -v mpremote >/dev/null 2>&1; then
	printf 'Error: mpremote no esta instalado o no esta en PATH.\n' >&2
	exit 1
fi

remote=(mpremote connect "${PORT}")

"${remote[@]}" fs mkdir :lib >/dev/null 2>&1 || true

for file in "${SOURCE_DIR}"/*.py; do
	"${remote[@]}" fs cp "${file}" ":$(basename "${file}")"
done

for file in "${SOURCE_DIR}/lib"/*.py; do
	"${remote[@]}" fs cp "${file}" ":lib/$(basename "${file}")"
done

printf 'Archivos cargados en %s.\n' "${PORT}"
