#!/usr/bin/env bash

set -x

export PATH="$HOME/.nvm:$PATH"

cd ts
nvm use 16.14.2
ng serve --open
