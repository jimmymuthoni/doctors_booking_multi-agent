from setuptools import find_packages, setup
from typing import List

#function to get all requirements and return them as a List
def get_requirements()->List:
    requirements_list: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirements_list.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirements_list
print(get_requirements())

setup(
    name = 'doctors_appointment_booking',
    version = '0.0.1',
    author = "jimmy muthoni",
    author_email = "jimmymuthoni26@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements(),
    python_requires=">=3.10",
)

