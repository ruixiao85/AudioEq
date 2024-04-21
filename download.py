import os
import shutil

os.system("git clone --no-checkout --filter=tree:0 https://github.com/jaakkopasanen/AutoEq")
os.system("cd AutoEq && git sparse-checkout set measurements")
os.system("cd AutoEq && git checkout")


# Define the sources and types
sources = [
  'innerfidelity',
  'kr0mka',
  'Kuulokenurkka',
  'oratory1990',
  'rtings',
  'Super Review'
]
types = ['earbud', 'in-ear', 'over-ear']

# Iterate over each source and type
for s in sources:
    for t in types:
        print(f"{s}/data/{t}")
        dest = f"../db/{s}/{t}/"
        os.makedirs(dest, exist_ok=True)
        # Find all .csv files and move them to the destination
        for root, dirs, files in os.walk(f"measurements/{s}/data/{t}"):
            for file in files:
                if file.endswith('.csv'):
                    shutil.move(os.path.join(root, file), dest)

# Change directory to the parent directory
os.chdir('..')
