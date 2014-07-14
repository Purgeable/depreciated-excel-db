ECHO OFF
Echo Current dir: "%CD%"

C:\Python33\python -m pydoc -w dir_file
C:\Python33\python -m _clean_html dir_file.html

C:\Python33\python -m pydoc -w markup
C:\Python33\python -m _clean_html markup.html

C:\Python33\python -m pydoc -w frame2db
C:\Python33\python -m _clean_html frame2db.html

C:\Python33\python -m pydoc -w db2xls
C:\Python33\python -m _clean_html db2xls.html

REM python -m pydoc markup > markup.txt
pause