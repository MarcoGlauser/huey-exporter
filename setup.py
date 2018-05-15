from setuptools import find_packages, setup

setup(
        name='huey-exporter',
        version='0.1.1',
        description=' Huey exporter for Prometheus',
        url='https://github.com/MarcoGlauser/huey-exporter',
        author='Marco Glauser',
        license='MIT',
        packages=find_packages(),
        include_package_data=True,
        install_requires=[
            'prometheus_client>=0.2.0',
            'huey>=1.9.0',
            'click>=6.7',
            'redis>=2.10.6',
        ],
        entry_points={
          'console_scripts': [
              'huey_exporter = huey_exporter.exporter:main'
          ]
        }
)
