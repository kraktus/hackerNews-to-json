# Hacker News to JSON

Save 'saved stories' from a Hacker News account to a simple JSON format.

The script parses the saved stories page on HN (http://news.ycombinator.com) and, for each link on each page of the saved stories history it outputs an entry to a JSON document with information taken from the Hacker News API. (https://github.com/HackerNews/API)

The script is meant to be launched from the command line.

Originally developed on iPad by Luciano Fiandesio with the awesome Pythonista (http://omz-software.com/pythonista/), modified for JSON output by John David Pressman (https://github.com/JD-P/HackerNewsToJSON), and rewritten by Kraktus.

## How to use

`HN_COMMENTS_ACCT=foo HN_COMMENTS_PW=bar python hn2json.py -n [Number of pages to grab] -f [JSON filename]`

See `python hn2json.py -h` for more options.

You can also set `HN_COMMENTS_ACCT` and `HN_COMMENTS_PW` in an `.env` file in the same directory as the script.