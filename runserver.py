#!/usr/bin/env python 

#-----------------------------------------------------------------------
# runserver.py
# Authors: Vedant Dhopte
#-----------------------------------------------------------------------

from sys import exit, argv, stderr
from tileboardflask import app
import argparse
 
#-----------------------------------------------------------------------

def main(argv):
    # Set up arg parser
    parser = argparse.ArgumentParser(description = "The registrar " \
                                     "application")

    parser.add_argument("port", type = int, help = "the port at " \
                        "which the server should listen")
    args = parser.parse_args() 

    print("Listening on port", args.port)
    app.run(host = '0.0.0.0', port = args.port, debug = True)

#-----------------------------------------------------------------------

if __name__ == '__main__':
    main(argv)