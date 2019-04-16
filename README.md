# Mediaorganiser

This little dumb python script organises a bunch of photos and videos into folders with the format `./YYYYMM`.
It scans the files and tries to work out the creation date from:

-  The file name (with or without prefixes)
-  The EXIF data (JPEG, TIFF, GIF, PNG, BMP, DNG)
-  RAW file data (RW2, CR2)
-  The file system metadata

If the script can't work out the date, then it copies the file to an `./undated` folder.

## Installation

Just install the dependencies:

```
$  pip install -r requirements.txt
```

## Usage

``
mediaorganiser -d DIR
``

The date folders will be created in the given directory. The script is not recursive, only the files directly into the given directory will be treated.
