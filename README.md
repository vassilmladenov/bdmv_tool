# bdmv_tool

Python reimplementation of `BDMV Modifier 2.0.exe` Windows tool linked [here](https://watershade.net/wmcclain/UDP-203-faq.html). Makes BDMV backups e.g. from MakeMKV or CloneBD play on from the Oppo file browser by modifying the `index.bdmv` file.

# Installation

Requires Python 3. I've tested this on Python 3.9.6. 

Clone or download the repository.
```
git clone https://github.com/vassilmladenov/bdmv_tool.git
cd bdmv_tool
chmod +x bdmv_tool.py
sudo ln -s "$PWD/bdmv_tool.py" /usr/local/bin/bdmv_tool
```
If you didn't make the symlink, you can run with `python3 path/to/bdmv_toool.py ...`.

# Usage
```
# run on single directory, assuming path/to/backup_dir/BDMV or path/to/backup_dir/AVCHD/BDMV exists
bdmv_tool path/to/backup_dir

# verbose mode
bdmv_tool -v path/to/backup_dir

# glob examples
bdmv_tool backups/*
bdmv_tool a_backup/Disc{1,2}
```

# Notes, TODO

- The Windows exe also looks for `INDEX.BDM` but none of my backups have this
- The exe updates the access time of `MovieObject.bdmv`, but the backups play fine without doing this step
- Make the tool offer to create the `AVCHD` directory if it doesn't exist (required for playback)

Please open an issue if the tool fails on a particular directory.