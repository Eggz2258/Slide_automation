cd /mnt/c/'Program Files (x86)'/Microsoft/Edge/Application
./msedge.exe --remote-debugging-port=9222 --user-data-dir="C:/Users/jishn/EdgeProfile"

cd /mnt/c/PycharmProjects/slide_scrape
source ./venv_linux/bin/activate

python3 test.py
