from setuptools import setup, find_packages

setup(
    name='script',
    version='0.0.3',
    packages= find_packages(),
    install_requires=[
        'click',
        'bullet',
        'requests',
        'pandas',
        'pyfiglet',
        'google-cloud-storage'
    ],
    entry_points='''
    [console_scripts]
    crawl = script:crawl
    '''
)