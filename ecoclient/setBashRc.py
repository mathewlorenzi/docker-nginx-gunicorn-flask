import os
import argparse

def updateBashRcWithEcovisionLibPath(ecovisionPath: str):
    if not os.path.isdir(ecovisionPath):
        print("[ERROR]ecovisionPath does not exist: ", ecovisionPath)
        exit(1)
    ecovisionLib = ecovisionPath+'/build/lib'
    bashRcString = 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:'+ecovisionLib
    if not os.path.isdir(ecovisionLib):
        print("[ERROR]updateBashRcWithEcovisionLibPath: this dir does not exist: ", ecovisionLib)
        exit(1)
    if 'HOME' not in os.environ:
        print("[ERROR]updateBashRcWithEcovisionLibPath: environ HOME not present")
        exit(1)
    bashrcPath = os.path.join(os.environ['HOME'], ".bashrc")
    print("[INFO]check bashrc is present: ", bashrcPath)
    if not os.path.isfile(bashrcPath):
        print("[WARNING]bashrc not present in home dir ", bashrcPath, "lets create it")
        with open(bashrcPath, "w") as fbashrc:
            fbashrc.write(bashRcString)
            fbashrc.write("\n")
        if not os.path.isfile(bashrcPath):
            print("[ERROR]bashrc failed to be created in home dir ", bashrcPath)
            exit(1)
    else:
        ecovisionPathFound = 0

        targetWords = bashRcString.split(' ')
        with open(bashrcPath, "r") as fbashrc:
            for line in fbashrc.readlines():
                # print(line)
                words = line.split(' ')
                # print(" ================= ")
                words2 = []
                for word in words:
                    words2.append(word.replace('\n',''))
                # print(words2)
                localFound = False
                if len(words2) == len(targetWords):
                    localFound = True
                    for index in range(len(words2)):
                        if words2[index] != targetWords[index]:
                            localFound = False
                # print(" +++++++++++++++++ ")
                # print(targetWords)            
                if localFound is True:
                    ecovisionPathFound += 1
                # print(" ----------------- ", localFound, ecovisionPathFound)
        if ecovisionPathFound == 0:
            print("[INFO]adding ecovision path lib into bashrc")
            with open(bashrcPath, "a") as fbashrc:
                fbashrc.write(bashRcString)
                fbashrc.write("\n")
        else:
            print("[INFO]ecovision path lib already present in bashrc")

        if ecovisionPathFound > 1:
            print("[WARNING]ecovision path lib was fou nd more than once: ", ecovisionPathFound)

    # bash = subprocess.run('bash')
    # bash.execute('source '+os.environ['HOME']+'/.bashrc')
    # subprocess.call(['source', os.environ['HOME']+'/.bashrc'])
          
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='ecovision threads manager')
    parser.add_argument('--ecovisionPath', metavar='port', required=True,
                        help='the ecovisionPath') # "/home/ecorvee/Projects/EcoVision/ecplatform2"
    args = parser.parse_args()

    print("[INFO]updateBashRcWithEcovisionLibPath")
    updateBashRcWithEcovisionLibPath(args.ecovisionPath)
    print("[INFO]exit, export /user/.bashrc and restart manager")
    exit(0)

