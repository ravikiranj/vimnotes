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
0 12 * * * PATH_TO_BACKUP_SCRIPT/backup_old_org_files.py 2>&1 | tee -a PATH_TO_BACKUP_SCRIPT/backup.log
```
