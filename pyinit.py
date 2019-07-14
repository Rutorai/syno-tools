#!/usr/bin/env python3

import requests, sys, json, os, tarfile, zipfile, shutil

# The DSM product name to download packages for
DSM_MODEL = "DS3615xs"

# The URL to use to download packages
DOWNLOAD_URL = "https://www.synology.com/api/support/findDownloadInfo?lang=fr-fr&product="+DSM_MODEL

if __name__ == "__main__":
    # Download list of packages (it's a JSON file)
    print("Downloading " + DOWNLOAD_URL)
    response = requests.get(DOWNLOAD_URL)

    # Process only if the download of the file is successful
    if response.ok:
        # Check the content type of the downloaded file
        contentType = response.headers.get('content-type')
        if contentType != 'application/json':
            print("Invalid type")
            #Exit in error if the file is not a JSON file
            sys.exit(-1)

        # Retrieve list of packages
        content = json.loads(response.content)
        packages = content["info"]["packages"]

        # Clean package folder
        if os.path.isdir("./packages"):
            shutil.rmtree("./packages")

        # Create package folder
        os.mkdir("./packages")

        # Loop over packages
        for package in packages:
            # Loop over files for packages
            for file in package["files"]:
                # Check if the package has a URL to download it, if not there's nothing to do
                if "url" in file:
                    # Download package
                    print("Downloading " + file["url"])
                    packageFile = requests.get(file["url"])
                    fileName = "./packages/" + package["package"] + "-" + package["version"] + ".spk"
                    open(fileName, "wb").write(packageFile.content)

                    # Create package folder to extract files
                    if not os.path.isdir("./packages/" + package["package"]):
                        os.mkdir("./packages/" + package["package"])

                    # Extract files of package
                    print("Extracting " + fileName)
                    tar_ref = tarfile.open(fileName, "r")
                    tar_ref.extractall("./packages/" + package["package"] + "/")
                    tar_ref.close()

                    # Create folder where files from package.tgz archive will be extracted to
                    os.mkdir("./packages/" + package["package"] + "/package")

                    fileName = "./packages/" + package["package"] + "/package.tgz"
                    print("Extracting " + fileName)

                    # Extract files from package.tgz
                    tar_ref = tarfile.open(fileName, "r")
                    tar_ref.extractall("./packages/" + package["package"] + "/package/")
                    tar_ref.close()
                else:
                    print("Missing package: " + str(package))
