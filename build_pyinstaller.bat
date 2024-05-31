call %OSGEO4W_ROOT%\o4w_env.bat
set PATH=%PATH%;%OSGEO4W_ROOT%\apps\qgis\bin
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT%\apps\qgis
set PYTHONPATH=%OSGEO4W_ROOT%\apps\qgis\python
set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\python312.zip
set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\\Python312\\DLLs
set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\\Python312\\Lib
set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\bin
set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\\Python312
set PYTHONPATH=%PYTHONPATH%;%OSGEO4W_ROOT%\apps\\Python312\\Lib\\site-packages
python setup_pyinstaller.py
pyinstaller -c --noconfirm -n roam src/roam/__main__.py