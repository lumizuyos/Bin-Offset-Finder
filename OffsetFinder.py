#Importing Stuff
import binascii, os, sys, subprocess

#Call handling
if len(sys.argv) <= 1:
 print('No arguments provided. Use: python offsetfinder.py --help')
 exit(1)
argueKid1 = str(sys.argv[1])
argueKid2 = str(sys.argv[2])
argueKid3 = str(sys.argv[3])
argueKid4 = str(sys.argv[4])
if argueKid1 == "--help":
 print('\nUsage: python offsetfinder.py [Function to MOD] [Nick Name] [Original Bytes] [Modified Bytes] \nMade By LCP')
 exit(0)
 
#Initialization
currentDir = str(os.getcwd())
toBeMod =   argueKid1
nickName =  argueKid2
origBytes = argueKid3
modBytes =  argueKid4

#Find line with matching function
for line in open('AllFuncs.txt'):
 if line.startswith(toBeMod) and '0000000C' not in line :
  toBeMod = line

#Find seek value of current function and size from line
toBeMod=toBeMod.split()
StartSeek=int(toBeMod[2],16)
SeekSize=int(toBeMod[3],16)

#Split lib*.so to current function toMod.so
os.system(currentDir+r'\bin\dd if=lib.so bs='+str(StartSeek)+r' skip=1 | '+currentDir+r'\bin\dd bs='+str(SeekSize)+r' count=1 > '+currentDir+r'\temp\toMod.so')

#Generate Hex Dump of function to mod
with open(currentDir + r'\temp\toMod.so', 'rb') as f:
    # Slurp the whole file and efficiently convert it to hex all at once
    hexDump = binascii.hexlify(f.read())
hexDump=str(hexDump)

#Find pattern in Dump and (ModOffset-2) gives position of pattern (ModOffset-2) and /2 gives byte position
ModOffset=hexDump.find(origBytes)
ModOffset=ModOffset-2
ModOffset=ModOffset/2

#Actual offset of ModOffset in main lib*.so
ModOffset=ModOffset+StartSeek

#Beautifying Values
ModOffsetHex=str(hex(int(ModOffset)))
ModOffset=str(int(ModOffset))

#Printing offset
print ('Decimal=' + ModOffset)
print ('Hex=' + ModOffsetHex)

#Saving Patch
Patch='\n'+str(nickName)+'\nOffset:'+str(ModOffsetHex.upper())+'\nOriginal:'+str(origBytes.upper())+'\nPatched:'+str(modBytes.upper())+'\n'
with open("Patches.txt", "a") as myfile:
  myfile.write(Patch)