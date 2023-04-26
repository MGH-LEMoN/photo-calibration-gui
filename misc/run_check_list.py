import glob
import os

OKGREEN = "\033[92m"
FAIL = "\033[91m"
ENDC = "\033[0m"


def dir_contents(dir_name):
    return sorted(
        [
            file
            for file in glob.glob(os.path.join(dir_name, "*"))
            if os.path.isfile(file)
        ]
    )


def check_extension(file_list):
    return set(os.path.splitext(file)[-1] for file in file_list if os.path.isfile(file))


def check_if_additional_folders(dir_name):
    return len(glob.glob(os.path.join(dir_name + "*"))) > 1


def check_file_suffix(src_dir, dst_dir, suffix=None):
    flag = True

    try:
        dst_ext = list(check_extension(dir_contents(dst_dir)))[0]
    except:
        return False

    for file in dir_contents(src_dir):
        dst_name = os.path.splitext(os.path.basename(file))[0] + "_" + suffix + dst_ext

        if not os.path.isfile(os.path.join(dst_dir, dst_name)):
            flag = False

    return flag


if __name__ == "__main__":
    # while True:
    #     dir_name = input("Enter Name of the Input Directory: ")
    #     print(dir_name.strip())
    #     if not os.path.isdir(dir_name):
    #         print("Directory Does Not Exist")
    #         continue
    #     else:
    #         break

    dir_name = "/cluster/vive/MGH_photo_recon/"
    subjects = sorted(glob.glob(os.path.join(dir_name, "*")))
    for subject in subjects:
        if not os.path.isdir(subject):
            print(f"Skipping: {os.path.basename(subject)}")
            continue
        print(os.path.basename(subject))

        # Check Folders
        photo_dir = os.path.join(subject, "photos")
        deformed_dir = os.path.join(subject, "deformed")
        masked_dir = os.path.join(subject, "masked")
        cc_dir = os.path.join(subject, "connected_components")

        if os.path.exists(photo_dir):
            print("\tphotos..." + OKGREEN + "\u2713" + ENDC)

            photos = dir_contents(photo_dir)
            print("\t\tfile extension...", check_extension(photos))

            if check_if_additional_folders(photo_dir):
                print("\t\tadditional folders..." + FAIL + "\u274c" + ENDC)

        else:
            print("\tphotos..." + FAIL + "\u274c" + ENDC)

        # deformed folder
        if os.path.exists(deformed_dir):
            print("\tdeformed...", OKGREEN + "\u2713" + ENDC)

            corrected_photos = dir_contents(deformed_dir)
            print("\t\tfile extension...", check_extension(corrected_photos))

            if check_file_suffix(photo_dir, deformed_dir, suffix="deformed"):
                print("\t\tFiles Match...", OKGREEN + "\u2713" + ENDC)
            else:
                print("\t\tFiles Match..." + FAIL + "\u274c" + ENDC)

            if check_if_additional_folders(deformed_dir):
                print("\t\tadditional folders..." + FAIL + "\u274c" + ENDC)

        else:
            print("\tdeformed...", FAIL + "\u274c" + ENDC)

        # masked folder
        if os.path.exists(masked_dir):
            print("\tmasked...", OKGREEN + "\u2713" + ENDC)

            masked_photos = dir_contents(masked_dir)
            print("\t\tfile extension...", check_extension(masked_photos))

            if check_file_suffix(deformed_dir, masked_dir, suffix="masked"):
                print("\t\tFiles Match...", OKGREEN + "\u2713" + ENDC)
            else:
                print("\t\tFiles Match..." + FAIL + "\u274c" + ENDC)

            if check_if_additional_folders(masked_dir):
                print("\t\tadditional folders..." + FAIL + "\u274c" + ENDC)

        else:
            print("\tmasked...", FAIL + "\u274c" + ENDC)

        # connected components folder
        if os.path.exists(cc_dir):
            print("\tcc...", OKGREEN + "\u2713" + ENDC)

            cc_photos = dir_contents(cc_dir)
            print("\t\tfile extension...", check_extension(cc_photos))

            if check_file_suffix(deformed_dir, cc_dir, suffix="mask"):
                print("\t\tFiles Match...", OKGREEN + "\u2713" + ENDC)
            else:
                print("\t\tFiles Match..." + FAIL + "\u274c" + ENDC)

            if check_if_additional_folders(cc_dir):
                print("\t\tadditional folders..." + FAIL + "\u274c" + ENDC)

        else:
            print("\tcc...", FAIL + "\u274c" + ENDC)
