from distutils.core import setup

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
files = ["media/*"]

setup(name = "couchman",
    version = "0.4",
    description = "couchman",
    author = "Pavel Krayzman",
    author_email = "pasha@smscoin.com",
    url = "https://github.com/kolyanu4/my_couchman",
    packages = ['couchman', 'couchman.couchman','couchman.couchman.UI'],
    #'package' package must contain files (see list above)
    #I called the package 'package' thus cleverly confusing the whole issue...
    #This dict maps the package name =to=> directories
    #It says, package *needs* these files.
    package_data = {'couchman' : files },
    #'runner' is in the root.
    scripts = ["couchman_run"],
    long_description = """Really long text here.""" 
    #
    #This next part it for the Cheese Shop, look a little down the page.
    #classifiers = []     
) 
