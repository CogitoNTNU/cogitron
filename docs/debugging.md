# illegal instruction
If the program gives you an "illegal instruction" error then this is because of binary incompatibility.
You can debug this problem by using running:
```bash
export PYTHONFAULTHANDLER=1
```
Then, in the same terminal, run the script which causes the error. You will then get a backtrace over which
function call and module which causes the error 

## Pyarrow
The illegal instruction error occurs when using arm-v8 hardware with pyarrow version 21. Detailed discussion can be found [here](https://github.com/apache/arrow/issues/47229).

To fix the problem you can install version 20 of arrow with the appropiate .whl from the [arrow repo](https://github.com/apache/arrow/releases/tag/apache-arrow-20.0.0). Alternativly, you can build pyarrow from source.