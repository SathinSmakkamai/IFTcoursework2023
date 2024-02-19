import os

root_files = ['.gitignore', 'README.md', 'bitbucket-pipelines.yml']
exclude_dirs_test = ['000.DataBases', '.git', '.gitignore', 'README.md', 'CHANGELOG.md', '000.Tests', '.pytest_cache']
folders_level_one = ['1.CourseworkOne', '2.CourseworkTwo', '3.CourseworkThree']
files_coursework_one = ['1.SQLQueries.sql','2.NoSQLQueries.js','README.md']

def check_files_cw_one(exclude_dirs_test, folders_level_one, files_coursework_one):
    list_repo_dirs = next(os.walk('.'))[1]    
    clean_dirs = [v for v in list_repo_dirs if v not in exclude_dirs_test]
    breaches_cw_one = []

    for single_dir in clean_dirs:
        files_cw_one = os.path.join('.', single_dir, folders_level_one[0])
        
        if not os.path.exists(files_cw_one):
            breaches_cw_one.append('Folder Coursework One missing for {}'.format(single_dir))
            continue
        
        list_files_cw_one_all = next(os.walk(files_cw_one))[2]      
        list_files_cw_one = [x for x in list_files_cw_one_all if x != '.gitkeep']

        if len(list_files_cw_one) == 0: continue

        files_matching = [x for x in list_files_cw_one if x in files_coursework_one]
        if len(files_matching) != 3:
            breaches_cw_one.append('Files coursework one missing for {}'.format(single_dir))        
    return breaches_cw_one

def check_dirs_level_one(exclude_dirs_test, folders_level_one):
    list_repo_dirs = next(os.walk('.'))[1]    
    clean_dirs = [v for v in list_repo_dirs if v not in exclude_dirs_test]

    breaches = []

    for single_dir in clean_dirs:
        check_one = os.path.join('.', single_dir)
        list_student_dirs = next(os.walk(check_one))[1]
        if not all(x in list_student_dirs for x in folders_level_one):
            breaches.append('Coursework folder mismatch for student {}'.format(single_dir))
    print(breaches)
    return breaches

"""

Function    : check_change_log
Purpose     : check that CHANGELOG.md file is included
Arguments   :
            - excluded_dirs_test: list of directories to be excluded from integration testing

"""

def check_change_log(exclude_dirs_test):
    list_repo_dirs = next(os.walk('.'))[1]    
    clean_dirs = [v for v in list_repo_dirs if v not in exclude_dirs_test]

    breaches = []

    for single_dir in clean_dirs:
        check_one = os.path.join('.', single_dir)
        list_student_files = next(os.walk(check_one))[2]
        if len(list_student_files) == 0:
           breaches.append('Changelog file missing for student {}'.format(single_dir)) 
        elif not any(x == 'CHANGELOG.md' for x in list_student_files):        #if not list_student_files == 'CHANGELOG.md':
            breaches.append('Changelog file missing for student {}'.format(single_dir))
    return breaches

"""

Function    : check_main_cw
Purpose     : check that all mandatory files for cw two or cw three are in relevant folder
Arguments   :
            - excluded_dirs_test: list of directories to be excluded from integration testing
            - folders_level_one : list of folders expected to be in coursework
            - posit             : which coursework (2 or 3) int
            - check_file_name   : which file name should be checked.

"""

def check_main_cw(exclude_dirs_test, folders_level_one, posit, check_file_name):
    list_repo_dirs = next(os.walk('.'))[1]    
    clean_dirs = [v for v in list_repo_dirs if v not in exclude_dirs_test]
    breaches_cw_main = []

    for single_dir in clean_dirs:
        files_cw_one = os.path.join('.', single_dir, folders_level_one[posit])
        
        if not os.path.exists(files_cw_one):
            breaches_cw_main.append('Folder Coursework {} missing for {}'.format(str(posit+1),single_dir))
            continue
        
        list_files = next(os.walk(files_cw_one))[2]
        
        list_files_main = [x for x in list_files if x != '.gitkeep']

        if len(list_files_main) == 0:
            continue    
        
        if not any(s.startswith(check_file_name) for s in list_files_main):
            breaches_cw_main.append('{} file in coursework {} missing for {}'.format(
                check_file_name,
                str(posit+1), 
                single_dir))        
    return breaches_cw_main

"""

Function    : mandatory_folder_present
Purpose     : check that all mandatory folders are in folder and they haven't been removed     

"""


def mandatory_folder_present():
    list_repo_dirs = next(os.walk('.'))[1]   

    return all(x for x in ['000.DataBases', '000.Tests', 'LucaCocconcelli'] if x in list_repo_dirs)

"""

Function    : mandatory_files_present
Purpose     : check that all mandatory files are in folder and they haven't been removed
Argument    :
            - root_files    : files in root folder that must be included in commit.

"""

def mandatory_files_present(root_files):
    list_repo_files = next(os.walk('.'))[1]
    return all(x for x in root_files if x in list_repo_files)
"""

Function    : folders_cw_two
Purpose     : test all expected folders are present for coursework two

"""

def folders_cw_two(posit):
    list_repo_dirs = next(os.walk('.'))[1]    
    clean_dirs = [v for v in list_repo_dirs if v not in exclude_dirs_test]
    breaches_cw_two = []

    for single_dir in clean_dirs:
        files_cw_two = os.path.join('.', single_dir, folders_level_one[posit])
        
        if not os.path.exists(files_cw_two):
            breaches_cw_two.append('Folder Coursework One missing for {}'.format(single_dir))
            continue
        
        list_files_cw_two_all = next(os.walk(files_cw_two))
        list_files_cw_two = [x for x in list_files_cw_two_all[1] if x != '.gitkeep']

        if len(list_files_cw_two) == 0: continue
        folders_missing = [x for x in ['config', 'modules', 'static', 'test'] if x not in list_files_cw_two_all[1]]

        if len(folders_missing) != 0:
            breaches_cw_two.append('Missing folders {} for Coursework {} in {}'.format(' , '.join(folders_missing), 
                                                                                       posit+1, single_dir))    
    return breaches_cw_two


"""

Function    : check_config_cw
Purpose     : check that all config files for cw two and cw three are in relevant folder
Arguments   :
            - excluded_dirs_test: list of directories to be excluded from integration testing
            - folders_level_one : list of folders expected to be in coursework
            - posit             : which coursework (2 or 3) int

"""

def check_config_cw(exclude_dirs_test, folders_level_one, posit):
    list_repo_dirs = next(os.walk('.'))[1]    
    clean_dirs = [v for v in list_repo_dirs if v not in exclude_dirs_test]
    breaches_cw_conf = []

    for single_dir in clean_dirs:
        files_cw_one = os.path.join('.', single_dir, folders_level_one[posit])
        
        if not os.path.exists(files_cw_one):
            breaches_cw_conf.append('Folder Coursework {} missing for {}'.format(str(posit+1),single_dir))
            continue
        
        list_files = next(os.walk(files_cw_one))[2]
        
        list_files_main = [x for x in list_files if x != '.gitkeep']

        if len(list_files_main) == 0:
            continue    
        py_file = [x for x in list_files if x in ['Main.py', 'App.py']]
        r_file = [x for x in list_files if x in ['Main.R', 'App.R', 'Global.R']]
        if len(py_file) == 1:
            config_file_path = os.path.join('.', single_dir, folders_level_one[posit], 'config', 'conf.yaml')
            if not os.path.exists(config_file_path):
                breaches_cw_conf.append('config yaml file in coursework {} missing for {}'.format(str(posit+1), single_dir))        
        elif len(r_file) == 1:
            config_file_path = os.path.join('.', single_dir, folders_level_one[posit], 'config', 'script.config')
            params_file_path = os.path.join('.', single_dir, folders_level_one[posit], 'config', 'script.params')
            if not os.path.exists(config_file_path) or not os.path.exists(params_file_path):
                breaches_cw_conf.append('Config or Params file in coursework {} missing for {}'.format(str(posit+1), single_dir))
        else:
            breaches_cw_conf.append('Main.py or Main.R file in coursework {} missing for {}'.format(str(posit+1), single_dir))    
    
    return breaches_cw_conf
