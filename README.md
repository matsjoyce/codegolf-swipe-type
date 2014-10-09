codegolf-swipe-type
===================

For the (currently suggested) Swipt Type question at http://meta.codegolf.stackexchange.com/questions/2140/sandbox-for-proposed-challenges/

To set up control for testing
-----------------------------

 - Add your code file to `entries/`
 - Add a section to `entries.ini` in the form

   ```
   [Your name]
   runner=python your_code.py
   compiler=g++ --help
   argv=True
   ```
 - `compiler` and `argv` is optional (`argv` defaults to `false`)
 - Run `python3 control.py`
 - Your log file will be at `logs/Your name.log`
