import os
import tempfile
import zipfile
import uuid
import shutil

class Kit:
    def __init__(self, name):
        self.name = name
        self.files = {}
        self.hasError = False
        self.error = None

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

    def extract(self, fromDir, dest):
        with tempfile.TemporaryDirectory() as tmpDir:
            for type in self.files:
                tempPath = os.path.join(tmpDir, type)
                os.makedirs(tempPath)
                print("Extracting to:", tempPath)
                for file in self.files[type]:
                    print("Extracting: ", file, "(", type ,")", "{file:",os.path.join(fromDir, file),"}")
                    kitzip = zipfile.ZipFile( os.path.join(fromDir, file))
                    #layout: tmpDir / filename / stuff
                    try:
                        if kitzip.testzip() is None:
                            kitzip.extractall(tmpDir)
                            kitzip.close()
                        else:
                            self.hasError = True
                            self.error = "Zip File Bad"
                            print()
                            print("Error Extracting: ", self.name)
                            print("Zip File has Error!")
                            print()
                            input("Please Press the 'Enter' key to continue...")
                    except Exception as e:
                        self.hasError = True
                        self.error = e
                        print()
                        print(e)
                        print()
                        print("Error Extracting: ", self.name)
                        input("Please Press the 'Enter' key to continue...")
                    self.copyImages(tmpDir, tempPath)
            self.createManifest(tmpDir)
            self.CopyKitFiles(tmpDir, dest)

    def copyImages(self, fromDir, toDir):
        exts = [".png", ".jpg"]
        print(" -> Copying Images from ", fromDir)
        skipPaths = [fromDir];
        for type in self.files:
            skipPaths.append(os.path.join(fromDir, type))
        #counter for renaming
        for i, (rootpath, subdirs, files) in enumerate(os.walk(fromDir)):
            if rootpath in skipPaths:
                continue
            for filename in files:
                if os.path.basename(filename).lower() == "folder":
                    # don't copy the folder image
                    continue
                if os.path.splitext(filename)[1].lower() in exts:
                    newName = os.path.join(toDir, filename)
                    if not os.path.exists(newName):
                        shutil.move(os.path.join(rootpath, filename), newName)
                    else:
                        # Rename the file if conflict using the loop index
                        f = os.path.splitext(newName)
                        shutil.move(os.path.join(rootpath, filename), f[0]+"-"+str(i)+f[1])

    def createManifest(self, tmpDir):
        manifest = []
        manifest.append('<Manifest vendorid="0" vendorpackageid="0" maintaincopyright="True" dpi="300">')
        manifest.append('<Groups />')
        manifest.append('<Entries>')
        for type in self.files:
            imageType = type if type is "embellishment" or type is "paper" else "embellishment"
            for image in os.listdir(os.path.join(tmpDir, type)):
                manifest.append('<Image ID="'+str(uuid.uuid4())+'" Name="'+os.path.join(type, image)+'" Group="'+imageType+'" />')
        manifest.append('</Entries>')
        manifest.append('</Manifest>')

        with open(os.path.join(tmpDir,'package.manifestx'), 'w') as f:
            for line in manifest:
                f.write(line + os.linesep)

    def CopyKitFiles(self, tmpDir, dest):
        basePath = os.path.join(dest, self.name)
        os.mkdir(basePath)
        for type in self.files:
            shutil.copytree(os.path.join(tmpDir, type), os.path.join(basePath, type))
        shutil.copy(os.path.join(tmpDir, "package.manifestx"), basePath)