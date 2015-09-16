# static-file-server

This little service is made to ease hosting static files. It makes use of Simple HTTP server included in Python3 `http.server` module.

You can use it to host:
* _Single file_: `armada run static-file-server --rename single-file-host -v /path/to/some/file_on_host.txt`
  * When you open hosting site you will see only link to this file
* _Single directory_: `armada run static-file-server --rename single-dir-host -v /path/to/some/dir_on_host/`
  * When you open hosting site you will see directly content of this directory
* _Combinations of above_ : `armada run static-file-server --rename massive-hosting -v /path/to/some/file_on_host.txt -v /path/to/some/dir_on_host -v /path/to/duplicate/dir_on_host`
  * In this case you will see list of files and directories specified with `-v` parameter, if names are duplicated then increasing counter is appended to file/directory name (so second entry will be named `dir_on_host1`)
