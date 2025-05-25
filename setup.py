from setuptools import setup,find_packages

def get_requirements(file_name):
    with open(file_name) as file:
        modules = file.readlines()
        packages = [i.replace('\n','') for i in modules]
    libraries = [i for i in packages if i not in ['','-e .']]
    return libraries

setup(
    name='NetworkSecurity',
    version='0.0.1',
    author='Azhar Siddiqui',
    author_email='azhar.sid@icloud.com',
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')

)