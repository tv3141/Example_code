Quickstart:

    > pip install
    > download_files -n 8 test_urls.txt file_storage

The tool ``download_files`` downloads files from URLs given in a file in
parallel into a single directory.
Existing files are not overwritten, but the event is logged. Additionally,
common exceptions, such as HTTP errors, SSL errors, or timeouts are caught and 
logged.

I also added some example tests, testing the user interface and the behaviour
when the download of a file fails. 
 

