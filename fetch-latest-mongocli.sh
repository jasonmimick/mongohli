#!/usr/bin/env bash

# Fetch latest mongocli for bundling
TARBALL=$(curl -sL https://github.com/mongodb/mongocli/releases/latest | grep ".tar.gz" | head -1 | cut -d'=' -f2 | cut -d' ' -f1)
echo "Fetching ${TARBALL}"
curl -OL "https://github.com${TARBALL}"
tar xvf ${TARBALL}
cp ${TARBALL}/mongocli ./mongocli.latest
rm ${TARBALL}
ls -l ./*mongocli*
