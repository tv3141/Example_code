# -*- coding: utf-8 -*-
import download_files
import requests
import pytest
from requests.exceptions import HTTPError, Timeout


class Test_download_url():

    def test_catch_HTTP_errors(self):
        """Tests that HTTP errors are caught."""
        # patch requests.get to raise exception
        def raise_HTTPError(*args):
            raise HTTPError
        requests.get = raise_HTTPError

        url = 'string'
        directory = 'non_existent_dir'
        try:
            download_files.download_url(directory, url)
        except FileNotFoundError:
            pass


    def test_catch_Timeout(self):
        """Tests that request timeouts are caught."""
        # patch requests.get to raise exception
        def raise_Timeout(*args):
            raise Timeout
        requests.get = raise_Timeout

        url = 'string'
        directory = 'non_existent_dir'
        try:
            download_files.download_url(directory, url)
        except FileNotFoundError:
            pass


class Test_parse_args():

    def test_required_args(self):
        """Tests which command line options are required."""
        args = ['file_with_urls.txt',
                'directory']

        # leave one out
        for i in range(len(args)):
            _args = args[:]
            _args.pop(i)
            with pytest.raises(SystemExit):
                download_files.parse_args(_args)


    def test_parse_all_args(self):
        """Tests that all command line options are available."""
        args = ['file_with_urls.txt',
                '/foo/bar',
                '-n', '2']
        parsed_args = download_files.parse_args(args)
        print(parsed_args)
        assert parsed_args.nprocs == 2
        assert parsed_args.file_with_urls == 'file_with_urls.txt'
        assert parsed_args.directory == '/foo/bar'

