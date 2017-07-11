import praw
import datetime
import os
import re
from time import sleep

def factorial(string):
    fact_num = int(string)
    if fact_num <= 1:
        return 1
    else:
        return fact_num * factorial(fact_num - 1)


def get_number(string):
    if re.findall("\d+", string):
        return True
    return False

def reply_to_comment(reddit, subreddit, amount):
    for comment in reddit.subreddit(subreddit).comments(limit=amount):
        if comment.author != reddit.user.me():
            if "!" in comment.body:
                try:
                    index_of_exlamation = comment.body.index("!")
                    index_of_number = re.search("\d", comment.body)
                    quote_string = comment.body[index_of_number.start()] + comment.body[index_of_exlamation]
                    fact_num = factorial(comment.body[index_of_number.start()])
                    print("replying")
                    comment.reply("> {quote} \n\n = {fact}".format(quote=quote_string, fact=fact_num))
                except ValueError as e:
                    pass

def did_reply(filepath, id):
    if id in open(filepath).read():
        return True
    return False


def reply_to_comment2(reddit, subreddit, amount):
    for comment in reddit.subreddit(subreddit).comments(limit=amount):
        if comment.author != reddit.user.me() and not did_reply(comments_replied_filename, comment.id):
            if "!" in comment.body:
                index_of_exlamation = comment.body.index("!")
                index_of_numbers = re.findall("\d", comment.body)
                for i in range(len(index_of_numbers)):
                    index_of_number = comment.body.index(index_of_numbers[i])
                    if "!" in comment.body[index_of_number:]:
                        print("replying")
                        quote_string = "> {}".format(comment.body[index_of_number:])
                        fact_num = factorial(comment.body[index_of_number:-1])
                        reply = "{quote} \n\n = {fact}".format(quote=quote_string, fact=fact_num)
                        comment.reply(reply)

                        with open(comments_replied_filename, "a") as f:
                            print("writing to file")
                            f.write(comment.id + "\n")

reddit = praw.Reddit("bot1")
test_sub = "PythonInfoBotTest"
bot_name = "UserInfo_Bot"
bot_profile = reddit.redditor(bot_name) 

blacklisted_subs_filepath = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\blacklisted_subreddits.txt"
blacklisted_users_filepath = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\blacklisted_users.txt"
posts_replied_filepath = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\posts_replied.txt"
comments_replied_filename = "C:\\Users\\Gutman\\Desktop\\Reddit_Bot\\comment_replied.txt"

reply_to_comment2(reddit, test_sub, 15)
