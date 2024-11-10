from setuptools import setup, find_packages

setup(
    name='your-package-name',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Dependencies, e.g.,
        # 'numpy>=1.18.0',
    ],
    include_package_data=True,
    license='MIT',
    description='A short description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/your-repo-name',
    author='Your Name',
    author_email='your.email@example.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
