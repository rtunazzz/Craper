#!/usr/bin/env bash

echo "*** Configuring Craper ***"
PROXY_FILE="../craper/config/proxies.txt"
EXMAPLE_CONFIG_FILE="../craper/config/config.example.json"
CONFIG_FILE="../craper/config/config.json"

if test -f "$PROXY_FILE"; then
  echo "Proxy file already exists."
else
  echo "Creating proxies.txt"
  touch "$PROXY_FILE"
fi

if test -f "$CONFIG_FILE"; then
  echo "Config file already exists."
else
  echo "Creating config.json"
  cp "$EXMAPLE_CONFIG_FILE" "$CONFIG_FILE"
fi
