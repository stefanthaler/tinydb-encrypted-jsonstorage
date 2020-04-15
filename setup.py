import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='tinydb-encrypted-jsonstorage',
     version='0.0.1',
     author="Stefan Thaler",
     author_email="bruthaler@gmail.com",
     description="A TinyDB storage implementation that uses JSON and AES encryption.",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/stefanthaler/tinydb-encrypted-jsonstorage",
     packages=setuptools.find_packages(),
     install_requires=[
          'tinydb',
          'pycryptodome',
     ],
     tests_require=[
      'nose' #  python setup.py test / nosetests
     ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
