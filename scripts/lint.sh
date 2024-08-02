#!/bin/sh

check=false

if [ -z "$1" ] || [ "$1" = "--check" ] ; then
  echo "Defaulting to apply on 'root'"
  FPATH="."
  if [ "$1" = "--check" ]; then
    check=true
  fi
else 
  FPATH=$1
  if [ "$2" = "--check" ]; then
    check=true
  fi
fi

echo $FPATH
echo $check

if "$check"; then
  ruff format $FPATH --check
  mypy $FPATH
  ruff check $FPATH
else
  ruff format $FPATH
  ruff check $FPATH --fix
  ruff check $FPATH --select I --fix
fi