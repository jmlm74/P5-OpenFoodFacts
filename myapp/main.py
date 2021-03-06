from myapp.models import models
from myapp.tools import jmlmtools
from myapp.views import apptextview

"""
The main program
"""

def main():
    jmlmtools.clear()
    print("")
    args = jmlmtools.parse_arguments()
    if args.db == "create":
        models.fill_database()
        exit(0)
    elif args.db == "test":
        models.test_database()
        exit(0)
    appliConsole  = apptextview.ConsoleView()
    appliConsole.appli()


if __name__ == "__main__":
    main()