import os
import tempfile
import zipfile
import uuid
import shutil

class Kit:
    def __init__(self, name):
        self.name = name
        self.files = {}

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

    def extract(self, current, dest):
        with tempfile.TemporaryDirectory() as tmpdirname:
            for type in self.files:
                os.makedirs(tmpdirname + "/" + type)
                for file in self.files[type]:
                    print("Extracting: ", file, "(", type ,")")
                    kitzip = zipfile.ZipFile( current + "/" + file)
                    #layout : tmpDir / filename / stuff
                    kitzip.extractall(tmpdirname)
                    self.copyImages(tmpdirname, os.path.splitext(os.path.basename(file))[0], type)
            self.createManifest(tmpdirname)
            self.CopyKitFiles(tmpdirname, dest)

    def copyImages(self, tmpDir, folder, dest):
        exts = [".png", ".jpg"]
        print(" -> Copying Images from ", folder)
        #counter for renaming
        for i, (rootpath, subdirs, files) in enumerate(os.walk(os.path.join(tmpDir, folder))):
            for filename in files:
                if os.path.basename(filename).lower() == "folder":
                    # don't copy the folder image
                    continue
                if os.path.splitext(filename)[1].lower() in exts:
                    newName = os.path.join(tmpDir, dest, filename)
                    if not os.path.exists(newName):
                        shutil.move(os.path.join(rootpath, filename), newName)
                    else:
                        # Rename the file if conflict using the loop index
                        f = os.path.splitext(newName)
                        shutil.move(os.path.join(rootpath, filename), f[0]+"-"+str(i)+f[1])
        shutil.rmtree(os.path.join(tmpDir, folder))

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

        with open(tmpDir + '/package.manifestx', 'w') as f:
            for line in manifest:
                f.write(line + os.linesep)

    def CopyKitFiles(self, tmpDir, dest):
        shutil.copytree(tmpDir, os.path.join(dest, self.name))
