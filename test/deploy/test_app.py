"""Testing code generated by nbdev in unpackai/deploy/app.py"""
# Generated automatically from notebook nbs/51_deploy_app.ipynb

from unpackai.deploy.app import *

# Test Cell
# For Test Cases (might have duplicate import because it will be in a dedicated file)
import re
from pathlib import Path
from typing import List

import pytest
from test_common.utils_4_tests import DATA_DIR, diff_files

DEPLOY_DATA_DIR = DATA_DIR / "deploy"

# Test Cell
def test_streamlit_cv_fastai(tmp_path):
    """Test Streamlit app for CV with fastai"""
    dest = tmp_path / "app_cv_fastai.py"
    StreamlitApp("CV").render_fastai(
        title="Is it a cat?", author="Jeff", model="model.pkl"
    ).append(
        """
        st.sidebar.write("---")
        st.sidebar.button("Show Balloons", on_click=st.balloons)
        """
    ).save(
        dest=dest
    )

    assert diff_files(DEPLOY_DATA_DIR / "app_CV.py", dest, show=True) == ""


# Test Cell
def test_streamlit_tabular_pycaret(tmp_path):
    """Test Streamlit app for Tabular with pycaret"""
    dest = tmp_path / "app_tabular_pycaret.py"
    StreamlitApp("Tabular").render_pycaret(
        title="My Mini Tabular App", author="Jeff", model="model.pkl", module="regression"
    ).save(dest=dest)

    assert diff_files(DEPLOY_DATA_DIR / "app_Tabular.py", dest, show=True) == ""


# Test Cell
def test_custom_app_code(tmp_path):
    """Test custom app with code provided via string"""
    dest = tmp_path / "app_custom_code.py"
    code = """
        st.write("hello")
        st.balloons()
    """
    StreamlitAppCustom().render("Custom App", "Jeff", code).save(dest=dest)

    assert diff_files(DEPLOY_DATA_DIR / "app_custom.py", dest, show=True) == ""


# Test Cell
def test_custom_app_external(tmp_path):
    """Test custom app with code provided via string"""
    dest = tmp_path / "app_custom_external.py"

    StreamlitAppCustom().render(
        "Custom App", "Jeff", DEPLOY_DATA_DIR / "correct_code_for_custom_app.py"
    ).save(dest=dest)

    # Because we have a absolute path of "test_data/deploy", we will replace by relative path
    # otherwise our tests will always be failed
    content = dest.read_text(encoding="utf-8").replace(
        str(DEPLOY_DATA_DIR), "<deploy_dir>"
    )
    content = content.replace(">\\", ">/").replace(
        'r"<deploy_dir>/', 'Path(__file__).parent / "'
    )
    dest.write_text(content, encoding="utf-8")

    assert diff_files(DEPLOY_DATA_DIR / "app_custom_external.py", dest, show=True) == ""
