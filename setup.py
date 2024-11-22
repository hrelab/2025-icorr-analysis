from setuptools import setup, find_packages

setup(
    name='icorr',  # Library name (matches [project] name in pyproject.toml)
    version='0.1.0',  # Replace with your version or use a dynamic solution
    author_email='your.email@example.com',  # Optional: Add your email
    url='https://github.com/yourusername/icorr',  # Optional: Add your repository
    packages=find_packages(where='src'),  # Use 'src' directory for package discovery
    package_dir={'': 'src'},  # Map the package root to 'src'
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas'
    ],
)
