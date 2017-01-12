from optparse import OptionParser
import Image

# Encodes a message by replacing the last bits of each RGB value in an image
def encode(msg, fname):
    inFile = Image.open(fname) 
    px     = list(inFile.getdata()) # list of 3-tuples w/ decimal RGB vals
    zeroPx = list()                 # image w/ all RGB values divisible by 2
    newPx  = list()                 # new image to be written
    binArr = msgToBinary(msg)       # array of the message as 1's and 0's

    # Replace all values with values which mod to 0 with 2
    for i in px:
        zeroPx.append(tuple(map(lambda x: x - 1 if x & 1 else x, i)))

    # Add 1 to every index that corresponds with a 1 in the binary array
    count = 0
    for i,j,k in zeroPx:
        if count < len(binArr):
            itmp = i + 1 if binArr[count] == 0 else i
            count += 1
            if count < len(binArr):
                jtmp = j + 1 if binArr[count] == 0 else j
                count += 1
            else:
                jtmp = j
            if count < len(binArr):
                ktmp = k + 1 if binArr[count] == 0 else k
                count += 1
            else:
                ktmp = k
            newPx.append((itmp,jtmp,ktmp))
        else:
            newPx.append((i,j,k))

    outFile = Image.new("RGB", (inFile.size))
    outFile.putdata(newPx)
    outFile.save("out.png") 

    inFile.close()
    outFile.close()

# Recovers the message from a steg image
def decode(fname):
    inFile = Image.open(fname)
    px     = list(inFile.getdata()) # list of 3-tuples w/ decimal binary values
    binArr = list()                 # list to hold the msg as an array of 1's/0's

    # populate binArr
    for i,j,k in px:
        if i % 2 == 1:
            binArr.append(0)
        else:
            binArr.append(1)
        if j % 2 == 1:
            binArr.append(0)
        else:
            binArr.append(1)
        if k % 2 == 1:
            binArr.append(0)
        else:
            binArr.append(1)

    msg = binaryToMsg(binArr)
    msgEnd = len(msg)

    # find a good place to truncate the message
    count = 0
    for i in range(len(msg)):
        if ord(msg[i]) == 255:
            count += 1
        else:
            count = 0
        if count == 2:
            msgEnd = i - 1 

    msg = msg[:msgEnd]

    print msg[:140]
    
    inFile.close()

# Converts a string message to an array of 1's/0's
def msgToBinary(msg):
    arr = list()
    for letter in msg:
        tmparr = toByte(ord(letter))
        for n in tmparr:
            arr.append(n)

    return arr

# Converts a decimal number into an array of 8 1's/0's
# Helper function for msgToBinary()
def toByte(n):
    arr = list()

    for i in range(8):
        if n != 0:
            arr.append(n % 2)
            n = n >> 1
        else:
            arr.append(0)
    arr.reverse()

    return arr

# Converts an array of 1's/0's to a string
def binaryToMsg(arr):
    tmpstr = ""
    for i in range(0, len(arr), 8):
        tmpstr += fromByte(arr[i : i + 8])

    return tmpstr

# Converts an array of 1's/0's to a char
# Helper function for binaryToMsg
def fromByte(arr):
    tmpstr = ""
    for n in arr:
        tmpstr += str(n)
    
    intVal = int(tmpstr, 2)
    return chr(intVal)

# Handles arguments from command line
def handleOptions():

    # Option Definitions
    parser = OptionParser()

    parser.add_option("-e", action="store_true", dest="encode",
                    help="encode FILE to out.png if no filename specified")
    parser.add_option("-m", dest="message",
                    help="specify message to encode")
    parser.add_option("-d", action="store_true", dest="decode",
                    help="decode FILE from in.png if no filename specified")
    parser.add_option("-f", dest="filename",
                    help="change filename for encoding/decoding")

    (options, args) = parser.parse_args()

    # Error Handling
    if options.encode and options.decode:
        parser.error("encode and decode are mutually exclusive")
    if options.decode and options.message:
        parser.error("cannot specify message to decode")

    # Encode
    if options.encode:
        if options.message:
            msg = options.message
        else:
            msg = "Test message for steg program"

        if options.filename:
            fname = options.filename
        else:
            fname = "in.png"
        encode(msg, fname)

    # Decode
    if options.decode:
        if options.filename:
            fname = options.filename
        else:
            fname = "in.png"
        decode(fname)

# Start program
handleOptions()
