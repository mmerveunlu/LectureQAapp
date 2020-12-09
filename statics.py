# Define constant file path
# On the client 
SPATH = "/var/www/LectureQAapp/LectureQAapp/"
DATAPATH = "/var/www/LectureQAapp/LectureQAapp/static/example-questions.json"
QPATH = "/var/www/LectureQAapp/LectureQAapp/static/asked-questions.txt"


# On the Server
SERVERDPATH = "/work/merve/dataFromClient/"
PREVPATH = ".."

chapter_keys = ['_ch03_2','_ch07_1','_ch05_1','_ch09_2','_ch01_5',
                '_ch01_3','_ch02_2','_ch03_1','_ch03_4','_ch01_4',
                '_ch04_1','_ch09_1','_ch01_0','_ch01_1','_ch01_2']

lectures = {
    'lecture1': {"ylink": "https://youtu.be/eh2yO5YtqRM", "subtitle": "static/ENG_001_20151602_01204_ch01_0.en.vtt", "key":"_ch01_0"},
    'lecture2': {"ylink": "https://youtu.be/nZAvdNK0d74", "subtitle": "static/ENG_001_20151602_01204_ch01_1.en.vtt", "key":"_ch01_1"}}

SEP=","

HOST="10.2.1.55"
PORT= 65432
