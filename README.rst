SuperFind
================

I got inspiration from the Code intelligence plugin SublimeCodeIntel but it never really worked for me well (especially on windows).  The only feature I miss in SublimeText is code navigation, code completion, and debugging so I decided to roll my own for the first one.

Provides the following features:

* Jump to definition

Installing
----------
**Without Git:** Download the latest source from `GitHub <http://github.com/EricGit/SuperFind.git>`_ and copy the whole directory into the Packages directory.

**With Git:** Clone the repository in your Sublime Text 2 Packages directory, located somewhere in user's "Home" directory::

    git clone git://github.com/EricGit/SuperFind.git


The "Packages" packages directory is located at:

* OS X::

    ~/Library/Application Support/Sublime Text 2/Packages/

* Linux::

    ~/.Sublime Text 2/Packages/

* Windows::

    %APPDATA%/Sublime Text 2/Packages/


Using
-----

* SuperFind helps you find class, modules, and functions in ruby, erb, and javascript files. even across files with just a click. Use ``command+click`` or ``ctrl+alt+click`` which will select the word and do a search.

* The first time you use it scans all files and reads at least some files.  Beacause of this, it might be slow on the first try.

