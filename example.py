""" this contains code on how to use the argxtract module/library """

# import the module/library
from argxtract import SimpleArgParser
from argxtract import ParsedEncoder


# import for emulating command-line arguments
from unittest.mock import patch

# import for pretty display
import json



def main():
    #
    # parse your own command-line arguments (if you passed any)
    #
    print("\nParsing actual command line arguments (if any):")
    params = SimpleArgParser().parse_args()
    
    print(f"{params._positional_args_ = }")
    print(f"{params._optional_args_ = }")
    print(json.dumps(params, indent=3, cls=ParsedEncoder))

    # you can also access the keyword/optional name:
    # example, if you passed --msg=hi
    # you can do this: print(params.msg)

    #
    # here are more controlled/simulated parameters
    # so you can test/see it without typing them one by one
    #
    test_cases = [ 
        # typical/usual
        ['yourscript.py', 'file01.txt', 'file02.dat', '--compress=Y', '--method=gzip'],

        # optional with no dash prefix:
        ['yourscript.py', 'file01.txt', 'file02.dat', 'compress=Y', 'method=gzip'],

        # optional and positional can be in any sequence:
        ['yourscript.py', '--compress=Y', 'file01.txt', '--method=gzip', 'file02.dat'],

        # optional with no dash, single dash, double, triple dashes, etc.
        ['yourscript.py', '---method=gzip', 'file01.txt', '-compress=Y', 'file02.dat', '--loglevel=3'],
    ]

    for index, testcase in enumerate(test_cases):
        print(f"\n{index} Testing: {testcase}:")
        with patch('sys.argv', testcase) as context:
            params = SimpleArgParser().parse_args()
            
            print(f"{params._positional_args_ = }")
            print(f"{params._optional_args_ = }")
            print(json.dumps(params, indent=3, cls=ParsedEncoder))


if __name__ == '__main__':
    main()

