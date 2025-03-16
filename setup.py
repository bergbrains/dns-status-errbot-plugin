from setuptools import setup, find_packages

setup(
    name='dns-status-errbot-plugin',
    version='1.0.0',
    description='Errbot plugin for checking DNS server responsiveness and resolution time',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/dns-status-errbot-plugin',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'errbot>=6.0.0',
        'dnspython>=2.0.0',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Errbot',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Chat',
        'Topic :: System :: Monitoring',
        'Topic :: System :: Networking',
    ],
)
