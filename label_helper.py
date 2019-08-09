import PySimpleGUI as sg
import os

nextBtn = sg.Button("Next")
prevBtn = sg.Button("Previous")


def selectFilesLayout():
    layout =[
                [sg.Input(key=("_FILES_")), sg.FilesBrowse()],
                [nextBtn]
    ]
    return layout


def inputFilenameLayout(displayImage):
    layout = [
                [displayImage],
                [sg.InputText(key="Answer", do_not_clear=False)],
                [prevBtn, nextBtn]
    ]
    return layout


browseWindow = sg.Window("Select Files", selectFilesLayout())
event, fileDict = browseWindow.Read()
if event != "Next" or len(fileDict["Browse"]) == 0:
    exit()
else:
    browseWindow.Close()

fileList = fileDict["_FILES_"].split(';')
fileAbsDir = '/'.join(fileList[0].split('/')[:-1])
fileList = [filename.split('/')[-1].split('.')[0] for filename in fileList]

displayImage = sg.Image(fileAbsDir + '/' + fileList[0] + ".png", key="imageContainer")
inputWindow = sg.Window("[{}/{}] Please Input - {}".format(1, len(fileList), fileList[0]),
                        inputFilenameLayout(displayImage))

index = 0
while True:
    newFilename = ""
    response = {}
    event, response = inputWindow.Read()

    newFilename = response["Answer"]

    if event == "Previous" and index > 0:
        if newFilename != "":
            os.rename(os.path.join(fileAbsDir, fileList[index] + ".png"), os.path.join(fileAbsDir, newFilename + ".png"))
            fileList[index] = newFilename
        index -= 1

    if event == "Next":
        if newFilename != "":
            os.rename(os.path.join(fileAbsDir, fileList[index] + ".png"), os.path.join(fileAbsDir, newFilename + ".png"))
            fileList[index] = newFilename
        index += 1
    if index >= len(fileList):
        break
    inputWindow.FindElement("imageContainer").Update(fileAbsDir + '/' + fileList[index] + ".png")
    inputWindow.TKroot.title("[{}/{}] Please input - {}".format(index, len(fileList), fileList[index]))

inputWindow.Close()

sg.Window("Finished!", [[sg.Text("Finished updating {} image labels.".format(len(fileList)))], [sg.OK()]]).Read()
