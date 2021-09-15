import praw
import pandas as pd
import config
import time

# connects to reddit praw object using the reddit application api client id and client secret
def reddit_object():

    reddit = praw.Reddit(client_id = config.client_id,
                        client_secret = config.client_secret,
                        user_agent = config.user_agent,
                        username = config.username,
                        password = config.password)

    return reddit

#Calls up to the last 1000 submissions from learnpython
def scrape_submissions_1000(reddit):
    sub_list = []
    # selects the subreddit learnpython.  This can be changed to any subreddit
    subreddit = reddit.subreddit('drumkits')
    # have it currently calling 100 submissions at a time, but can be any number between 1 and 1000
    for submission in subreddit.hot(limit=12):
        # different submission attributes I choose to pull are below
        # look at the praw documentation for other submission attributes



        text = submission.selftext
        title = submission.title
        pk = submission.id
        direction = submission.url

        sub_list.append([pk, title, direction])
    df = pd.DataFrame(sub_list, columns=['id','title', 'direction'])

    return df


def new_submissions(df):
    # pulls full csv
    df_current = pd.read_csv('learnpython_submissions.csv', index_col=0)

    # Checks for only the new rows in the df
    new_submission = df[~df['id'].isin(df_current['id'])]

    new_sub_list = new_submission.values.tolist()

    # Removes first 2 columns (#, id)


    # Appends the new submissions to the current pandas df which was read from the learnpython_submissions.csv
    df_current = df_current.append(new_submission, sort=False)


    # saves new version of the csv
    df_current.to_csv('learnpython_submissions.csv')

    return new_sub_list, new_submission, df_current


def main():
    reddit = reddit_object()
    df = scrape_submissions_1000(reddit)
    new_sub_list, new_submission, df_current = new_submissions(df)
    print("new submissions: ", new_submission.shape)
    print("Current Dataframe: ", df_current.shape)


main()
