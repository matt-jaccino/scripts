import sys
from pathlib import Path

src_dir = Path(sys.argv[1])
dest_dir = Path(sys.argv[2])

src = set(map(lambda f: f.name, src_dir.glob("*.*")))
dest = set(map(lambda f: f.name, dest_dir.glob("*.*")))
nl='\n  - '
print(f"Added:\n  - {nl.join(map(str, dest - src))}")
print(f"Removed:\n  - {nl.join(map(str, src - dest))}")

remove_inp = input("Remove? [y/N]")
if remove_inp.lower() == 'y':
    for f in src - dest:
        (src_dir/f).unlink()
