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
        res = filter_transcript(keywords)
    else:
        res = ""

    return (
        """
        <!DOCTYPE html>
        <html>
        
        <style>
        body 
        {
            margin:auto;
            width:80%;
            padding:10px;
            background-color:#1a1a1a;
            font-size:18px;
            font-family:Helvetica;
            color:#bbbbbb;
        }
        input:focus::placeholder 
        {
            color: transparent;
        }
        input[type=text] 
        {
            width: 100%;
            height: 60px;
            padding: 12px 20px;
            margin: 8px 0;
            box-sizing: border-box;
            border: 2px solid red;
            border-radius: 4px;
            font-size: 20px;
        }
        input[type=submit]
        {
            background-color: white;
            border: none;
            color: black;
            padding: 16px 32px;
            text-decoration: none;
            margin: 4px 2px;
            cursor: pointer;
        }
        a:link 
        {
            color:#0096FF;
        }
        a:visited {
            color:#0096FF;
        }
        a:hover {
            color:#89CFF0;
        }
        </style>


        <h1> Helper 138 </h1>
        <h3> <a href="https://cdn.discordapp.com/attachments/1013687788807405579/1049190892583526443/all138slidesAnnotated.pdf">Link to PDF of all slides</a>
         (Includes table of contents for each chapter, section, and subsection!) </h3>
        <h3> <a href="https://youtube.com/playlist?list=PLis31mB9Uihr9Z_wFL0rMAP__CbuFYZVx" target="_blank" rel="noopener noreferrer">Link to all lectures Youtube Playlist</a> </h3>
        
        <h2> Instructions </h2>
        This is a study tool for CSC138.
        In the box below, you can search keywords or phrases from all lectures. 
        To search multiple keywords, separate them by a comma as shown in the example below.
        The search is case sensitive so you may want to try different variations of the same word. 
        Only exact matches will be found.
        <br><br>
        For example, you can type something like <code style="background-color:#301934"> test,exam,DNS,dns</code> into the search box
        and all occurences of the professor saying any of those keywords will be displayed.
        <br>
        <br>
        Click the timestamp link to go to that part of the lecture. Goodluck on the final!
        <br><br>
        <form action="" method="get">
                    <input type="text" placeholder="type something here"  name="keywords">
                    <input type="submit" value="Search">
                </form>"""
        + res +
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
            words = text.split()
            keywordslist = keywords.split(sep='|')
            for i in range(len(words)):
                if words[i] in keywordslist:
                    words[i] = '<b><span style="color: #FF3131">' + \
                        words[i] + '</span></b>'
            text = ' '.join(words)
            # accumulating each text group into one large output
            res += f'<p><a href="{links[video]}?t={seconds}" target="_blank" rel="noopener noreferrer">{video} Lecture - {timestamp}</a>' \
                + '<br>' + text + '</p>'
        except Exception as e:
            print(e)  # Most likely due to index OOB
            continue
    # print(res)
    return str(res)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
