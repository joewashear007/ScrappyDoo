import os
import tempfile
import zipfile
import uuid
import shutil

class Kit:
    def __init__(self, name, dir ):
        self.name = name
        self.files = {}
        self.hasError = False
        self.error = None
        self.dir = dir
        self.imageTypeMap = {}
        p = os.path.join(dir, name)
        if not os.path.exists(p):
            os.makedirs(p)

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
        with tempfile.TemporaryDirectory() as tmpDir:
            for type in self.files:
                print("Extracting to:", tmpDir)
                for file in self.files[type]:
                    print("Extracting: ", file, "(", type ,")", "{file:",os.path.join(self.dir, file),"}")
                    kitzip = zipfile.ZipFile( os.path.join(self.dir, file))
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
                    self.copyImages(tmpDir, type)
            self.createManifest(tmpDir)

    def copyImages(self, fromDir, type):
        exts = [".png", ".jpg"]
        print(" -> Copying Images from ", fromDir)
        skipPaths = [fromDir];
        #counter for renaming
        for i, (rootpath, subdirs, files) in enumerate(os.walk(fromDir)):
            if rootpath == fromDir:
                continue
            for filename in files:
                if os.path.basename(filename).lower() == "folder":
                    # don't copy the folder image
                    continue
                if os.path.splitext(filename)[1].lower() in exts:
                    newName = os.path.join(self.dir, self.name, filename)
                    if os.path.exists(newName):
                        # Rename the file if conflict using the loop index
                        f = os.path.splitext(newName)
                        newName = f[0]+"-"+str(i)+f[1]
                shutil.move(os.path.join(rootpath, filename), newName)
                self.imageTypeMap[newName] = type
        print("Done!")

    def createManifest(self, tmpDir):
        manifest = []
        manifest.append('<Manifest vendorid="0" vendorpackageid="0" maintaincopyright="True" dpi="300">')
        manifest.append('<Groups />')
        manifest.append('<Entries>')
        for image in os.listdir(tmpDir):
            imageType = self.imageTypeMap[image]
            manifest.append('<Image ID="'+str(uuid.uuid4())+'" Name="'+image+'" Group="'+imageType+'" />')
        manifest.append('</Entries>')
        manifest.append('</Manifest>')

        with open(os.path.join(self.dir, self.name,'package.manifestx'), 'w') as f:
            for line in manifest:
                f.write(line + os.linesep)