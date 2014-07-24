"""
Main entry file.  This file creates and setups the main window and then hands control over to that.

The MainWindow object handles everything from there on in.
"""

import os
import sys

srcpath = os.path.dirname(os.path.realpath(sys.argv[0]))
sys.path.append(srcpath)

import roam.environ

with roam.environ.setup() as roamapp:
    import roam.config
    import roam
    import roam.mainwindow
    import roam.utils
    import roam.api.featureform
    import roam.api.plugins

    # Fake this module to maintain API.
    sys.modules['roam.featureform'] = roam.api.featureform

    window = roam.mainwindow.MainWindow()

    pluginspaths = [os.path.join(roamapp.apppath, 'plugins'),\
                    os.path.join(roamapp.apppath, 'roam', 'plugins')]

    print pluginspaths
    roam.api.plugins.load_plugins_from(pluginspaths)

    roamapp.setActiveWindow(window)
    roamapp.set_error_handler(window.raiseerror, roam.utils)

    projectpaths = roam.environ.projectpaths(roamapp.projectsroot, roam.config.settings)
    projects = roam.project.getProjects(projectpaths)
    window.loadprojects(projects)
    window.actionProject.toggle()
    window.viewprojects()
    window.loadpages(roam.api.plugins.registeredpages)
    window.show()

