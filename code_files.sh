path=$1
if [ -z path ]; then
    path="."
fi
echo $path

EXTENSION_FILE=$2
ext=''
while IFS= read -r line
do
        ext+=" -e \.${line}$"
done < $EXTENSION_FILE
find $path | grep $ext