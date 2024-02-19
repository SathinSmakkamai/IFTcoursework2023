import pytest
# from checks_functions import checkDirsLevelOne, checkFilesCwOne, checkChangeLog, checkMainCw
import checks_functions as cf

Root_files = ['.gitignore', 'README.md', 'bitbucket-pipelines.yml', '.flake8', '.lintr', 'docker-compose.yml']
Files_coursework_one = ['1.SQLQueries.sql','2.NoSQLQueries.js','README.md']
Exclude_dirs_test = ['000.DataBases', '.git', '.gitignore', 'README.md', 'CHANGELOG.md', '000.Tests', '.pytest_cache', 'Student_00000000']
Folders_level_one = ['1.CourseworkOne', '2.CourseworkTwo']



"""

Test Case: CHANGELOG.md file included in submission

"""
def test_change_log_included():    
    test_data_changelog = cf.check_change_log(exclude_dirs_test=Exclude_dirs_test)
    print(test_data_changelog)
    assert len(test_data_changelog) == 0




def test_files_cw_one():
    test_files_cw_one = cf.check_files_cw_one(Exclude_dirs_test, Folders_level_one, Files_coursework_one)
    print(test_files_cw_one)
    assert len(test_files_cw_one) == 0



"""

Test case: no mandatory folders are removed

"""
def test_folders_mandatory():
    assert cf.mandatory_folder_present()

"""

Test case: no mandatory files are removed

"""
def test_files_mandatory():
    assert cf.mandatory_files_present(Root_files)

