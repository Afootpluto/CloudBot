import time
import random
import subprocess
import re
import os
import socket

from cloudbot.util import web
from cloudbot.util.colors import parse, strip_all
from data.ports import toScan
from plugins.minecraft_ping import *
from cloudbot import hook
from plugins.usingBot import getTokens, takeTokens


def scanport(IP, PORT):
    """
    :return: True/False if the port is open for the give ip:port
    """
    time.sleep(0.005)
    # noinspection PyBroadException
    try:
        s = socket.socket()
        s.connect((IP, PORT))
        return True
    except:
        return False


def colorize(number, low, med, lowcolor="$(dark_green)", medcolor="$(orange)", highcolor="$(red)",
             clearcolor="$(clear)"):
    """
    :param number: The value to test
    :param low: limit where the result will be lowcolor
    :param med: limit where the resul will be medcolor. If it's higher it'll turn highcolor
    :param lowcolor: color to use for the lower values (default to green)
    :param medcolor: color to use for the medium values (default to orange)
    :param highcolor: color to use for the lower values (default to red)
    :param clearcolor: color to use to clear (default to clear)
    :return: a ready to be parsed string
    """

    if float(number) <= low:
        return lowcolor + number + clearcolor
    elif float(number) <= med:
        return medcolor + number + clearcolor
    else:
        return highcolor + number + clearcolor


@hook.command("portscan1", "ps1", "scan1")
def scanOne(reply, text, nick, notice):
    """
    Command to scan a single port
    """

    if getTokens(nick) < 1000:
        notice("You don't have enough tokens to do a portscan (1000 needed)... Help a little more !")
        return None

    args = text.split()

    try:
        IP = str(args[0])
        PORT = int(args[1])
    except IndexError:
        notice("Syntax : !ps1 IP PORT. Use !ps3000 for the 3000 most used ports")
        return None

    takeTokens(100, nick, notice)
    socket.setdefaulttimeout(5)
    reply("Scanning port number " + str(PORT) + " for ip " + str(IP))

    result = scanport(IP, PORT)

    if result:
        reply("The port " + str(PORT) + " of the IP " + IP + " is OPEN !")
    elif not result:
        reply("The port " + str(PORT) + " of the IP " + IP + " is CLOSED ! ")


@hook.command("portscan3000", "scan3000", "ps3000")
def scan3000(reply, text, nick, notice):
    """
    Command to scan the 3000 most used ports. List from nmap
    """
    if getTokens(nick) < 10000:
        notice("You don't have enough tokens to do a portscan3000 (10000 needed)... Help a little more !")
        return None

    if not text:
        reply("Please specify an IP address/ dns ! !ps3000 IP")

    scanned = 0

    takeTokens(500, nick, notice)
    IP = text
    openPorts = []
    timeout = float((float(pingavg(IP)) / 100) + 0.5)
    socket.setdefaulttimeout(timeout)
    notice("i'm scanning with a timeout of " + str(timeout))
    reply("Scanning 3000 ports... It's a long task, you'll have to wait !")

    for PORT in toScan:
        scanned += 1
        if scanport(IP, PORT):
            openPorts.append(PORT)

        if scanned % 250 == 0:
            notice("Progress (" + str(IP) + "): " + str(scanned) + " / 3000")

    openPorts.sort()
    reply("Open ports found for " + text + " (" + str(len(openPorts)) + "): " + str(openPorts))


@hook.command("passwordgenerator", "genpass", "passgen", "password")
def passgen(reply, nick, notice):
    """
    Command to generate a random 10 chars password
    """

    if getTokens(nick) < 100:
        notice("You don't have enough tokens to do a password generation (100 needed)... Help a little more !")
        return None

    takeTokens(5, nick, notice)

    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890^=+/:.;?,-_)&"'(!<>'
    pw_length = 10
    mypw = ""

    for i in range(pw_length):
        next_index = random.randrange(len(alphabet))
        mypw += alphabet[next_index]

    reply("I just generated a 10 chars random password for you ! Here you go ! " + mypw)


unix_ping_regex = re.compile(r"(\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")
win_ping_regex = re.compile(r"Minimum = (\d+)ms, Maximum = (\d+)ms, Average = (\d+)ms")


@hook.command()
def ping(text, reply, notice):
    """<host> [count] - pings <host> [count] times"""

    args = text.split(' ')
    host = args[0]

    # check for a second argument and set the ping count
    if len(args) > 1:
        count = int(args[1])
        if count > 20:
            count = 20
    else:
        count = 5

    count = str(count)

    if os.name == "nt":
        args = ["ping", "-n", count, host]
    else:
        args = ["ping", "-c", count, host]

    notice("Attempting to ping {} {} times...".format(host, count))
    try:
        pingcmd = subprocess.check_output(args).decode("utf-8")
    except subprocess.CalledProcessError:
        return "Could not ping host."

    if re.search("(?:not find host|timed out|unknown host)", pingcmd, re.I):
        return "Could not ping host."

    if os.name == "nt":
        m = re.search(win_ping_regex, pingcmd)
        r = int(m.group(2)) - int(m.group(1))
        min, max, avg, range, count = str(m.group(1)), str(m.group(2)), str(m.group(3)), str(r), str(count)
    # return "min: %sms, max: %sms, average: %sms, range: %sms, count: %s" \
    #			   % (m.group(1), m.group(2), m.group(3), r, count)
    else:
        m = re.search(unix_ping_regex, pingcmd)
        min, max, avg, range, count = str(m.group(1)), str(m.group(3)), str(m.group(2)), str(m.group(4)), str(count)
    # return "min: %sms, max: %sms, average: %sms, range: %sms, count: %s" \
    #			   % (m.group(1), m.group(3), m.group(2), m.group(4), count)

    # Build up a toreply str
    toreply = "min: " + colorize(min, 20, 50) + ", max: " + colorize(max, 30, 100) + ", average: " + colorize(avg, 25,
                                                                                                              75) + ", range: " + colorize(
        range, 5, 10) + ", count: " + count

    return parse(host + " : " + toreply)


def pingavg(host):
    if os.name == "nt":
        args = ["ping", "-n", "2", host]
    else:
        args = ["ping", "-c", "2", host]

    try:
        pingcmd = subprocess.check_output(args).decode("utf-8")
    except subprocess.CalledProcessError:
        return -1

    if re.search("(?:not find host|timed out|unknown host)", pingcmd, re.I):
        return -1

    if os.name == "nt":
        m = re.search(win_ping_regex, pingcmd)
        return m.group(3)
    else:
        m = re.search(unix_ping_regex, pingcmd)
        return m.group(2)


@hook.command("harmonystatus", "hhstatus", "harmony", "ddos", "pinghh", "hh")
def hhstatus(reply, notice, nick):
    """
    :return: Check the status of harmonyhosting's servers, and some external servers.
    """
    if getTokens(nick) < 100:
        notice("You don't have enough tokens. (100 needed)... Help a little more !")
        return None

    notice("Je vérifie le statut des serveurs ! Cela prends environ 20 secondes, voire moins !")
    InternalHosts = sorted(["lisa", "homer", "marge", "maggie", "flanders", "www", "apu", "burns", "irc"])
    ExternalHosts = sorted(["bukkit.fr", "google.fr", "ovh.com", "proof.ovh.net", "iooner.klat00.org"])
    #	dead = []
    #	good = []
    #	bad = []
    toreply = "NODES : "

    for host in InternalHosts:
        avg = float(pingavg(host + ".harmony-hosting.com"))

        if avg == -1:
            # dead.append(host)
            toreply += "$(dark_red)" + host + "(ERR)" + "$(clear) "
        elif avg <= 20:
            # good.append(host)
            toreply += "$(dark_green)" + host + "$(clear) "
        elif avg <= 1000:
            # bad.append(host)
            toreply += "$(orange)" + host + "(" + str(avg) + " ms)" + "$(clear) "
        else:
            # dead.append(host)
            toreply += "$(red)" + host + "(" + str(avg) + " ms)" + "$(clear) "

    toreplyINT = parse(toreply)

    toreply = "SERVICES: "
    for host in ExternalHosts:
        avg = float(pingavg(host))

        host = host.replace('.', '_')

        if avg == -1:
            # dead.append(host)
            toreply += "$(dark_red)" + host + "$(clear) "
        elif avg <= 20:
            # good.append(host)
            toreply += "$(dark_green)" + host + "$(clear) "
        elif avg <= 1000:
            # bad.append(host)
            toreply += "$(orange)" + host + "(" + str(avg) + " ms)" + "$(clear) "
        else:
            # dead.append(host)
            toreply += "$(red)" + host + "$(clear) "

    toreplyEXT = parse(toreply)

    reply(toreplyINT)
    reply(toreplyEXT)


@hook.command("serverinfo", "servinfo")
def servinfo(reply, text, notice, nick):
    """
    :return: Give the user info about a server common services
    """
    if getTokens(nick) < 1000:
        notice("You don't have enough tokens to do a portscan (1000 needed)... Help a little more !")
        return None

    takeTokens(250, nick, notice)
    host = text

    # First of all, check the ping !
    ping = float(pingavg(host))

    # Check if ssh is working (port 22 open)
    sshWorking = scanport(host, 22)

    # Check if web HTTP is working
    httpWorking = scanport(host, 80)

    # Check if web HTTP is working
    httpsWorking = scanport(host, 443)

    # Check if DNS is working
    dnsWorking = scanport(host, 53)

    # Check if SMTP is working
    smtpWorking = scanport(host, 25)

    # Lets reply that !
    toreply = ""

    if ping == -1:
        toreply += "$(dark_red)ping $(clear)"
    elif ping <= 20:
        toreply += "$(dark_green)ping $(clear)"
    elif ping <= 1000:
        toreply += "$(orange)ping (" + str(ping) + " ms)" + "$(clear)"
    else:
        toreply += "$(red)ping $(clear)"

    if sshWorking:
        toreply += "$(dark_green)ssh $(clear)"
    else:
        toreply += "$(red)ssh $(clear)"

    if httpWorking:
        toreply += "$(dark_green)http $(clear)"
    else:
        toreply += "$(red)http $(clear)"

    if httpsWorking:
        toreply += "$(dark_green)https $(clear)"
    else:
        toreply += "$(red)https $(clear)"

    if dnsWorking:
        toreply += "$(dark_green)dns $(clear)"
    else:
        toreply += "$(red)dns $(clear)"

    if smtpWorking:
        toreply += "$(dark_green)smtp  $(clear)"
    else:
        toreply += "$(red)smtp $(clear)"

    reply(host + " : " + parse(toreply))


@hook.command("securebungee", "bungeesecure", "bungee")
def bungeesec(reply, text, nick, notice):
    """
    This will scan ports near 25565 to check if a bungee server is secured or not.
    """
    if getTokens(nick) < 15000:
        notice("You don't have enough tokens to do a bungeesecure (15000 needed)... Help a little more !")
        return None

    if not text:
        reply("Please specify an IP address/ dns ! !bungeesecure IP")

    takeTokens(2000, nick, notice)
    IP = text
    timeout = float((float(pingavg(IP)) / 100) + 0.1)
    socket.setdefaulttimeout(timeout)
    notice("I'm scanning with a timeout of " + str(timeout))
    reply("Scanning ports... I'll tell you my progress, please wait !")
    toreply = "List of minecraft servers found for : " + str(IP) + ":\n"

    found = 0

    start = 20000
    end = 40000

    for PORT in range(start, end):
        if scanport(IP, PORT):
            mcinfo = pingmc(IP, PORT)
            if mcinfo:
                toreply += "Server found on port " + str(PORT) + " : " + str(mcinfo) + "\n"
                found += 1

        if PORT % 250 == 0:
            notice(
                "Progress bungeesec (" + str(IP) + "): " + str(int(PORT) - 20000) + " / 20000 | Found so far : " + str(
                    found))

    if found == 0:
        toreply += "No servers found. Check the entered IP address."

    if found < 5:
        return toreply
    else:
        return web.paste(strip_all(toreply))


def pingmc(ip, port=25565):
    """
    :param ip: The IP/DNS of the server
    :param port: The port to check, usually 25565
    :return: A formatted string giving info on the minecraft server
    """

    try:
        server = MinecraftServer.lookup(str(ip) + ":" + str(port))
        s = server.status()
    except:
        return None

    if isinstance(s.description, dict):
        description = format_colors(" ".join(s.description["text"].split()))
    else:
        description = format_colors(" ".join(s.description.split()))

    if s.latency:
        return "{}\x0f - \x02{}\x0f - \x02{:.1f}ms\x02" \
               " - \x02{}/{}\x02 players".format(description, s.version.name_clean, s.latency,
                                                 s.players.online, s.players.max).replace("\n", "\x0f - ")
    else:
        return "{}\x0f - \x02{}\x0f" \
               " - \x02{}/{}\x02 players".format(description, s.version.name_clean,
                                                 s.players.online, s.players.max).replace("\n", "\x0f - ")
