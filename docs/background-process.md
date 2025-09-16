If you want to start a script in the background of a ssh session this can be accomplished by running
```bash
some_command > some-command-log.txt 2>&1 &
```
where `some_command` should be replaced by the command you want to run in the background,
and `some-command-log.txt` should be replaced by the file you want the log to appear in.