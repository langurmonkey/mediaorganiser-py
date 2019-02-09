#!/usr/bin/env python

from os import walk
import argparse, os, shutil, re
import exifread, subprocess

parser = argparse.ArgumentParser(description='Process some integers.')
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument("-d", "--dir",  help="The directory", required=True)
args = parser.parse_args()

if not os.path.isdir(args.dir):
    print("%s is not a directory" % args.dir)
    exit()

def move(folder, yearmonth, filename, i, n):
    datefolder = os.path.join(folder, yearmonth)

    if not os.path.exists(datefolder):
        os.makedirs(datefolder)

    # Move
    shutil.move(os.path.join(folder, filename), os.path.join(datefolder, filename))
    
    # Info
    print("%d of %d - %d%% completed: %s -> %s" % (i, n, i*100.0/n, filename, yearmonth))


# CONSTANTS
prefixes = ['VID_', 'VID-', 'IMG_', 'IMG-', 'PHOTO_', 'PANO_', 'AUD-']
regexps = ['(\d{4})-(\d{2})-(\d{02}).*', '(\d{4})-(\d{2})-(WA\d{02}).*']
extexif = ['.jpg']
extraw = ['.rw2', '.cr2']
undatedfolder = os.path.join(args.dir, "undated")

# MAIN SCRIPT
for (dirpath, dirnames, filenames) in walk(args.dir):
    n = len(filenames)
    i = 1
    for filename in filenames:
        found = False

        ##################
        # PREFIXES
        ##################
        for prefix in prefixes:
            if filename.startswith(prefix):
                yearmonth = filename[len(prefix):len(prefix) + 6]

                found = True
                move(args.dir, yearmonth, filename, i, n)
                i = i+1
                break

        ##################
        # REGEXP
        ##################
        for regexp in regexps:
            pattern = re.compile(regexp)
            if not found and pattern.match(filename):
                yearmonth = filename[:4] + filename[5:7]

                found = True
                move(args.dir, yearmonth, filename, i, n)
                i = i+1
                break


        ############################
        # EXIF with extensions     #
        ############################
        for extension in extexif:
            if not found and filename.lower().endswith(extension.lower()):
                f = open(filename, 'rb')
                tags = exifread.process_file(f)
                
                datetime = tags['Image DateTime'].values
                yearmonth = datetime[:4] + datetime[5:7]

                found = True
                move(args.dir, yearmonth, filename, i, n)
                i = i + 1 
                break

        ############################
        # RAW with extensions      #
        ############################
        for extension in extraw:
            if not found and filename.lower().endswith(extension.lower()):
                result = subprocess.run(['identify', '-verbose', args.dir + filename], stdout=subprocess.PIPE)
                resstr = result.stdout.decode('utf-8')

                for line in resstr.splitlines():
                    if line.strip().startswith('dng:create.date'):
                        l = line.strip()
                       
                        yearmonth = l[17:21] + l[22:24]

                        found = True
                        move(args.dir, yearmonth, filename, i, n)
                        i = i + 1 
                        break
                break

        ##################
        # DEFAULT
        ##################
        if not found:
            # To default folder
            if not os.path.exists(undatedfolder):
                os.makedirs(undatedfolder)

            # Move
            ffrom = os.path.join(args.dir, filename)
            fto = os.path.join(undatedfolder, filename)
            shutil.move(ffrom, fto)

            print("%d of %d - %d%% completed: %s" % (i, n, i*100.0/n, filename))
            i = i+1
    break
