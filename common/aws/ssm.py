# -*- coding: utf-8 -*-

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from ..exc import SSMListParameterError


class Utils(object):
    """
    Please refer
    https://boto3.readthedocs.io/en/latest/reference/services/ssm.html#SSM.Client.get_parameters
    for detail
    """
    def __init__(self, logger, max_retry=3):

        retry_config = Config(
            retries=dict(
                max_attempts=max_retry
            )
        )

        self.ssm = boto3.client(service_name='ssm',
                                config=retry_config)
        self.logger = logger

    def list_parameters(self, parameter_list, with_decryption=True):
        """
        :param parameter_list: Names of the parameters for which you want to query information.
        :param with_decryption:  Return decrypted secure string value
        :return:
        """
        try:
            res = self.ssm.get_parameters(Names=parameter_list,
                                          WithDecryption=with_decryption)
            return res['Parameters']

        except ClientError as e:
            self.logger.error(e)
            raise SSMListParameterError(f'list parameter for {parameter_list} failed') from e


if __name__ == '__main__':
    pass
