import sys
from urlhook import url_hook
from url_finder import URLFinder
from urlloader import URLLoader


sys.path_hooks.append(url_hook)

print(sys.path_hooks)