#!/usr/bin/env python3

import os, sys

ROOT = sys.argv[1]

PATHS = (
        ('static/certificates/', 'certificates'),
    )

for source, destination in PATHS:
    source_path = os.path.join(ROOT, source)
    destination_path = os.path.join(ROOT, destination)

    print("Moving {} -> {}".format(source_path, destination_path))
    os.rename(source_path, destination_path)
