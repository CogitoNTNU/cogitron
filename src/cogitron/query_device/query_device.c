#define PY_SSIZE_T_CLEAN
#include <systemd/sd-device.h>
#include <Python.h>


static PyObject *
query_device_get_devpath(PyObject *self, PyObject *args)
{
    const char *filepath;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &filepath))
        return NULL;

    sd_device* device = NULL; 
    sts = sd_device_new_from_devname(&device, filepath);

    if (sts < 0){
        PyErr_SetString(PyExc_ValueError, "Unable to create sd device. Make sure you input a valid device path.");
        return NULL;
    }

    const char* devpath;
    sts = sd_device_get_devpath(device, &devpath);

    if (sts < 0){
        PyErr_SetString(PyExc_RuntimeError, "Internal error. Unable to obtain devpath from the device.");
        return NULL;
    }
    
    return PyUnicode_FromString(devpath);
}

static PyMethodDef query_device_methods[] = {
    {"get_devpath",  query_device_get_devpath, METH_VARARGS,
     "Get the devpath of a linux device file"},
    
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


static struct PyModuleDef query_device_module = {
    .m_methods = query_device_methods
};

PyMODINIT_FUNC
PyInit_query_device(void)
{
    return PyModuleDef_Init(&query_device_module);
}


main(int argc, char *argv[])
{
    PyStatus status;
    PyConfig config;
    PyConfig_InitPythonConfig(&config);

    /* Add a built-in module, before Py_Initialize */
    if (PyImport_AppendInittab("query_device", PyInit_query_device) == -1) {
        fprintf(stderr, "Error: could not extend in-built modules table\n");
        exit(1);
    }

    /* Pass argv[0] to the Python interpreter */
    status = PyConfig_SetBytesString(&config, &config.program_name, argv[0]);
    if (PyStatus_Exception(status)) {
        goto exception;
    }

    /* Initialize the Python interpreter.  Required.
       If this step fails, it will be a fatal error. */
    status = Py_InitializeFromConfig(&config);
    if (PyStatus_Exception(status)) {
        goto exception;
    }
    PyConfig_Clear(&config);

    /* Optionally import the module; alternatively,
       import can be deferred until the embedded script
       imports it. */
    PyObject *pmodule = PyImport_ImportModule("query_device");
    if (!pmodule) {
        PyErr_Print();
        fprintf(stderr, "Error: could not import module 'query_device'\n");
    }

    // ... use Python C API here ...

    return 0;

    exception:
        PyConfig_Clear(&config);
        Py_ExitStatusException(status);
}

