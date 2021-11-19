import setuptools
from configparser import ConfigParser
from pathlib import Path
from pkg_resources import parse_version

assert parse_version(setuptools.__version__) >= parse_version("36.2")

# note: all settings are in settings.ini; edit there, not here
config = ConfigParser(delimiters=["="])
config.read("settings.ini")
cfg = config["DEFAULT"]

cfg_keys = "version description keywords author author_email".split()
expected = (
    cfg_keys
    + "lib_name user branch license status min_python audience language".split()
)
for exp in expected:
    assert exp in cfg, f"missing expected setting: {exp}"
setup_cfg = {k: cfg[k] for k in cfg_keys}

licenses = {
    "apache2": (
        "Apache Software License 2.0",
        "OSI Approved :: Apache Software License",
    ),
    "MIT": ("MIT", "OSI Approved :: MIT License"),
}
statuses = [
    "1 - Planning",
    "2 - Pre-Alpha",
    "3 - Alpha",
    "4 - Beta",
    "5 - Production/Stable",
    "6 - Mature",
    "7 - Inactive",
]
py_versions = (
    "2.0 2.1 2.2 2.3 2.4 2.5 2.6 2.7 3.0 3.1 3.2 3.3 3.4 3.5 3.6 3.7 3.8".split()
)

requirements = cfg.get("requirements", "").split()
license_info = licenses[cfg["license"]]
min_python = cfg["min_python"]
comp_version = py_versions[py_versions.index(min_python) :]
doc_url = cfg["doc_host"] + cfg["doc_baseurl"]

setuptools.setup(
    name=cfg["lib_name"],
    license=license_info[0],
    classifiers=[
        "Development Status :: " + statuses[int(cfg["status"])],
        "Intended Audience :: " + cfg["audience"].title(),
        "License :: " + license_info[1],
        "Natural Language :: " + cfg["language"].title(),
    ]
    + [f"Programming Language :: Python :: {v}" for v in comp_version],
    url=f"https://github.com/{cfg['user']}/{cfg['lib_name']}",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        "PDF": ["pdfminer.six"],
        "deploy": ["streamlit", "pyngrok", "jinja2", "black"],
    },
    python_requires=">=" + cfg["min_python"],
    long_description=Path("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    project_urls={
        "Documentation": doc_url,
        "Tracker": "https://github.com/unpackAI/unpackai/issues",
    },
    zip_safe=False,
    entry_points={"console_scripts": cfg.get("console_scripts", "").split()},
    **setup_cfg,
)
