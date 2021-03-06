import praw #reddit
import random
import time
import datetime
import traceback #para logear los errores
import botlogin #informacion personal para log in del bot
import unicodedata
import string

def update_log(id, log_path): #para los comentarios que ya respondi
    with open(log_path, 'a') as my_log:
        my_log.write(id + "\n")

def load_log(log_path): #para los comentarios que ya respondi
    with open(log_path) as my_log:
        log = my_log.readlines()
        log = [x.strip('\n') for x in log]
        return log

def output_log(text): #lo uso para ver el output del bot
    output_log_path = "output_log.txt"
    with open(output_log_path, 'a') as myLog:
        s = "[" +  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] "
        s = s + text +  "\n"
        myLog.write(s)

def find_substring(needle, haystack):
    index = haystack.find(needle)
    if index == -1:
        return False
    if index != 0 and haystack[index-1] in string.letters:
        return False
    L = index + len(needle)
    if L < len(haystack) and haystack[L] in string.letters:
        return False
    return True

uruguay_misspells = [
    "urugay",
    "uraguay",
    "uragay",
    "urogway",
    "uruguauy",
    "uruguary",
    ]

def is_quote(text):
    if len(text) > 1:
        return text[0] == '>'

def check_misspells(text, misspells):
    for version in misspells:
        if find_substring(version, text.lower()):
            return True

def check_condition(c): #llamaron al bot?
    for p in c.body.split('\n'):
        # separo en parrafos para no responder a texto citado.
        if not is_quote(p) and check_misspells(p, uruguay_misspells):
            return True

def get_reply():
    replies = [ "Did you mean *Uruguay**?",
                "I'm pretty sure you meant *Uruguay**",
                ]
    return random.choice(replies)


print("RUNNING")
if __name__ == "__main__":
    comment_log_path = "log.txt"
    while True:
        try:
            
            output_log("Comenzando el script")
            log = load_log(comment_log_path)
            reddit = praw.Reddit(   client_id = botlogin.client_id,
                                    client_secret = botlogin.client_secret,
                                    password = botlogin.password,
                                    user_agent = "Its_URUGUAY_bot script by Sevg/Dirkgentle/ElectrWeakHyprCharge",
                                    username = botlogin.username)
            print("Logged to reddit as " + reddit.user.me().name)                       
            output_log("Login to reddit as: " + reddit.user.me().name)
            

            for comment in reddit.subreddit('all').stream.comments():
                if check_condition(comment) and comment.id not in log:
                    #output_log("{" + unicodedata.normalize('NFKD', comment.body).encode('ascii', 'ignore') + "}") #esto porque me daba pila de problemas los comentarios unicode
                    reply = get_reply()
                    
                    s = "\n\n*****"
                    s = s + "\n\n Script by \/u/Sevg, hosting by \/u/DirkGentle *^and ^yes, ^weed ^is ^legal ^here*"
                    s = s + "\n\n [Source.](https://github.com/sevgit/Its_URUGUAY_bot)"
                    
                    
                    comment.reply(reply + s)
                    output_log("{" +  reply + "}")
                    log.append(comment.id)
                    update_log(comment.id, comment_log_path) 
        except Exception as exception:
            
            output_log(str(exception))
            output_log(traceback.format_exc())
