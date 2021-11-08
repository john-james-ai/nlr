#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \__main__.py                                                                                                  #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james@nov8.ai                                                                                            #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Saturday, November 6th 2021, 11:15:18 pm                                                                      #
# Modified : Sunday, November 7th 2021, 6:35:38 pm                                                                         #
# Modifier : John James (john.james@nov8.ai)                                                                               #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""Console script for cookie."""


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    args = parser.parse_args()

    print("Arguments: " + str(args._))
    print("Replace this message by putting your code into "
          "cookie.cli.main")
    return 0


if __name__ == "__main__":
    main()
