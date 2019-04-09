# vimorgmode
Useful vim orgmode and markdown notes scripts

## Dependencies
* VimOrgMode - https://github.com/jceb/vim-orgmode
* Emacs - https://www.gnu.org/software/emacs/
* Emacs OrgMode - https://www.gnu.org/software/emacs/
* LaTeX - https://www.latex-project.org/
* markdown-pdf - https://github.com/alanshaw/markdown-pdf
* markdown-toc - https://github.com/jonschlinkert/markdown-toc 

## Scripts
* All the python files have `notes_mode` variable. Configure it to `.md` or `.org` to switch to markdown or org mode respectively.

### `gen_notes_pdf.py`
* Generates a consolidate PDF out of the mode notes between a given date range.
* Usage

```
./gen_notes_pdf.py -s 2018-02-20 -e 2018-02-22
```

### `backup_old_notes_files.py`
* Use it as a cron to backup org files as below

```
# Backup org mode files everyday at 12pm
0 12 * * * cd PATH_TO_NOTE_FILES_FOLDER && PATH_TO_BACKUP_SCRIPT/backup_old_notes_files.py 2>&1 | tee -a PATH_TO_BACKUP_SCRIPT/backup.log
```

### `create_todays_notes_file.py`
* Use it to create a new note file everyday in the morning

```
# Create new org mode file every weekday if it doesn't exist
0 9,11,13,15 * * 1-5 cd PATH_TO_CREATE_NOTES_FILE && PATH_TO_CREATE_SCRIPT/create_todays_notes_file.py 2>&1 | tee -a PATH_TO_CREATE_SCRIPT/notes_file_create.log
```

### `gen_html_from_markdown.py`
* Generates HTML files for the markdown files present in the current folder and places it in `html` folder.
* If `--all` option is passed to it, it also generates the html files for the markdown files present in `./backup` folder.
* These can be rsync-ed to any webserver for sharing purposes
