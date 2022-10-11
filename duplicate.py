#!/usr/bin/python

import sys, getopt, os
import shutil
import filecmp
import time
from datetime import datetime

def main(arguments):
    # variable initialization to be used to later
    source_directory = ''
    log_file_path = ''

    # to keep track on any changes inbetween the directories
    changes = False

    # checking for any errors faced during the getting of each argv
    try:
        opts, args = getopt.getopt(arguments,"hi:t:l:", ["folder_path=","sync_int=","log_path="])
    except getopt.GetoptError:
        print ('duplicate.py -i <folder path> -t <synchronization interval(seconds)> -l <log file path>')
        sys.exit(2)
    
    # iterating over the input variables
    for opt, arg in opts:

        # created a help fucntion to define the input format
        if opt == '-h':
            print('duplicate.py -i <folder path> -t <synchronization interval(seconds)> -l <log file path>')
            sys.exit()

        # set varaibles from each command line input
        # as mentioned here we set each variable individually
        elif opt in ("-i", "--folder_path"):
            source_directory = arg
        elif opt in ("-l", "--log_path"):
            log_file_path = arg

    # perlim check to see if source directory exist and can be read
    if os.path.exists(source_directory):

        # defining variables to keep track of the base directories i.e. root for folders
        # this is not the computer root folder just labelled so
        root_source_dir = source_directory
        dir, final_dir = os.path.split(source_directory)
        root_dest_dir = os.path.join(dir, "replica") # root_dest_dir = dir + '/replica'
    else:
        print("The Source Directory doesnot exist or need permission to be able to br read")
        exit(0)

    # opening log file to have all lines of logs be written in sequence
    # using timestamp the updates so as to see any changes
    # hence now file acts as a log file in no changes performed we dont write anything
    with open(log_file_path, "a") as logfile: # open file with write w => over write what ever is in the file to new writes

        # go through each directory independeptly and create them in new folder if required
        for dirpath, dirnames, filenames in os.walk(source_directory):

            # replacing the source path to the new replica path
            dest_dir = dirpath.replace(root_source_dir, root_dest_dir)

            # creating the directory if not exist
            if not os.path.exists(dest_dir):
                os.mkdir(dest_dir)
                logfile.write("Creating " + dest_dir + " directory \n")
                print("Creating " + dest_dir + " directory")
                changes = True

            # looping over each file in directory to determine the source and the destiantion
            for file in filenames:
                src_file = os.path.join(dirpath, file)
                dst_file = os.path.join(dest_dir, file)

                # determining the status of files and accordingly performing the operation
                # filecmp.cmp(src_file, dst_file) == True
                if os.path.exists(src_file) == True and os.path.exists(dst_file) == False:
                    shutil.copy(src_file, dest_dir)
                    logfile.write("Copying " + dest_dir + "/" + file + "\n")
                    print("Copying " + dest_dir + "/" + file + "")
                    changes = True
                
                # check even if content of file change the file must be copied then as there is an edit
                # used supporting library filecmp as it makes life easier => can be implemented
                elif os.path.exists(src_file) == True and os.path.exists(dst_file) == True and filecmp.cmp(src_file, dst_file) == False:
                    shutil.copy(src_file, dest_dir)
                    logfile.write("Modifying " + dest_dir + "/" + file + "\n")
                    print("Modifying " + dest_dir + "/" + file + "")
                    changes = True

        # checking if we remove any file from source that must be removed from replica
        # the removal process is carried out reversed i.e. we go through the replica to remove
        for ddirpath, ddirnames, dfilenames in os.walk(root_dest_dir):
            ddest_dir = ddirpath.replace(root_dest_dir, root_source_dir)

            # remove files that exist in replica folder that dont exist in source anymore
            for dfile in dfilenames:
                dsrc_file = os.path.join(ddirpath, dfile)
                ddst_file = os.path.join(ddest_dir, dfile)
                if os.path.exists(dsrc_file) == True and os.path.exists(ddst_file) == False:
                    os.remove(dsrc_file)
                    logfile.write("Removing " + ddst_file + "\n")
                    print("Removing " + ddest_dir + "/" + dfile + "")
                    changes = True
            
            # if directory removed then remove it from the replica folder
            if not os.path.exists(ddest_dir) and len(os.listdir(ddirpath)) == 0:
                os.rmdir(ddirpath)
                logfile.write("Removing " + ddirpath + " directory \n")
                print("Removing " + ddirpath + " directory")
                changes = True
            # ordering this was is important as the directory must be empty to be removed 
            # hence the deletion of the directory comes after the deletion of all files inside

        # if some change has occured log it else no need for printing or logging
        if changes == True:

            # datetime imported to have exact logging 
            logfile.write('\nABOVE UPDATE AT TIME %s\n' %datetime.now() + "\n\n")
            print('\nABOVE UPDATE AT TIME %s\n' %datetime.now())


# obtaining the path and the data from the command line
if __name__ == "__main__":
    # keep trying to run code until an Interrupted
    try:
        while True:
            # the code it runs
            main(sys.argv[1:])
            time.sleep(int(sys.argv[4]))
    # to end the running of the program press CTRL + C
    except KeyboardInterrupt:
        print('\n INTERRUPTED! \n')