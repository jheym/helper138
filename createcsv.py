# I made this just for creating the csv since my trifacta wrangler trial is over :(

import itertools
outfile = open('transcript.csv', 'a')
VIDEO = '10-10'
with open(f'transcripts/{VIDEO}.txt') as infile:
    for line1, line2 in itertools.zip_longest(*[infile]*2):
        time = line1.split(':', 1)
        seconds = (int(time[0]) * 60) + int(time[1])
        outfile.write(f'"{VIDEO}","' + line1.strip() +
                      '","' + line2.strip() + '"\n')

    # adding lines with matches to final list
    # results.append('<p> <a href = "https://youtu.be/VS5L-Z1vnj4?t={}" target = "_blank" rel = "noopener noreferrer">{}</a>'.format(
    #     seconds, line1.strip()) + ' ' + line2.strip() + '<br></p>')

    # return str(results).replace('[', '').replace(']', '').replace("'", '').replace(',', '')
