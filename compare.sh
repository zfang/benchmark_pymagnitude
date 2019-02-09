#!/usr/bin/env bash

set -e

python main.py -m raw -i $@ > /tmp/before_patch.out
sh patch_pymagnitude.sh
python main.py -m raw -i $@ > /tmp/after_patch.out
sh patch_pymagnitude.sh -R

diff /tmp/before_patch.out /tmp/after_patch.out
