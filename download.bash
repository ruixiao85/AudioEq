#!/usr/bin/env bash
echo "self, scpt=${0}"; scpt=${0}

git clone --no-checkout --filter=tree:0 https://github.com/jaakkopasanen/AutoEq
cd AutoEq
git sparse-checkout set measurements
git checkout

sources=(innerfidelity oratory1990 rtings)
types=(earbud in-ear over-ear)
for s in "${sources[@]}"; do
  for t in "${types[@]}"; do
    echo "${s}/data/${t}"
    dest="../db/${s}/${t}/";
    mkdir -p ${dest}
    find "measurements/${s}/data/${t}" -maxdepth 2 -type f -name "*.csv" -exec mv -t ${dest} {} +
  done
done

cd ..