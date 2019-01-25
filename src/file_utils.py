import glob
import json
import os
import pickle
import shutil


class FileUtility(object):

    @staticmethod
    def read_json_file(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    @staticmethod
    def write_json_file(file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def read_pickle_file(file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)

    @staticmethod
    def write_pickle_file(file_path, data):
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)

    @staticmethod
    def mkdir_p(dir_path):
        if os.path.isdir(dir_path):
            return

        os.makedirs(dir_path)

        return dir_path

    @staticmethod
    def delete_folder(folder):
        if folder and os.path.isdir(folder):
            shutil.rmtree(folder)

    @staticmethod
    def remove_and_create_folder(folder):
        if os.path.exists(folder):
            if os.path.isdir(folder):
                shutil.rmtree(folder, ignore_errors=True)
            else:
                os.remove(folder)

        FileUtility.mkdir_p(folder)

    @staticmethod
    def get_file_list(root_dir, *,
                      file_prefix=None,
                      file_suffix=None,
                      recursive=False,
                      sort=False,
                      limit=None):

        # It would return an empty list if the root_dir does not exist
        file_name = '*'

        if file_prefix:
            file_name = f'{file_prefix}{file_name}'

        if file_suffix:
            file_name = f'{file_name}{file_suffix}'

        path_name = root_dir

        if recursive:
            path_name = os.path.join(path_name, '**')

        path_name = os.path.join(path_name, file_name)

        files = glob.glob(path_name, recursive=recursive)

        if sort:
            files.sort()

        if limit:
            return files[:limit]

        return files

    @staticmethod
    def get_file_generator(root_dir, *,
                           recursive=False,
                           file_prefix=None,
                           file_suffix=None):

        file_name = '*'

        if file_prefix:
            file_name = f'{file_prefix}{file_name}'

        if file_suffix:
            file_name = f'{file_name}{file_suffix}'

        path_name = root_dir

        if recursive:
            path_name = os.path.join(path_name, '**')

        path_name = os.path.join(path_name, file_name)

        return glob.iglob(path_name, recursive=recursive)

    @staticmethod
    def delete_file(file_path):
        if file_path and os.path.isfile(file_path):
            os.unlink(file_path)
