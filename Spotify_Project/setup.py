from setuptools import setup, find_packages

requires = [
    'flask',
    'spotipy',
    'requests',
    'os',
    'json',
    'time',
    'Jinja2'
]

setup(
    name='SongTyr',
    version='1.0',
    description='An application that retrieves a users Spotify songs to create an html/js visualization',
    author='Christian Hackelman',
    author_email='cphackelman@ou.edu',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)