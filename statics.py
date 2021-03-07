# Define constant file path
# On the client
SPATH = "/var/www/LectureQAapp/LectureQAapp/"
DATAPATH = "/var/www/LectureQAapp/LectureQAapp/static/example-questions.json"
QPATH = "/var/www/LectureQAapp/LectureQAapp/static/asked-questions.txt"
STATFOLDER = "/var/www/LectureQAapp/LectureQAapp/static/"

# On the Server
SERVERDPATH = "/work/merve/dataFromClient/"
PREVPATH = ".."

chapter_keys = ['_ch03_2','_ch07_1','_ch05_1','_ch09_2','_ch01_5',
                '_ch01_3','_ch02_2','_ch03_1','_ch03_4','_ch01_4',
                '_ch04_1','_ch09_1','_ch01_0','_ch01_1','_ch01_2']

lectures1 = {
    'video1': {"ylink": "https://youtu.be/eh2yO5YtqRM",
                 "subtitle": "static/ENG_001_20151602_01204_ch01_0.en.vtt",
                 "key":"_ch01_0",
                 "title":"Introduction to Signal and Systems"},
    'video2': {"ylink": "https://youtu.be/nZAvdNK0d74",
                 "subtitle": "static/ENG_001_20151602_01204_ch01_1.en.vtt",
                 "key":"_ch01_1",
                 "title":"Transformation of the Independent Variable"},
    'video3': {"ylink": "https://youtu.be/MBOi3sAOkFc",
                 "subtitle": "static/ENG_001_20151602_01204_ch01_2.en.vtt",
                 "key":"_ch01_2",
                 "title":"Continuous-Time Exponential and Sinusoidal Signals"},
    'video4': {"ylink": "https://youtu.be/gUOj7r0IxSk",
                 "subtitle": "static/ENG_001_20151602_01204_ch01_3.en.vtt",
                 "key":"_ch01_3",
                 "title":"Discrete-Time Exponential and Sinusoidal Signals"},
    'video5': {"ylink": "https://youtu.be/UlWF-Flea9c",
                 "subtitle": "static/ENG_001_20151602_01204_ch01_4.en.vtt",
                 "key":"_ch01_4",
                 "title":"Unit Impulse and Unit Step Functions"},
    'video6': {"ylink": "https://youtu.be/9iJr0KNQruo",
                 "subtitle": "static/ENG_001_20151602_01204_ch01_5.en.vtt",
                 "key":"_ch01_5",
                 "title":"Basic System Properties"},
}


lectures2 = {
    'video1': {"ylink": "https://youtu.be/koUZFxyeYXg",
                 "subtitle": "static/ENG_001_20151602_01204_ch02_0.en.vtt",
                 "key":"_ch02_0",
                 "title":"Convolution Sum and Convolution Integral"},
    'video2': {"ylink": "https://youtu.be/dpjbA1zDGXE",
                 "subtitle": "static/ENG_001_20151602_01204_ch02_1.en.vtt",
                 "key":"_ch02_1",
                 "title":"Properties of LTI Systems"},
}

lectures31 = {
    'video1': {"ylink": "https://youtu.be/Mt0pnYVQRq8",
                 "subtitle": "static/ENG_001_20151602_01204_ch03_0.en.vtt",
                 "key":"_ch03_0",
                 "title":"Response of LTI systems to complex exponentials"},
    'video2': {"ylink": "https://youtu.be/HI2Hcw_tIK4",
                 "subtitle": "static/ENG_001_20151602_01204_ch03_1.en.vtt",
                 "key":"_ch03_1",
                 "title":"Fourier series representation of continuous-time periodic signals"},
}


lectures32 = {
    'video1': {"ylink": "https://youtu.be/2Sfld9mg-no",
                 "subtitle": "static/ENG_001_20151602_01204_ch03_0.en.vtt",
                 "key":"_ch03_0",
                 "title":"Fourier series representation of discrete-time periodic signals"},
}

lectures4 = {
    'video1': {"ylink": "https://youtu.be/F-8OlJYMXPk",
                 "subtitle": "static/ENG_001_20151602_01204_ch04_0.en.vtt",
                 "key":"_ch04_0",
               "title":"Continuous-Time Fourier Transform"},
}

lectures5 = {
    'video1': {"ylink": "https://youtu.be/QUMJ8-dtsnI",
                 "subtitle": "static/ENG_001_20151602_01204_ch05_0.en.vtt",
                 "key":"_ch05_0",
               "title":"Discrete-Time Fourier Transform"},
}


lectures7 = {
    'video1': {"ylink": "https://youtu.be/XhGEmrdthfY",
                 "subtitle": "static/ENG_001_20151602_01204_ch07_0.en.vtt",
                 "key":"_ch07_0",
               "title":"Sampling"},
    'video2': {"ylink": "https://youtu.be/geTD4_Ho89E",
                 "subtitle": "static/ENG_001_20151602_01204_ch07_1.en.vtt",
                 "key":"_ch07_1",
               "title":"Interpolation"},
    'video3': {"ylink": "https://youtu.be/uPd0fQr7-gY",
                 "subtitle": "static/ENG_001_20151602_01204_ch07_2.en.vtt",
                 "key":"_ch07_2",
               "title":"Discrete-Time Processing of Continuous-Time Signals"},
    'video4': {"ylink": "https://youtu.be/E4ukWO459M8",
                 "subtitle": "static/ENG_001_20151602_01204_ch07_3.en.vtt",
                 "key":"_ch07_3",
               "title":"Sampling of Discrete-Time Signals"},
}

lectures9 = {
    'video1': {"ylink": "https://youtu.be/0pgpBrHANmg",
                 "subtitle": "static/ENG_001_20151602_01204_ch09_0.en.vtt",
                 "key":"_ch09_0",
               "title":"The Laplace Transform"},
    'video1': {"ylink": "https://youtu.be/ZtJQXSIB08A",
                 "subtitle": "static/ENG_001_20151602_01204_ch09_1.en.vtt",
                 "key":"_ch09_1",
               "title":"The Region of Convergence"},

}

lecture_dict = {'Chapter 1':lectures1,'Chapter 2':lectures2, 'Chapter 3-1':lectures31, 'Chapter 3-2':lectures32 , \
                'Chapter 4':lectures4, 'Chapter 5':lectures5, 'Chapter 7': lectures7, 'Chapter 9':lectures9 }

video_dict = {'Chapter 1': ['Video 1 : Introduction to Signals and Systems',\
              'Video 2 : Transformation of the Independent Variable',\
              'Video 3 : Continuous-Time Exponential and Sinusoidal Signals',\
              'Video 4 : Discrete-Time Exponential and Sinusoidal Signals',\
              'Video 5 : Unit Impulse and Unit Step Functions',\
                                        'Video 6 : Basic System Properties'],
              'Chapter 2': ['Video 1 : Convolution Sum and Convolution Integral', \
                                       'Video 2 : Properties of LTI Systems'],
              'Chapter 3-1': ['Video 1 : Response of LTI systems to complex exponentials',
                              'Video 2 : Fourier series representation of continuous-time periodic signals'],
              'Chapter 3-2': ['Video 1 : Fourier series representation of discrete-time periodic signals'],
              'Chapter 4': ['Video 1 : Continuous-Time Fourier Transform'],
              'Chapter 5': ['Video 1 : Discrete-Time Fourier Transform'],
              'Chapter 7': ['Video 1 : Sampling',
                            'Video 2 : Interpolation',
                            'Video 3 : Discrete-Time Processing of Continuous-Time Signals',
                            'Video 4 : Sampling of Discrete-Time Signals'],
              'Chapter 9': ['Video 1 : The Laplace Transform',
                            'Video 2 : The Region of Convergence']}

counts = {'Chapter 1':6,'Chapter 2':2,'Chapter 3-1':1,'Chapter 3-2':1,'Chapter 4':1,'Chapter 5':1,'Chapter 7':4,'Chapter 9':2}


SEP=","

HOST="10.2.1.55"
PORT= 65432
