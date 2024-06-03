# Betterinput library
# Author: Gex97

__version__ = "0.3.5"
__author__  = "Gex97"

from typing import Any, final
from accessify import private
from libexceptions import *

class InputDevice:
    """Input device that improves input operations.
    
        constructor:
            params:
                `warnings`       : bool #private property
                `raise_exception`: bool #private property
                `streamsize`     : int  #private property
                `kit`            : dict #private
                
        use set_attribute(attr, value) to change their value\n
        A direct access to one of those attributes raises an exception (future patch will handle this exception)
    """

    default_kit: dict[str, str] = {
        "separator": " ",
        "iter_separator":",",
        "text": ""
    }

    def __init__(self, warnings:bool=False, raise_exceptions:bool=False, streamsize:int=None, kit:dict=default_kit):
        self.warnings = warnings
        self.raise_exceptions = raise_exceptions
        self.streamsize = streamsize
        self.kit = kit
        if not self.__check_kit():
            self.kit = InputDevice.default_kit
    
    @property
    def streamsize(self):
        return self._streamsize
    
    @streamsize.setter
    @private
    def streamsize(self, size:int):
        """ streamsize property setter, use set_attribute("streamsize", value: int) to change its value """
        if isinstance(size, int):
            self._streamsize = size if size > 0 else None
        elif size is None:
            self._streamsize = None
        else:
            raise TypeError(f"Invalid value type for \"streamsize\" expected int or None, found {type(size).__name__}")
    
    @property
    def warnings(self):
        return self._warnings
    
    @warnings.setter
    @private
    def warnings(self, state:bool):
        """ warnings property setter, use set_attribute("warnings", value: bool) to change its value """
        if isinstance(state, bool):
            self._warnings = state
        else:
            raise TypeError(f"Invalid value type for \"warnings\" expected bool, found {type(state).__name__}")
    
    @property
    def raise_exceptions(self):
        return self._raise_exceptions
     
    @raise_exceptions.setter
    @private
    def raise_exceptions(self, state:bool):
        """ raise_exceptions property setter, use set_attribute("raise_exceptions", value: bool) to change its value """
        if isinstance(state, bool):
            self._raise_exceptions = state
        else:
            raise TypeError(f"Invalid value type for \"raise_exception\" expected bool, found {type(state).__name__}")
    
    @final
    def set_attribute(self, attr, value):
        if attr and value is not None:
            if hasattr(self, attr):
                try:
                    self.__setattr__(attr, value)
                except AttributeError:
                    return
            else:
                raise AttributeError(f"Attribute: {attr} not found")
        else:
            raise WrongArgumentError("Invalid arguments: {}, {}".format(attr, value))

    @private
    def __check_kit(self):
        if len(self.kit) == len(InputDevice.default_kit):
            for item in list(self.kit.keys()):
                try:
                    if not self.kit[item] or type(self.kit[item]).__name__ != type(InputDevice.default_kit[item]).__name__:
                        return False
                except KeyError:
                    return False

            return True

        return False

    def process_data(self, values:list=None, types:list[type]=[str], iter_separator: str = ",", input_streamsize:int=None):
        """This function gets a list containing some values
            
            Then the inputs are casted to the type we put at the same position into `types`
            
            params:
                `values`:list, default:None -> this list contains the values to process
                
                `types`:list, default:[str] -> this list contains the types to cast the values to
                
                `input_streamsize`:int, default: None -> substitute property self.streamsize without changing its value (value can be higher than self.streamsize)
                
            returns:
                `values`:list -> This list contains the elaborated data insert in input
                
            ~ If self.warnings is set on True, the function will show you any warnings/errors ~
            
            ~ If self.raise_exceptions is set on True, the function will raise exceptions if needed ~
        """
        if type(values) not in (list, tuple):
            if self.raise_exceptions:
                raise TypeListError("Couldn't cast values: parameter \"values\" should be of type list or tuple, not {}".format(type(values).__name__))
            elif self.warnings:
                print("Warning: Couldn't cast values: parameter \"values\" should be of type list or tuple, not {}".format(type(values).__name__))
        
        if not input_streamsize:
            input_streamsize = self.streamsize
        elif input_streamsize == -1:
            input_streamsize = None
        elif input_streamsize < 1:
            input_streamsize = self.streamsize
        
        values:list[str] = values[0:input_streamsize if input_streamsize else None] # gets the input from index 0 to input_streamsize, if input_streamsize is None gets all the values from 0 to self.streamsize (if None gets all the values)
        
        if type(types) not in (list, tuple):
            if self.raise_exceptions:
                raise TypeListError("Couldn't cast values: parameter \"types\" should be of type  list or tuple, not {}".format(type(types).__name__))
            elif self.warnings:
                print("Warning: Couldn't cast values: parameter \"types\" should be of type list or tuple, not {}".format(type(types).__name__))
         
        elif len(types) != len(values) and len(types) != 1:
            if self.raise_exceptions:
                raise TypeListError("Invalid number of values: expected {}, got {}".format(len(types), len(values)))
            elif self.warnings:
                print("Warning: Invalid number of values: expected {}, got {}".format(len(types), len(values)))

        else:
            if len(types) != 1 and not all([types[x]==types[x+1] for x in range(len(types)-1)]):
                for i in range(len(values)):
                    skip_checks = True # Maybe this will be changed in future
                    try:
                        try:
                            if isinstance(types[i], type):
                                _ = iter(types[i]())
                                del _
                                
                                # Is iterable (not list of types)
                                # returns an object of the given iterable type
                                _v = values[i].strip()
                                
                                if _v.startswith("(") and _v.endswith(")") or _v.startswith("[") and _v.endswith("]") or _v.startswith("{") and _v.endswith("}"):
                                    values[i] = types[i]([x for x in values[i][1:-1].split(iter_separator)])
                                else:
                                    if self.raise_exceptions:
                                        raise ValueError(f"Invalid iterable syntax <{values[i]}>")
                                    elif self.warnings:
                                        print(f"Warning: Invalid iterable syntax <{values[i]}> [returning]")
                                    
                                    return values
                            else:
                                _: Any = types[i][0] # tries to get the first element of the, maybe, iterable. If it fails then it's not an iterable
                                
                                # Is iterable (is list of types)
                                # It will return a list object
                                if len(types[i]) == 1:
                                    try:
                                        _v = values[i].strip()
                                        
                                        if _v.startswith("(") and _v.endswith(")") or _v.startswith("[") and _v.endswith("]") or _v.startswith("{") and _v.endswith("}"):
                                            values[i] = [types[i][0](x) for x in values[i][1:-1].split(iter_separator)]
                                        else:
                                            if self.raise_exceptions:
                                                raise ValueError(f"Invalid iterable syntax <{values[i]}>")
                                            elif self.warnings:
                                                print(f"Warning: Invalid iterable syntax <{values[i]}> [returning]")
                                            
                                            return values
                                    except ValueError as err:
                                        if self.raise_exceptions:
                                            raise TypeListError("Couldn't cast {} to {} due an error... {}".format(values[i], types[i][0].__name__, err))
                                        elif self.warnings:
                                            print("Warning: Couldn't cast {} to {} due an error... {}".format(values[i], types[i][0].__name__, err))
                                            
                                        continue
                                else:
                                    try:
                                        _types: list = [t for t in types[i]]
                                        _v: str = values[i].strip()
                                        
                                        try:
                                            if _v.startswith("(") and _v.endswith(")") or _v.startswith("[") and _v.endswith("]") or _v.startswith("{") and _v.endswith("}"):
                                                values[i] = [_types[n](x) for n, x in enumerate(values[i][1:-1].split(iter_separator))]
                                            else:
                                                if self.raise_exceptions:
                                                    raise ValueError(f"Invalid iterable syntax <{values[i]}>")
                                                elif self.warnings:
                                                    print(f"Warning: Invalid iterable syntax <{values[i]}> [returning]")
                                                
                                                return values
                                        except ValueError as err:
                                            if self.raise_exceptions:
                                                raise TypeListError("Couldn't cast {} to {} due an error... {}".format(values[i], [t.__name__ for t in _types], err))
                                            elif self.warnings:
                                                print("Warning: Couldn't cast {} to {} due an error... {}".format(values[i], [t.__name__ for t in _types], err))
                                                
                                            continue
                                    except IndexError:
                                        if self.raise_exceptions:
                                            raise TypeListError("Couldn't cast {} to {} because the type list was invalid".format(values[i], type(types[i]).__name__))
                                        elif self.warnings:
                                            print("Warning: Couldn't cast {} to {} because the type list was invalid".format(values[i], type(types[i]).__name__))

                        except TypeError: # not iterable
                            try:
                                if isinstance(types[i], type):
                                    values[i] = types[i](values[i])
                            except ValueError:
                                if self.raise_exceptions:
                                    raise ValueCastError(f"Couldn't cast the value ({values[i]}) to {types[i].__name__}")
                                elif self.warnings:
                                    print(f"Warning: Couldn't cast the value ({values[i]}) to {types[i].__name__}")
                                    
                            skip_checks = False
                            continue
                            
                    except TypeError:
                        if self.raise_exceptions:
                            raise TypeListError("Couldn't cast the value ({}) to {}".format(values[i], type(types[i]).__name__))
                        elif self.warnings:
                            print("Warning: Couldn't cast the value ({}) to {}".format(values[i], type(types[i]).__name__))
                            
                        continue
                    
                    if not isinstance(types[i], type) and not skip_checks:
                        if self.raise_exceptions:
                            raise ValueCastError(f"Couldn't cast the value ({values[i]}) because the type ({types[i]}) was not valid")
                        elif self.warnings:
                            print(f"Warning Couldn't cast the value ({values[i]}) because the type ({types[i]}) was not valid")
                            
                    elif isinstance(values[i], str) and types[i] != str and not skip_checks:
                        if self.raise_exceptions:
                            raise TypeListError("Couldn't cast the value ({}) to {}".format(values[i], types[i].__name__))
                        elif self.warnings:
                            print("Warning: Couldn't cast the value ({}) to {}".format(values[i], types[i].__name__))
            else:
                try:
                    values = list(map(types[0], values))
                except ValueError:
                    if self.raise_exceptions:
                        raise ValueCastError("Couldn't cast the value because the type was not valid")
                    elif self.warnings:
                        print("Warning: Couldn't cast the value because the type was not valid")
        
        return values

    def get_input(self, text: str = default_kit["text"], cast_type: type = str, includes_spaces: bool = True, input_streamsize: int = None):
        """This function get a single input value from keyboard
            
            The input value can be casted to the given type `cast_type` (default `str`)
            
            NOTE: PLEASE, TO READ AN ITERABLE USE `get_multiple_input` INSTEAD!
            
            params:
                `text`:str, default: `""` -> the text of the input function
                
                `cast_type`:type, default: `str` -> the type to cast the value to
                
                `input_streamsize`:int, default: `None` -> substitute property self.streamsize without changing its value (value can be higher than self.streamsize)
                
            returns:
                `value`:cast_type -> This list contains the elaborated data insert in input
                
            ~ If self.warnings is set on True, the function will show you any warnings/errors ~
            
            ~ If self.raise_exceptions is set on True, the function will raise exceptions if needed ~
        """
        if not self.__check_kit(): # if there's an error in the kit, replaces it with the default kit
            self.kit = InputDevice.default_kit
        
        text = text if isinstance(text, str) else self.kit["text"]
        if not input_streamsize:
            input_streamsize = self.streamsize
        elif input_streamsize == -1:
            input_streamsize = None
        elif input_streamsize < 1:
            input_streamsize = self.streamsize
        
        try:
            value = input(text)[0:input_streamsize if input_streamsize else None]

            if not includes_spaces:
                fs: int = value.find(" ")
                value: str = value[0:fs if fs != -1 else None]
            
            return cast_type(value)
        except ValueError:
            if self.raise_exceptions:
                raise ValueCastError(f"Couldn't cast the value ({value}) to {cast_type.__name__}")
            elif self.warnings:
                print(f"Warning: Couldn't cast the value ({value}) to {cast_type.__name__}")
            
            return value

    def get_multiple_input(self, types:list[type]=[str], text:str=default_kit["text"], separator:str=default_kit["separator"], iter_separator:str=default_kit["iter_separator"], input_streamsize:int=None) -> list:
        """This function gets multiple inputs in a single line, separated by a separator (default is `" "`)
            
            Then the inputs are casted to the type we put at the same position into `types`
            
            params:
                `types`:list[Any], default:[str] -> this list contains the types to cast the values to
                
                `text`:str, default:`""` -> the text of the input function
                
                `separator`:str, default:`" "` -> this string is used to split the input values
                
                `input_streamsize`:int, default: None -> substitute property self.streamsize without changing its value (value can be higher than self.streamsize)
                
            returns:
                `values`:list -> This list contains the elaborated data insert in input
                
            ~ If self.warnings is set on True, the function will show you any warnings/errors ~
            
            ~ If self.raise_exceptions is set on True, the function will raise exceptions if needed ~
        """
        if not self.__check_kit(): # if there's an error in the kit, replaces it with the default kit
            self.kit: dict[str, str] = InputDevice.default_kit
        
        text = text if isinstance(text, str) else self.kit["text"]
        separator = separator if isinstance(separator, str) and separator else self.kit["separator"]
        iter_separator = iter_separator if isinstance(iter_separator, str) and iter_separator else self.kit["iter_separator"]
        
        if separator == iter_separator:
            if self.raise_exceptions:
                raise WrongArgumentError(f"Items separator ({separator}) and iter_separator ({iter_separator}) cannot be equal")
            elif self.warnings:
                print(f"Items separator ({separator}) and iter_separator ({iter_separator}) cannot be equal")
                return
        
        if not input_streamsize or input_streamsize < 1:
            input_streamsize = self.streamsize
        elif input_streamsize == -1:
            input_streamsize = None
                
        values:list[str] = input(text).split(separator)[0:input_streamsize if input_streamsize else None] # gets the input from index 0 to input_streamsize, if input_streamsize is None gets all the values from 0 to self.streamsize (if None gets all the values)
        types = types[0:input_streamsize if input_streamsize else None]
        
        return self.process_data(values, types, iter_separator, input_streamsize)
