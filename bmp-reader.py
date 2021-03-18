import math
#reads the first two bytes of the image, which represents the BMP filetype
def checkBMPType(array):
    BMPType=array[0] + array[1]
    output = "BMP Type: "
    if (BMPType == "424d"):
        output += "Windows 3.1x, 95, NT, ... etc."
    else:
        if (BMPType == "4241"):
            output += "BMP Type: OS/2 struct bitmap array"
        elif (BMPType == "4349"):
            output += "BMP Type: OS/2 struct color icon"
        elif (BMPType == "4350"):
            output += "BMP Type: OS/2 const color pointer"
        elif (BMPType == "4943"):
            output += "BMP Type: OS/2 struct icon"
        elif (BMPType == "5054"):
            output += "BMP Type: OS/2 pointer"
        output += "\nWhere did you even get this image?!"
    return output

def BMPSize(array):
    output="Size of image: "
    size = "0x" + array[3]+array[2]
    output += str(int(size, 16) // 1024) + "KB (" + str(int(size, 16)) + " bytes)"
    return output
image = open("aimless.bmp", "rb")

def tableHeader(string, title):
    header = ""
    j = 0
    k = 0
    while(j <= math.ceil(len(string)/2) - math.ceil(len(title)/2)+1):
        header += "="
        j += 1
    header += title
    while(k <= math.ceil(len(string)/2) - math.ceil(len(title)/2)+1):
        header += "="
        k += 1
    return header

def offsetToPixelData(array):
    offsetToPixels = "0x"+array[13]+array[12]+array[11]+array[10]
    
image_data=image.read().hex()

image.close()

WORD = 2
DWORD = 4
QWORD = 8

imageDataArray = []
i = 0
while i < len(image_data):
    imageDataArray.append(image_data[i:i+2])
    i += 2

BMPTypeOutput = ("|" + checkBMPType(imageDataArray) + "\t|")
BMPSizeOutput = ("|" + BMPSize(imageDataArray) + "\t\t|")
print(tableHeader(BMPTypeOutput, "IMAGE DATA"))
print(BMPTypeOutput)
print(BMPSizeOutput)
