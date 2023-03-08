# Import libraries
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt

# Define amplitude thresholds and duration criteria
amp_high = 0 # Change this value according to your needs
amp_low = 0.05 # Change this value according to your needs
dur_high = 1.5 # Change this value according to your needs
dur_low = 0.1 # Change this value according to your needs

# Read audio file
fs, data = wavfile.read("result.wav") # Change this file name according to your needs

# Normalize audio data
data = data / np.max(np.abs(data))

# Plot audio waveform
plt.plot(data)
plt.xlabel("Time (samples)")
plt.ylabel("Amplitude")
plt.show()

# Find start and end points of audio segments based on amplitude thresholds and duration criteria
start_points = []
end_points = []
above_high_count = 0 # Counter to indicate how long the amplitude is above the high threshold 
below_low_count = 0 # Counter to indicate how long the amplitude is below the low threshold

i = 0
j = 0
while(i < len(data)) :
    if data[i] >= amp_high: # Amplitude is above the high threshold 
        above_high_count += 1 # Increment counter 
        below_low_count = 0 # Reset counter 
        start_point = max(0, i) # Go back by dur_low seconds and set as start point 
        start_points.append(start_point)
        
        while(j < len(data)) :
            if data[j] <= amp_low: # Amplitude is below the low threshold 
                below_low_count += 1 # Increment counter 
                above_high_count = 0 # Reset counter 
                if below_low_count == int(dur_high * fs): # Amplitude has been below the low threshold for dur_high seconds 
                    end_point = min(len(data) - 1, j) # Set current index as end point 
                    end_points.append(end_point)
                    j = end_point
                    break
                j = j + 1
            i = j

print(start_points)
print(end_points)

# Check if the number of start and end points match 
if len(start_points) != len(end_points):
    print("Error: Number of start and end points do not match!")
else:
    print(f"Found {len(start_points)} audio segments.")



# Extract audio segments and save them as separate files 
for i in range(len(start_points)):
    segment_data = data[start_points[i]:end_points[i]] # Slice the data array using start and end points 
    segment_file_name = f"segment_{i}.wav" # Create a file name for each segment 
    wavfile.write(segment_file_name, fs, segment_data) # Write segment data as a wav file 
    print(f"Saved {segment_file_name}.")