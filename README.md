## Organise in folders

This little python script organises a bunch of photos and files in folders by date with the format `./YYYYMM`.
It recognises the following prefixes:
*  `IMG-` + date
*  `IMG_` + date
*  `VID-` + date
*  `VID_` + date
*  `PANO_` + date
*  `PHOTO_` + date

It also recognises dates in the filename as `YYYY-MM-DD`. If the script can't work out the date, then it copies the file to an `./undated` folder.

### Usage

``
organiseinfolders.py -d DIRECTORY_WITH_FILES
``

The date folders will be created in the given directory. The script is not recursive, only the files directly into the given directory will be treated.
