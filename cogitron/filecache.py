import platformdirs
import os

cachefolder = platformdirs.user_cache_path().joinpath("cogitron")

def filecache_str(file_name, validation_function):
    """
    Stores the result of the function in a file inside the cache folder.
    The output is transformed using the 'str' function.

    The validation function gets the saved output as an argument.
    If it returns True, the cached value is used. Otherwise
    a new value is created.
    """
    
    def decorator(original_func):
        cache_path = cachefolder.joinpath(file_name)
        
        def new_func():
            try:
                with open(cache_path, "r") as file:
                    value = file.read()
            except:
                value = str(original_func())
                os.makedirs(cachefolder, exist_ok=True)
                with open(cache_path, "w+") as file:
                    file.write(value)
                return value

            if not validation_function(value):
                value = str(original_func())
                os.makedirs(cachefolder, exist_ok=True)
                with open(cache_path, "w+") as file:
                    file.write(value)
                return value
            return value
            
        return new_func
    return decorator