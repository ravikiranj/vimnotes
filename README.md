# vimorgmode
Useful vim orgmode scripts

## Dependencies
* VimOrgMode - https://github.com/jceb/vim-orgmode
* Emacs - https://www.gnu.org/software/emacs/
* Emacs OrgMode - https://www.gnu.org/software/emacs/
* LaTeX - https://www.latex-project.org/

## Scripts
### `gen_org_mode_notes_pdf.py`
* Generates a consolidate PDF out of the org mode notes between a given date range.
* Usage

```
./gen_org_mode_notes_pdf.py -s 2018-02-20 -e 2018-02-22
```

### `backup_old_org_files.py`
* Use it as a cron to backup org files as below

```
# Backup org mode files everyday at 12pm
0 12 * * * cd PATH_TO_ORG_FILES_FOLDER && PATH_TO_BACKUP_SCRIPT/backup_old_org_files.py 2>&1 | tee -a PATH_TO_BACKUP_SCRIPT/backup.log
```

### `create_todays_org_file.py`
* Use it to create a new org file everyday in the morning

```
# Create new org mode file every weekday if it doesn't exist
0 9,11,13,15 * * 1-5 cd PATH_TO_CREATE_ORG_FILE && PATH_TO_CREATE_SCRIPT/create_todays_org_file.py 2>&1 | tee -a PATH_TO_CREATE_SCRIPT/org_file_create.log
```
