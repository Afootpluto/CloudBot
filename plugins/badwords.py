import sys
from cloudbot import hook
import os
import re
from cloudbot.util import textgen


@hook.command("addbadword", "adbw", permissions=["badwords"])
def addbadword(chan, text):
        list = open(os.path.join("badwords/" + chan + ".txt"), "wr" )
        list.read = old
        list.write(old + text + "\n")

@hook.command("delbadword", "delbw", permissions=["badwords"])
def delbadword(chan, text):
    open(os.path.join("badwords/" + chan + ".txt"), "wr" )

@hook.command("badwordlist", "bwl", permissions=["badwords"])
def badwordlist(chan, text):
        open(os.path.join("badwords/" + chan + ".txt"), "r" )

@hook.regex()
def badword(text , chan , nick):
    list = open(os.path.join("badwords/" + chan + ".txt"), "wr" )
    for line in list:
        line = line.rstrip()
        if re.search(text , line) :
            conn.send("KICK " + chan + " " + nick " You aren't allowed to say: " + line)
        else
            return None
