#!/usr/bin/env python3

import sys
import json
from itertools import dropwhile




    
class ParsedArguments:
    """
    this will contain or represent both positional and optional
    arguments from the command line as object properties.
    """

    def __repr__(self):
        return json.dumps(self.__dict__)
    


class ParsedEncoder(json.JSONEncoder):
    """
    This is for when the caller wants to view the ParsedArgument
    object via json.dumps, just pass this as the 'cls' param
    of json.dumps

    ex. json.dumps(parsed_arguments, cls=ParsedEncoder, indent=4)
    """

    def default(self, o):
        if isinstance(o, ParsedArguments):
            return o.__dict__
        return json.JSONEncoder.default(self, o)
    


class SimpleArgParser:
    """
    A non-structured, dynamic class for parsing command line arguments
    that you can use on your Python scripts to collect
    any sequence of positional and optional (no sequence enforced).

    These things are all valid:
    # typical/usual
    python yourscript.py file01.txt file02.dat --compress=Y --method=gzip

    # optional with no dash prefix:
    python yourscript.py file01.txt file02.dat compress=Y method=gzip

    # optional and positional can be in any sequence:
    python yourscript.py --compress=Y file01.txt --method=gzip file02.dat  

    # optional with no dash, single dash, double, triple dashes, etc.
    python yourscript.py ---method=gzip file01.txt -compress=Y file02.dat --loglevel=3

    
    NOTE:
    Every parameter value will be a string (str) as this was conceived just to have a
    simple way to collect command-line arguments with no setups, just parse/collect
    and that's it.

    """

    def __init__(self, add_script_to_positional:bool=False):
        """
        the script name (typically the item at index zero) will
        be set as the 'script_name' property/data.

        if add_script_to_positional is set to True, then the script name
        by the time SimpleArgParser is initialized will be 
        included in positional arguments as well.
        """
        self.add_script_to_positional = add_script_to_positional

 

    def parse_args(self) -> ParsedArguments:
        """
        the main method that iterates over sys.argv and group the
        raw arguments into either positional or optional.

        as mentioned in the class docstring, optional is freestyle,
        or non-strict so you can opt not to use any dash or hypen at all,
        the only required is the equal sign between the key and value.
        you can also add 1 or more dash/hypen depending on your style
        """
        
        parsed = ParsedArguments()
        
        # convert to iterable so we can easily choose to process
        # one or all of it
        iargs = iter(sys.argv)

        # get the first item as it's "normally" the python script
        script_name = str(next(iargs)).strip()
        setattr(parsed, 'script_name', script_name)
        
        # define storage for positional and optional arguments,
        # and let's also add one for invalid ones,
        # apart from individual params as properties
        _positional_args = []
        _optional_args = {}


        kw_indicator = "="  # clear sign it's an optional
        kw_prefix = "-"

        def nonkw(c:str):
            """ dropwhile predicate to remove dashes """
            if c == kw_prefix:
                return True
            return False
        

        for raw_value in iargs:
            if kw_indicator in raw_value:
                # assume it's optional.
                # to make this super flexible, allow zero or more hypens
                # so the user can customize their own app based on their needs
                # we just have to remove those hypens and keep the name
                chopped = list(dropwhile(nonkw, list(raw_value)))
                kwvalue = ''.join(chopped).split(kw_indicator)
                key = kwvalue[0].strip()
                value = kwvalue[1].strip()
                _optional_args[key] = value

                # aside from adding it to the optionals,
                # make keyword arguments have be its own property
                setattr(parsed, key, value)
            else:
                # this is positional
                _positional_args.append(raw_value)



        setattr(parsed, '_positional_args_', _positional_args)
        setattr(parsed, '_optional_args_', _optional_args)

        return parsed
    

