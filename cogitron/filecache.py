from os import path
import pickle
import platformdirs
import inspect

CACHE_PATH = path.join(platformdirs.user_cache_dir("cogitron"))

def filecache(validation_function=None):
        def decorator(func):
            function_id = f"function-{str(func.__name__)}"
            cache_filepath = path.join(CACHE_PATH, function_id)

            if validation_function != None:
                def wrapper():
                    try:
                        with open(cache_filepath, "r") as file:
                            value = pickle.load(file)
                        is_valid = validation_function(value)
                        if is_valid:
                            return value
                        else:
                            value = func()
                            with open(cache_filepath, "w") as file:
                                pickle.dump(value, file)
                            return value
                    except Exception as e:
                        value = func()
                        with open(cache_filepath, "w") as file:
                            pickle.dump(value, file)
                        return value

                return wrapper
            else:
                def wrapper():
                    try:
                        with open(cache_filepath, "r") as file:
                            value = pickle.load(file)
                        return value
                    except Exception as e:
                        value = func()
                        with open(cache_filepath, "w") as file:
                            pickle.dump(value, file)
                        return value

                return wrapper 
        return decorator
        
