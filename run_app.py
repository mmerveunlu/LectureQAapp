from flask import Flask, render_template, request

app = Flask(__name__)


lectures = {'lecture1':{"ylink":"https://youtu.be/eh2yO5YtqRM","subtitle":"static/ENG_001_20151602_01204_ch01_0.en.vtt"},
            'lecture2':{"ylink":"https://youtu.be/nZAvdNK0d74","subtitle":"static/ENG_001_20151602_01204_ch01_1.en.vtt/"}}


@app.route('/', methods=['GET', 'POST'])
def form():
    ylink = "https://youtu.be/eh2yO5YtqRM"
    subtitle = "static/ENG_001_20151602_01204_ch01_0.en.vtt"
    return render_template('video-question-page.html', ylink=ylink, subtitle=subtitle)

@app.route('/question', methods=['GET', 'POST'])
def question():
    ylink = "https://youtu.be/eh2yO5YtqRM"
    subtitle = "static/ENG_001_20151602_01204_ch01_0.en.vtt"
    for lecture in lectures.keys():
        if request.form.get(lecture):
            # print("Button %s is clicked" %lecture)
            ylink = lectures[lecture]["ylink"]
            subtitle = lectures[lecture]["subtitle"]
    return render_template('video-question-page.html', ylink=ylink, subtitle=subtitle)


@app.route('/answer', methods=['GET', 'POST'])
def answer():
    # TODO: answer will come from QA-server
    ylink = request.form['ylink']
    subtitle = request.form['subtitle']
    answer_text = "NLP people call a large pile of text a corpus"    
    return render_template('video-answer-page.html',
                           question=request.form['question'],
                           answer=answer_text,
                           ylink = ylink,
                           subtitle= subtitle)


if __name__ == "__main__":
    app.run()
