import sys
from cloudbot import hook
import os


@hook.command("addbadword", "adbw", permissions=["badwords"])
def addbadword(chan, text):
        list = open(os.path.join("/badwords/" + chan + ".txt"), "wr" )
        list.write(text)
        list.write("\n")

@hook.command("delbadword", "delbw", permissions=["badwords"])
def delbadword(chan, text):
    open(os.path.join("/badwords/" + chan + ".txt"), "wr" )

@hook.command("badwordlist", "bwl", permissions=["badwords"])
    def badwordlist(chan, text):
        open(os.path.join("/badwords/" + chan + ".txt"), "r" )

@hook.regex()
