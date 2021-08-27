import cv2
import numpy as np

def decode_fourcc(cc):
    return "".join([chr((int(cc) >> 8 * i) & 0xFF) for i in range(4)])

# Create a VideoCapture object
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))


# Check if camera opened successfully
if (cap.isOpened() == False): 
  print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

print(frame_width)
print(frame_height)

codec = cap.get(cv2.CAP_PROP_FOURCC)
print(decode_fourcc(codec))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
# out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_he$

while(True):
  ret, frame = cap.read()

  if ret == True:

    # Write the frame into the file 'output.avi'
    # out.write(frame)

    # Display the resulting frame
    cv2.imshow('frame',frame)

    # Press Q on keyboard to stop recording
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break

  # Break the loop
  else:
    break

# When everything done, release the video capture and video write objects
cap.release()
# out.release()

# Closes all the frames
cv2.destroyAllWindows()
