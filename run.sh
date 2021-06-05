
if [[ ! -f "$1" ]] && [[ ! -d "$1" ]]
then
  echo "file or Path does not exist"
fi

if [[ ! -f "$1" ]]
then
    APKsPath="$1/*.apk"
    for apk in $APKsPath; do
        ((count++))
        echo "App no:"
        echo $count
        #if [ $count -lt 367 ]
        #then
            #continue
        #fi
        filename=$(basename -- "$apk")
        filename="${filename%.*}"
        echo "Processing...."
        echo $filename
        echo "Generating CFG..."
    #    if [[ -f "/Users/sujon335/Desktop/AmanDroid/FinanceApps/$filename.txt" ]]
    #    then
    #        echo "result there"
    #        continue
    #    fi
        java -jar CFG-Generator.jar g $apk CFGFiles > CFGFiles/$filename.txt
        echo "Finding Leak Signatures...."
        python App_Wise_Signature.py CFGFiles/$filename.txt
    done
else
    apk=$1
    filename=$(basename -- "$apk")
    filename="${filename%.*}"
    echo "Processing...."
    echo $filename
    echo "Generating CFG..."
    java -jar CFG-Generator.jar g $apk CFGFiles > CFGFiles/$filename.txt
    echo "Finding Leak Signatures...."
    python App_Wise_Signature.py CFGFiles/$filename.txt
fi

