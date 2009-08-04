import os
from fabric import local

PROJECT_ROOT = os.path.abspath(os.path.curdir)

def bootstrap():
    local("rm -Rf ve/")

    local('virtualenv ve')

    # hack activate so it uses project directory instead of ve in prompt
    local('sed \'s/(`basename \\\\"\\$VIRTUAL_ENV\\\\\"`)/(`basename \\\\`dirname \\\\"$VIRTUAL_ENV\\\\"\\\\``)/g\' ve/bin/activate > ve/bin/activate.tmp')
    local('mv ve/bin/activate.tmp ve/bin/activate')

    # PIP install requirements
    local("pip install -I --source=ve/src/ --environment=ve/ -r REQUIREMENTS")

    # Cleanup pip install process
    local("rm -Rf build/")

    # Add local src folders to python path.
    local("echo '%s' >> ve/lib/python2.5/site-packages/easy-install.pth" % PROJECT_ROOT)

def documentation():
    local("rm -Rf docs/_build/html/")
    local("ve/bin/sphinx-build -aE docs/ docs/_build/html/")
    print "View the documentation here: file://%s" % os.path.join(PROJECT_ROOT, 'docs', '_build', 'html', 'index.html')
