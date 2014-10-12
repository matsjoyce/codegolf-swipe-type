codegolf-swipe-type
===================

For the Swipt Type Converter question at http://codegolf.stackexchange.com/questions/39741/swipe-type-converter

To set up control for testing
-----------------------------

 - Add your code file to `entries/`
 - Add a section to `entries.ini` in the form

   ```
   [Your name]
   runner=python your_code.py
   compiler=g++ --help
   argv=true
   ```
 - `compiler` and `argv` is optional (`argv` defaults to `false`)
 - Run `python3 control.py`
 - Your log file will be at `logs/Your name.log`

Credits
-------

Word list from [SCOWL (And Friends)](http://wordlist.aspell.net/)
