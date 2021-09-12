# Backup and Restore Linux Config
Almost all linux configuration can be done editing files. These scripts allows you to save those files, which usually start by a *dot*.

For example this: https://github.com/ThePrimeagen/.dotfiles

It would be easy to copy and paste all those files, but this tool gives you:
- User specific and common configuration
- Save backup when restoring files
- Show the diff when restoring files
- Dry-run, ask in each file...

## Installation

```bash
pip install backup_and_restore_linux_config
```

## Usage
```bash
mkdir -p home_config_files/home/_any_user
touch home_config_file/home/_any_user/.zshrc
backup_linux_config  home_config_file  _any_user
```
Now the .zshrc has been saved and you can "git push" the "home_config_files" directory.

Suppose that have installed recentelly your operative system and want to recover the saved config;
```bash
restore_linux_config  home_config_file  _any_user
```

And that it's! 

