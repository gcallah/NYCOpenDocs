path=$1
if [ -z path ]; then
    path="."
fi
echo $path
# find $path -maxdepth 1 -o -regex ".*\.\(py\|css\|html\)"
# find $path -type f \( -name '*.py' -or -name '*.js' -or -name '*.yml' -or -name '*.sh' -or -name '*.html' -or -name '*.css' \)

EXTENSION_FILE=$2
ext=''
while IFS= read -r line
do
        ext+=" -e \.${line}$"
done < $EXTENSION_FILE
find $path | grep $ext