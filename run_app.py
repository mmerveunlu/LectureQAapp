from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def form():
    with open('subs/Lecture1-English.txt', 'r') as f:
        text = f.read()
    return render_template('video-question-page.html', text=text)

@app.route('/question', methods=['GET', 'POST'])
def question():
    # TODO: altyazi text i icinde html kod olursa acaba sayfada gorunur mu?
    # Boylece highlight kismini yapabilir miyim? 
    with open('subs/Lecture1-English-answer.txt', 'r') as f:
        text = f.read()
    # TODO: answer will come from QA-server
    answer_text = "NLP people call a large pile of text a corpus"    
    return render_template('video-answer-page.html',
                           text=text,
                           question=request.form['question'],
                           answer=answer_text)


if __name__ == "__main__":
    app.run()
