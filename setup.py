import os

import setuptools

README_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'README.md')
with open(README_PATH) as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name='i3-scratchpad',
    version='0.0.1-alpha',
    description='Manage i3wm workspaces in groups you control',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/infokiller/i3-scratchpad',
    author='infokiller',
    author_email='joweill@icloud.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='i3 i3wm extensions add-ons',
    packages=setuptools.find_packages(),
    install_requires=['i3ipc'],
    scripts=[
        'scripts/i3-scratchpad',
    ],
)
