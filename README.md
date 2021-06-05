# Algebraic-datatype-TaintTracker
Given a list of sources, this TaintTracker tool produces algebric leak signatures of the sources and also categorize the leak as third party or own code leak.

### Overview
   CFG-Generator.jar (extension of Amandroid) will generate CFG (Control Flow Graph) given an apk 
   App_Wise_Signature.py will create the leak signature given the CFG file as text input

  #### Prerequisites
   Java installed and should be on path.

   Python installed (python 3) and should be on path
   
   bash installed (if you are using windows OS)

### Run
  First git clone the project.
  Then simply run the run.sh script with the specific apk file path or apk files directory (to run as a batch) as the argument. This google drive link contains some sample apps (Table 9 apps of the paper).
https://drive.google.com/drive/folders/1KD0ORh2ZnGQbSMAXrQEjgDpKL2raVIEr?usp=sharing
  Command:
  
    ./run.sh <apk_file> or <apk_files directory> 
    Example:
    ./run.sh com.dunkinbrands.otgo.apk

    (for Windows OS)
    bash run.sh <apk_file> or <apk_files directory>
    
  To run CFG file generation and Signature creation seperately follow the steps below: 
  #### CFG file Generation
    Command:
      java -jar CFG-Generator.jar g <file_apk/dir> <output_dir> > <output_file>
      
  #### Leak Signature Generation
    Command:
      python App_Wise_Signature.py <CFG_file>
      
### Input      
   The source APIs to be tracked can be edited and listed in sources.txt file as the following format
   <source_API> <space> <Name_for_the_signature>
    
### Output
   The ouput is a text file generated in the same directory as the run.sh script as <apk_file>_signature.txt. 
   
   Each line in the ouput file represents a different leak signature for that app.
   #### An example output:
   ```
   (h(Mac) ^ h(AndroidID) ) + IMEI  + GUID (Third Party Leak)
   ```
   It means either raw IMEI or hashed Mac address is combined (AND) with hashed AndroidID or random GUID is being leaked as deviceID and it's third party leak. SignatureResults folder has all the ouput signatures gennerated from running the tool on top Google Play apps.
   
For more details please read the paper.
      
