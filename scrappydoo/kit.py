import os
import tempfile
import zipfile
import uuid
import shutil
from misc import Pause

class Kit:
    def __init__(self, name, dir ):
        self.name = name
        self.files = {}
        self.hasError = False
        self.error = None
        self.dir = dir
        self.outputDir = os.path.join(dir, name)
        self.imageTypeMap = {}
        if not os.path.exists(self.outputDir):
            os.makedirs(self.outputDir)

    def addFile(self, type, filename):
        if type not in self.files:
            self.files[type] = []
        self.files[type].append(filename)

    def __str__(self):
        kstr = self.name +  "(" + str(len(self.files)) + ")\n"
        for type in self.files:
            for f in self.files[type]:
                kstr += type + ": " + f + "\n"
        return kstr

    def extract(self):
        """ Extracts each zip file and copies images to the output dir"""
        with tempfile.TemporaryDirectory() as tmpDir:
            print()
            print("Processing ", self.name, "    (", tmpDir, ")")
            print()
            for type in self.files:
                for file in self.files[type]:
                    path = os.path.join(self.dir, file)
                    print()
                    print("Extracting: ", file, "(", type ,")")
                    print(" -> File:", path)
                    try:
                        kitzip = zipfile.ZipFile(path)
                        if kitzip.testzip() is None:
                            kitzip.extractall(tmpDir)
                            kitzip.close()
                            self.copyImages(tmpDir, type)
                        else:
                            self.hasError = True
                            self.error = "Zip File Bad"
                            print()
                            print("Error Extracting: ", self.name)
                            print("Zip File has Error!")
                            print()
                            Pause()
                    except Exception as e:
                        self.hasError = True
                        self.error = e
                        print()
                        print(e)
                        print()
                        print("Error Extracting: ", self.name)
                        Pause()
        self.createManifest()

    def copyImages(self, tmpDir, type):
        exts = [".png", ".jpg"]
        print(" -> Copying Images ...")
        #counter for renaming
        for i, (rootpath, subdirs, files) in enumerate(os.walk(tmpDir)):
            if rootpath == tmpDir:
                continue
            for filename in files:
                # don't copy the folder image
                if os.path.basename(filename).lower() == "folder":
                    continue
                # only copy the allowed file types
                if os.path.splitext(filename)[1].lower() in exts:
                    newName = os.path.join(self.outputDir, filename)
                    if os.path.exists(newName):
                        # Rename the file if conflict using the loop index
                        f = os.path.splitext(newName)
                        newName = f[0]+"-"+str(i)+f[1]
                    shutil.move(os.path.join(rootpath, filename), newName)
                    self.imageTypeMap[newName] = type
        print(" -> Done! Copied ", len(self.imageTypeMap), "Images")

    def createManifest(self):
        print("Creating Manifest ...");
        with open(os.path.join(self.outputDir,'package.manifestx'), 'w') as f:
            f.write('<Manifest vendorid="0" vendorpackageid="0" maintaincopyright="True" dpi="300">\n')
            f.write('<Groups />\n')
            f.write('<Entries>\n')
            for image in os.listdir(self.outputDir):
                imageType = self.imageTypeMap.get(os.path.join(self.outputDir, image), "embellishment")
                if imageType != "embellishment" and imageType != "paper":
                        imageType = "embellishment"
                f.write('<Image ID="'+str(uuid.uuid4())+'" Name="'+image+'" Group="'+imageType+'" />\n')
            f.write('</Entries>\n')
            f.write('</Manifest>\n')
        print("Done! Saved ", os.path.join(self.outputDir,'package.manifestx'))
