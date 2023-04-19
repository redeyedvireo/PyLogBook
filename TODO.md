# PyLogBook To Do

These are roughly in order of priority.

- Redo layout:
  - Put dock on the left of the app window
  - Remove the search pane
  - Maybe place the log viewer in a stacked view with the log editor
- Implement font family buttons in the editor
  - Figure out why font cannot be set in the document.
- Implement Style button
- Implement Search, but do this as a modeless dialog, rather than as a pane in the app window.
- Implement Addendum button
- Make the log tree able to grow vertically
- I think there is a bug at startup where if a log file can't be opened, the program crashes
- Search for all TODO items and fix
- Compare with the C++ version that all needed functionality is present
- Create PyInstaller for both Windows and Linux
- Use Python sqlite3 module instead of Qt's SQL support (do this much later)
- Use PySide instead of PyQt (much later)
