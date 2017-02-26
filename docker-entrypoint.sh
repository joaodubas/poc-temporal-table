#!/bin/bash
set -e

if [ "$1" = 'python' -a "$(id -u)" = '0' ]; then
	mkdir -p /opt/src
	chown -R account /opt/src
	exec gosu account "$BASH_SOURCE" "$@"
fi

exec "$@"
