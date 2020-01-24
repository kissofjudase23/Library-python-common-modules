import glob
import json
import os
import subprocess
import shutil
import pickle
import pathlib

from common.exc import HDFSError, SubProcessError


class HDFSUtils(object):
    @staticmethod
    def mkdir(path):
        p = subprocess.run(['hadoop', 'fs', '-mkdir', '-p', path])
        if p.returncode != 0:
            raise HDFSError(f'create hdfs path:{path} error')

    @staticmethod
    def rm(path):
        p = subprocess.run(['hadoop', 'fs', '-rm', '-r', path])
        if p.returncode != 0:
            raise HDFSError(f'rm path:{path} error')

    @staticmethod
    def put(src_path, dst_path):
        p = subprocess.run(['hadoop', 'fs', '-put', '-f', src_path, dst_path])
        if p.returncode != 0:
            raise HDFSError(f'put file:{src_path} to hdfs:{dst_path} error')


class FileUtility(object):

    @staticmethod
    def get_file_len(file_path):
        """ get the line number of fname
        """
        p = subprocess.run(['wc', '-l', file_path],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           encoding="utf-8")

        try:
            p.check_returncode()
        except subprocess.CalledProcessError as e:
            raise SubProcessError(f"{e}, err={p.stdout}") from e

        return int(p.stdout.strip().split()[0])

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
        p = pathlib.Path(dir_path)
        p.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def rm_folder(dir_path):
        if not os.path.isdir(dir_path):
            return

        shutil.rmtree(dir_path)

    @staticmethod
    def rm_file(file_path):
        if not os.path.isfile(file_path):
            return
        os.unlink(file_path)

    @classmethod
    def _get_glbo_path(cls,
                       root_dir,
                       *,
                       file_prefix,
                       file_suffix,
                       recursive):

        file_name = '*'

        if file_prefix:
            file_name = f'{file_prefix}{file_name}'

        if file_suffix:
            file_name = f'{file_name}{file_suffix}'

        glob_path = root_dir

        if recursive:
            """
            If recursive is true, the pattern '**' will match any files and zero or more directories,
            subdirectories and symbolic links to directories.
            If the pattern is followed by an os.sep or os.altsep then files will not match.
            """
            glob_path = os.path.join(glob_path, '**')

        glob_path = os.path.join(glob_path, file_name)

        return glob_path

    @classmethod
    def get_file_list(cls,
                      root_dir,
                      *,
                      file_prefix=None,
                      file_suffix=None,
                      recursive=False,
                      sort=False,
                      limit=None):

        glob_path = cls._get_glbo_path(root_dir,
                                       file_prefix=file_prefix,
                                       file_suffix=file_suffix,
                                       recursive=recursive)

        files = glob.glob(glob_path, recursive=recursive)

        if sort:
            files.sort()

        if limit:
            return files[:limit]

        return files

    @classmethod
    def get_file_list_generator(cls,
                                root_dir,
                                *,
                                recursive=False,
                                file_prefix=None,
                                file_suffix=None):

        glob_path = cls._get_glbo_path(root_dir,
                                       file_prefix=file_prefix,
                                       file_suffix=file_suffix,
                                       recursive=recursive)

        return glob.iglob(glob_path, recursive=recursive)
