from setuptools import setup, Extension

setup(
    ext_modules=[
        Extension(
            "query_device",
            sources=["cogitron/query_device/query_device.c"],
            extra_link_args=["-lsystemd", "-lcap"]
        )
    ]
)
