from fabric import local

def documentation():
    local("sphinx-build -C -D extensions=['sphinx.ext.autodoc'] -D project=django-eventlogs -D authors='Nowell Strite' -D version='0.1.0' -D release='0.1.0' -D master_doc='index' docs/ docs/_build/")
