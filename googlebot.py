#!/usr/bin/env python2

from ircbot import SingleServerIRCBot
from irclib import nm_to_n, irc_lower, DEBUG
import string, time, re, random
import newgoogle as google
import twitter

class JackHandyBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.nickname = nickname
        self.channel = channel
        self.deepthoughts = self.meditate()
        self.start()

    def get_version(self):
        """Returns the bot version.
        Used when answering a CTCP VERSION request.
        """
        return "VERSION JackHandyBot by David Lucifer <david@lucifer.com>"
    
    def delay(self):
        time.sleep(random.randrange(2,5))
    
    def meditate(self):
        thoughts = []
        fp = open("deepthoughts.txt", "r")
        lines = fp.readlines()
        fp.close()
        for line in lines:
            line = string.strip(line)
            if len(line) > 0:
                thoughts.append(line)
                if DEBUG: print len(line), line
        return thoughts
          
    def on_topic(self,c,e):
        if e.arguments()[0] == self.channel:
            topic = e.arguments()[1]
        else:
            topic = e.arguments()[0]

    def on_welcome(self, c, e):
        if (self.channel != None):
            c.join(self.channel)
        
    def on_invite(self, c, e):
        channel = e.arguments()[0]
        self.delay()
        c.join(channel)

    def on_privmsg(self, c, e):
        args = e.arguments()
        msg = args[0]
        nick = nm_to_n(e.source())
        channel = e.target()
        
        output = self.do_command(nick, channel, msg)
        if output != None:
            self.privmsg_multiline(c,nick,output)

    def nick_is_voiced(self, channel, nick):
        return self.channels.has_key(channel) and self.channels[channel].is_voiced(nick)
    
    def is_listening(self, channel):
        mynick = self.connection.get_nickname()
        return self.channels.has_key(channel) and self.channels[channel].is_voiced(mynick)
    
    def i_am_mentioned(self, c, msg):
        msg = irc_lower(msg)
        mynick = irc_lower(c.get_nickname())
        pat = r"\b" + mynick + r"\b"
        return re.search(pat, msg)
        
    def on_ctcp(self, c, e):
        args = e.arguments()
        type = args[0]
        
        source = nm_to_n(e.source())
        channel = e.target()            

        if type == 'ACTION':
            if len(args) > 1:
                msg = args[1]
            else:
                msg = ""
            if self.i_am_mentioned(c, msg) and self.is_listening(channel):
                if not self.nick_is_voiced(channel, source):
                    self.privmsg_multiline(c, channel, random.choice(self.deepthoughts))
        else:
            return SingleServerIRCBot.on_ctcp(self, c, e)                          
        
    def on_pubmsg(self, c, e):
        args = e.arguments()
        msg = args[0]
        channel = e.target()
        source = nm_to_n(e.source())

        if not self.is_listening(channel):
            return
        
        if source == 'Futura':
            return
        
#        if self.nick_is_voiced(channel, source):
#            return
        
        m = re.search(r".*def:(.*)", msg)
        if m:
            terms = string.join(string.split(m.group(1)), '+')
            c.privmsg(channel, "Try http://www.hyperdictionary.com/search.aspx?Dict=&define=" + terms)
            return
        
        m = re.search(r".*tweet:(.*)", msg)
        if m:
            msg = "%s says '%s'" % (source, m.group(1).strip())

            c.privmsg(channel, "tweeting: " + msg)

            if len(msg) > 140:
                c.privmsg(channel, "oops, tweet is too long (keep it under 140 characters)")
                return

            try:
                api = twitter.Api(username='churchofvirus', password='p1ngp0ng')
                api.PostUpdate(msg)
            except:
                c.privmsg(channel, "bah, twitter service unavailable")
            return
        
        m = re.search(r".*udict:(.*)", msg)
        if m:
            terms = string.join(string.split(m.group(1)), '+')
            c.privmsg(channel, "Try http://www.urbandictionary.com/define.php?term=" + terms)
            return
        
        m = re.search(r".*wtf is (.*)", msg)
        if m:
            terms = m.group(1)
            c.privmsg(channel, "googling for " + terms)
            try:
                data = google.doGoogleSearch(terms)
                if len(data.results) > 0:
                    c.privmsg(channel, data.results[0].URL)
                else:
                    c.privmsg(channel, "no google results")
            except:
                c.privmsg(channel, "shit, google service unavailable")
            return

        m = re.search(r".*googlebot:(.*)", msg)
        if m:
            terms = m.group(1)
            c.privmsg(channel, "googling for " + terms)
            try:
                data = google.doGoogleSearch(terms)
                if len(data.results) > 0:
                    c.privmsg(channel, data.results[0].URL)
                else:
                    c.privmsg(channel, "no google results")
            except:
                c.privmsg(channel, "shit, google service unavailable")
            return

        m = re.search(r".*wikip:(.*)", msg)
        if m:
            terms = m.group(1)
            c.privmsg(channel, "looking up " + terms)
            try:
                data = google.doGoogleSearch(terms + " site:en.wikipedia.org")
                if len(data.results) > 0:
                    c.privmsg(channel, data.results[0].URL)
                else:
                    c.privmsg(channel, "no google results")
            except:
                c.privmsg(channel, "shit, google service unavailable")
            return

        m = re.search(r".*imdb:(.*)", msg)
        if m:
            terms = m.group(1)
            c.privmsg(channel, "looking up " + terms)
            try:
                data = google.doGoogleSearch(terms + " site:imdb.com")
                if len(data.results) > 0:
                    c.privmsg(channel, data.results[0].URL)
                else:
                    c.privmsg(channel, "no google results")
            except:
                c.privmsg(channel, "shit, google service unavailable")
            return

        m = re.search(r".*amazon:(.*)", msg)
        if m:
            terms = m.group(1)
            c.privmsg(channel, "looking up " + terms)
            try:
                data = google.doGoogleSearch(terms + " site:amazon.com")
                if len(data.results) > 0:
                    c.privmsg(channel, data.results[0].URL)
                else:
                    c.privmsg(channel, "no google results")
            except:
                c.privmsg(channel, "shit, google service unavailable")
            return

        m = re.search(r".*google:(.*)", msg)
        if m:
            terms = m.group(1)
            
            if random.random()<0.05:
                c.privmsg(channel, "talk to the hand")
                return
            
            c.privmsg(channel, "googling for " + terms)
            try:
                data = google.doGoogleSearch(terms)
                if len(data.results) > 0:
                    c.privmsg(channel, data.results[0].URL)
                else:
                    c.privmsg(channel, "no google results")
            except:
                c.privmsg(channel, "shit, google service unavailable")
            return

        m = re.search(r".*google10:(.*)", msg)
        if m:
            terms = m.group(1)
            c.privmsg(channel, "googling for " + terms)
            data = google.doGoogleSearch(terms)
            count = len(data.results)
            if count > 0:
                resp = "Top %d results: " % (count,)
                for i in range(count):
                    resp = "%s %d. %s  " % (resp, i+1, data.results[i].URL)
                c.privmsg(channel, resp)
            else:
                c.privmsg(channel, "no google results")
            return

        m = re.search(r".*google\+:(.*)", msg)
        if m:
            terms = m.group(1)
            c.privmsg(channel, "googling for " + terms)
            data = google.doGoogleSearch(terms)
            if len(data.results) > 0:
                c.privmsg(channel, "Google found approx. %s results for %s" % (data.meta.estimatedTotalResultsCount, terms))
                c.privmsg(channel, data.results[0].title)
                c.privmsg(channel, data.results[0].summary)
                c.privmsg(channel, data.results[0].URL)
            else:
                c.privmsg(channel, "no google results")
            return

        m = re.search(r".*google10\+:(.*)", msg)
        if m:
            terms = m.group(1)
            c.privmsg(channel, "googling for " + terms)
            data = google.doGoogleSearch(terms)
            count = len(data.results)
            if count > 0:
                c.privmsg(channel, "Google found approx. %s results for %s" % (data.meta.estimatedTotalResultsCount, terms))
                for i in range(count):
                    result = data.results[i]
                    resp = "%d. %s %s - %s" % (i+1, result.URL, result.title, result.summary)
                    c.privmsg(channel, resp)
            else:
                c.privmsg(channel, "no google results")
            return

        m = re.search(r".*spell:(.*)", msg)
        if m:
            try:
                terms = m.group(1)
                data = google.doSpellingSuggestion(terms)
                if data:
                    c.privmsg(channel, "maybe try " + data)
                else:
                    c.privmsg(channel, terms + " looks OK to me")
            except:
                c.privmsg(channel, "shit, google service unavailable")
            return
                          
        responses = ["frack", "gah!", "^8", "pfffft", "arrrr", "avast", "STFU!!11!!1", "OMGWTFBBQ!", "close but no cigar", "veet!", "ask the rhino", "I'll answer for $5", "ask someone else", "no way", "way", "if you say so...not", "if you say so", "I'm reserving judgement", "ask me later", "chya, right", "what?", "hmm?", "om", "as if", "whatever", "I agree", "no", "yes", "bite me", "I don't think so", "maybe", "I'm not sure", "super", "no comment", "sometimes", "I dunno", "almost never", "sorry, wasn't paying attention", "I doubt it", "Maybe not", "who knows?", "exactly", "in your dreams", "*sigh*", "hmmm... possibly", "yeah, OK", "meh", "lucky charms!", "ho hum", "I'm not convinced", "if you say so", "who am I to argue?", "I rather doubt that"]
        actions = ["shrugs", "blows milk out his nose", "ponders", "thinks about it", "coughs", "checks his email", "contacts the authorites", "sells out", "bites aloril", "skypes Mo", "blames teh hermit", "punches Sat", "let's one rip", "transcends", "sells it on ebay", "does a happy dance", "applauds", "appeals to authority", "weeps", "chuckles", "brings out the gimp", "farts quietly", "scoots", "hides in shadows", "levitates on a pillar of blue flame", "shuffles and kicks", "frowns", "grins", "grinaces", "grimaces", "furrows his brow", "raises both eyebrows", "snortles", "scortles", "scrotles", "hangs his head", "examines his toes", "sighs", "chuckles", "raises an eyebrow"]

        greetz = ["arrr", "ahoy", "aveet", "oi", "arrRRRrr", "hi", "hello", "hey", "heya", "greetings", "howzitgoin", "yo", "hey there", "'sup", "hola"]
        laterz = ["bye", "later", "seeya", "ciao", "so long"]
        
        if self.i_am_mentioned(c, msg) and self.is_listening(channel):
            self.delay()
            for greet in greetz:
                pat = r"\b" + greet + r"\b"
                if re.search(pat, msg):
                    c.privmsg(channel, random.choice(greetz) + " " + source)
                    return

            for later in laterz:
                pat = r"\b" + later + r"\b"
                if re.search(pat, msg):
                    c.privmsg(channel, random.choice(laterz) + " " + source)
                    return

            if random.random() < 0.2:
                c.action(channel, random.choice(actions))
            else:
                c.privmsg(channel, random.choice(responses))

    def notice_multiline(self,c,channel,msg):
        self.delay()
        for x in string.split(msg,"\n"):
            c.notice(channel, x)
            time.sleep(1)
            
    def privmsg_multiline(self,c,nick,msg):
        self.delay()
        for x in string.split(msg,"\n"):
            c.privmsg(nick, x)
            time.sleep(1)

    def do_command(self, nick, channel, cmd):
        masters = ["Lucifer", "LuciferAFK", "Hermit"]
        
        if not nick in masters:
            return random.choice(self.deepthoughts)
        
        if cmd == "die":
            self.die()
        elif cmd == "part" or cmd == "depart" or cmd == "leave":
            self.connection.part(channel)
        else:
            return random.choice(self.deepthoughts)

def main():
    import sys
    import getopt
    args = sys.argv[1:]
    optlist, args = getopt.getopt(args,'s:p:c:n:h')
    port = 6667

    channel = None
    nickname = 'Jack'
    server = 'localhost'

    for o in optlist:
        name = o[0]
        value = o[1]
        if name == '-s':
            server = value
        elif name == '-p':
            try:
                port = int(value)
            except ValueError:
                print "Error: Erroneous port."
                sys.exit(1)
        elif name == '-c':
            channel = value
        elif name == '-n':
            nickname = value

    if(channel != '' and nickname != '' and server != ''):
        bot = JackHandyBot(channel, nickname, server, port)
        bot.start()
    else:
        print "Commandline options:"
        print
        print "  -s server"
        print "  [-p port]"
        print "  -n nick"
        print "  -c channel"
        print

if __name__ == "__main__":
    main()
