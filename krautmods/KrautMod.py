import socket, traceback
class KrautMod(object):
	PORT 	= 6667
	SERVER 	= ""
	CHAN	= ""
	irc 	= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	nick	= ""
	oBuff 	= ""

	"""docstring for KrautMod"""
	def __init__(self, nick="krautbot", chan="#krautbot", SERVER="irc.freenode.net"):
		super(KrautMod, self).__init__()
		self.nick 	= nick
		self.chan 	= chan
		self.SERVER = SERVER
		try:
			self.connect()
			self.IRCinit()
			self.RecvData()
		except:
			traceback.print_exc()

	def connect(self):
		connectionObject = self.irc.connect((self.SERVER, self.PORT))
		return connectionObject

	def IRCinit(self):
		self.irc.recv(4096)
		self.irc.send(self.UTF8enc("NICK " + str(self.nick) + "\r\n"))
		self.irc.send(self.UTF8enc("USER krautbot krautbot krautbot :kraut IRC \r\n")) 
		self.irc.send(self.UTF8enc("JOIN " + str(self.chan) + "\r\n"))
		self.irc.send(self.UTF8enc("PRIVMSG "+ str(self.chan) + ":Hello \r\n"))

	def UTF8enc(self, string):
		return string.encode("UTF-8")

	def UTF8dec(self, dec):
		return dec.decode("UTF-8")

	def RecvData(self):
		readbuffer = ""
		while True:
			readbuffer = readbuffer + self.irc.recv(4096).decode("UTF-8")
			temp = str.split(readbuffer, "\n")
			readbuffer = temp.pop()
			for line in temp:
				print(line)
				line = str.rstrip(line)
				line = str.split(line)
				print("LIST:"+str(line))
				# Krauty plays PING PONG with the server here
				self.KeepAlive(line)


	def KeepAlive(self, ircOutputLine):
		if(ircOutputLine[0] == "PING" ):
			print("PONG MOTHAFUCKA!!!")
			self.irc.send(bytes("PONG %s\r\n" % ircOutputLine[1], "UTF-8"))
			return 1
		return 0
	