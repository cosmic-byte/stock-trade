#!/usr/bin/env bash
# Note: when first run this script or migrations are updated, please remove the options --nomigrations and --reuse-db

py.test -n 8  stock_trade/tests/
