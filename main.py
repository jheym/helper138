from flask import Flask
from flask import request
import re
import pandas as pd
from links import links

app = Flask(__name__)

df = pd.read_csv('transcript.csv')


@app.route("/")
def index():

    keywords = request.args.get("keywords", "")
    if keywords:
        keywords = filter_transcript(keywords)
    else:
        keywords = ""

    return (
        """
        <!DOCTYPE html>
        <html>
        <style>
        body 
        {
            margin:auto;
            width:1024px;
            padding:10px;
            background-color:#1a1a1a;
            font-size:18px;
            font-family:Helvetica;
            color:#bbbbbb;
        }
        </style>
        <h1> Helper 138 </h1>
        <a href="https://cdn.discordapp.com/attachments/1013687788807405579/1049190892583526443/all138slidesAnnotated.pdf">Link to PDF of all slides</a>
         (Includes table of contents for each chapter, section, and subsection!)
        <br><br><br>
        This is a study tool for CSC138.
        In the box below, you can search keywords or phrases from all lectures. 
        <br><br>
        Separate keywords or phrases by commas, spaces are okay. Case sensitive.
        <br><br>
        For example, try something like this: 
        <p style="background-color:Gray;"> <code> exam,exams,final,test,remember this,important,understand,dns,DNS,TCP,tcp,http,HTTP </code> </p>
        <br>
        
        <br>
        Click the timestamp link to go to that part of the lecture. Goodluck on the final!
        <br><br>
        <form action="" method="get">
                    <input type="text" placeholder="test,exam,final,midterm,important,exams,tests" size="100" height="50" name="keywords">
                    <input type="submit" value="Search">
                </form>"""
        + keywords +
        """
        </body>
        </html>"""
    )


def filter_transcript(keywords: str):
    keywords = keywords.replace(',', '|')
    # Regex pattern for exact matching words e.g. '\b(final|exam|test)\b'
    # not that \b needs to be escaped
    pattern = rf'\b({keywords})\b'

    rowMatches = df.index[df['text'].str.contains(pattern) == True].tolist()
    # print(rowMatches)
    rowsExpanded = []

    # adding surrounding rows for more context
    for i in rowMatches:
        rowsExpanded.append([i - 2, i - 1, i, i + 1, i + 2])
    res = ''
    for i in rowsExpanded:
        try:
            timestamp = df.iloc[i[0]]['timestamp']
            video = df.iloc[i[0]]['video']
            text = ''
            # Calculate time in seconds from timestamp
            time = timestamp.split(':', 1)
            seconds = (int(time[0]) * 60) + int(time[1])
            # Accumulate all text from surrounding rows
            for rownum in i:
                text += df.iloc[rownum]['text'] + '\n'
            # Formatting matched strings in HTML
             # FIXME: When someone searches 'a', replace recursively replaces 'a' in </span> resulting in bad output
            for i in re.findall(pattern, text):
                text = text.replace(
                    i, '<b><span style="color: #ff0000">' + i + '</span></b>')

            res += f'<p><a href="{links[video]}?t={seconds}" target="_blank" rel="noopener noreferrer">{video} Lecture - {timestamp}</a>' \
                + '<br>' + text + '</p>'
        except Exception as e:
            print(e)  # Most likely due to index OOB
            continue
    # print(res)
    return str(res)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
