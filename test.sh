#!/bin/bash
# chmod +x test.sh makes it so you don't have to type bash 
# everytime in order to run the script
echo "testing http://www.example.com"
python3 egjensenMyCurl.py http://www.example.com
curl http://www.example.com --output download.html
diff HTTPoutput.html download.html

echo "testing http://pudim.com.br/"
python3 egjensenMyCurl.py http://pudim.com.br/
curl http://pudim.com.br/ --output download.html
diff HTTPoutput.html download.html

echo "testing http://www.google.com"
python3 egjensenMyCurl.py http://www.google.com

echo "testing http://www.example.com/anyname.html"
python3 egjensenMyCurl.py http://www.example.com/anyname.html

echo "testing http://neverssl.com"
python3 egjensenMyCurl.py http://neverssl.com
curl http://neverssl.com --output download.html

echo "testing http://www.example.com:443"
python3 egjensenMyCurl.py http://www.example.com:443