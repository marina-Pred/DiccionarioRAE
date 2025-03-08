from setuptools import setup, find_packages

setup(
    name='DiccionarioRAE',
    version='1.0.0',
    description='Herramienta para interactuar con el diccionario de la RAE.',
    author='Marina P.C.',
    packages=find_packages(),  
    install_requires=[
        'beautifulsoup4', 'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)