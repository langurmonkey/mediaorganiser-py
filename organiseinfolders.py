from os import walk
import argparse, os, shutil, re

parser = argparse.ArgumentParser(description='Process some integers.')
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument("-d", "--dir",  help="The directory", required=True)
args = parser.parse_args()

if not os.path.isdir(args.dir):
    print("%s is not a directory" % args.dir)
    exit()

# CONSTANTS
prefixes = ['VID_', 'VID-', 'IMG_', 'IMG-', 'PHOTO_', 'PANO_']
regexps = ['(\d{4})-(\d{2})-(\d{02}).*']
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

                datefolder = os.path.join(args.dir, yearmonth)

                if not os.path.exists(datefolder):
                    os.makedirs(datefolder)

                # Move
                shutil.move(os.path.join(args.dir, filename), os.path.join(datefolder, filename))

                print("%d of %d - %d%% completed: %s" % (i, n, i*100.0/n, filename))
                i = i+1
                break

        ##################
        # REGEXP
        ##################
        for regexp in regexps:
            pattern = re.compile(regexp)
            if pattern.match(filename):
                yearmonth = filename[:4] + filename[5:7]

                found = True

                datefolder = os.path.join(args.dir, yearmonth)

                if not os.path.exists(datefolder):
                    os.makedirs(datefolder)

                # Move
                shutil.move(os.path.join(args.dir, filename), os.path.join(datefolder, filename))

                print("%d of %d - %d%% completed: %s" % (i, n, i*100.0/n, filename))
                i = i+1
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
