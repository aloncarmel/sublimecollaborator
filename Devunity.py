import sublime, sublime_plugin, urllib, urllib2
import json, pprint, os, threading

class DevunityCommand(sublime_plugin.TextCommand):

	settings = sublime.load_settings('Devunity.sublime-settings')

	userid = settings.get('userid')

	activeedit = 0

	def run(self, edit):

		self.activeedit = edit

		sublime.active_window().show_input_panel('Enter email addresses to share with, comma seperated', 'dev@mycompany.com', self.on_done, None, None)
		#self.on_done('test')

	def on_done(self, username):

		DevunitySendCode(self.activeedit).sharecodeprep(self.view, username, self.activeedit)


class DevunitySendCode(sublime_plugin.TextCommand):

	settings = sublime.load_settings('Devunity.sublime-settings')

	userid = settings.get('userid')

	def run(self, edit):
		pass

	@classmethod	
	def sharecodeprep(self, activeview, username, edit):

		sels = activeview.sel()

		for sel in sels:
			code = activeview.substr(sel)

			DevunitySendCode(self).sharecode(username, code, activeview, sel.end(), sel.begin(), edit)

	@classmethod
	def sharecode(self, username, code, activeview, selend, selbegin, edit):
		try:  
			if activeview.file_name():
				fileName, fileExtension = os.path.splitext(activeview.file_name())
			else:
				fileName, fileExtension = os.path.splitext('untitled.txt')

			data = urllib.urlencode({'code': code,'authorid': self.userid, 'members': username, 'filepath': activeview.file_name(), 'extension': fileExtension})  

			request = urllib2.Request('http://dev.watercooler.io/v1/code/post', data, headers={"User-Agent": "Sublime Devunity"})
			http_file = urllib2.urlopen(request, timeout=30).read()

			response = json.loads(http_file)
			for case in switch(fileExtension):
			    if case('.py'):

					activeview.insert(edit, selbegin, '\n# Start Collaboration url: http:///dev.devunity.com/code/'+str(response)+'\n')	
					activeview.insert(edit, selend, '\n# End collaboration code')	

					break
			    if case('.php'):

					activeview.insert(edit, selbegin, '\n// Collaboration url: http:///dev.devunity.com/code/'+str(response)+'\n')	
					activeview.insert(edit, selend, '\n// End collaboration code\n')	

					break
			    if case('.html'):
					activeview.insert(edit, selbegin, '\n<!-- Collaboration url: http:///dev.devunity.com/code/'+str(response)+'-->\n')	
					activeview.insert(edit, selend, '\n<!-- End collaboration code\n')	

					break
			    if case('.js'):
					activeview.insert(edit, selbegin, '\n// Collaboration url: http:///dev.devunity.com/code/'+str(response)+'\n')	
					activeview.insert(edit, selend, '\n// End collaboration code\n')	

					break
			    if case('.c'):
					activeview.insert(edit, selbegin, '\n/* Collaboration url: http:///dev.devunity.com/code/'+str(response)+' */\n')	
					activeview.insert(edit, selend, '\n/* End collaboration code */\n')	

					break
			    if case('.h'):
					activeview.insert(edit, selbegin, '\n/* Collaboration url: http:///dev.devunity.com/code/'+str(response)+' */\n')	
					activeview.insert(edit, selend, '\n/* End collaboration code */\n')	

					break
			    if case('.jsp'):
					activeview.insert(edit, selbegin, '\n/* Collaboration url: http:///dev.devunity.com/code/'+str(response)+' */\n')	
					activeview.insert(edit, selend, '\n/* End collaboration code */\n')	

					break
			    if case('.txt'):
					activeview.insert(edit, selbegin, '\n# Collaboration url: http:///dev.devunity.com/code/'+str(response)+'\n')	
					activeview.insert(edit, selend, '\n# End collaboration code */\n')	

					break
			    if case('.pl'):
					activeview.insert(edit, selbegin, '\n# Collaboration url: http:///dev.devunity.com/code/'+str(response)+'\n')	
					activeview.insert(edit, selend, '\n# End collaboration code\n')	

					break
			    if case('.rc'):
					activeview.insert(edit, selbegin, '\n# Collaboration url: http:///dev.devunity.com/code/'+str(response)+'\n')	
					activeview.insert(edit, selend, '\n# End collaboration code\n')	

					break
			    if case(): # default, could also just omit condition or 'if True'
					activeview.insert(edit, selbegin, '\n# Collaboration url: http:///dev.devunity.com/code/'+str(response)+'\n')	
					activeview.insert(edit, selend, '\n# End collaboration code\n')

			        # No need to break here, it'll stop anyway

			#sublime.message_dialog('Your collaboration url is: \nUrl: http:///dev.devunity.com/code/'+str(response)+'\nInvited: '+username)
			#sublime.status_message('Your collaboration url is: \nUrl: http:///dev.devunity.com/code/'+str(response)+'\nInvited: '+username)

			return
		except (urllib2.HTTPError) as (e):  
			    err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))  
		except (urllib2.URLError) as (e):  
			    err = '%s: URL error %s contacting API' % (__name__, str(e.reason))  
			    sublime.error_message(err)  
			    self.result = False 


class DevunityEventListener(sublime_plugin.EventListener):

	settings = sublime.load_settings('Devunity.sublime-settings')

	userid = settings.get('userid')

	def on_post_save(self, view):
        #print view.file_name()#
        #sublime.active_window().show_input_panel('Enter Devunity @username to share with, comma seperated', '@someone', None, None, None)
		pass

	def on_modified(self, view):
        #print view.file_name()
		self.settings.set('crap','test')

	def on_selection_modified(self, view):
    	#print view.sel()[0].end()
    	#sublime.status_message('Updating!')
    	#view.insert(view, self.end(), 'kaka')
    	#activewindow = view.window()
    	#activewindow.new_file()
		pass

	def createfile(self, activewindow, codeid , codestr, waitingid):

		threads = []
		thread = WaitingListDelete(waitingid)
		threads.append(thread)
		thread.start()

		newfile = activewindow.new_file()
		edit = newfile.begin_edit('devunity')
		newfile.insert(edit, 0, str(codestr))
		newfile.end_edit(edit)
		

	def on_load(self, view):
    	#print str(view.sel()[0].begin())+'-'+str(view.sel()[0].end())
    	#print view.file_name()
    	#edit = view.begin_edit('devunity')

    	
    	#print edit
    	#view.end_edit(edit)
		CheckCodeWaiting().opencode(view, self.userid)


	def on_post_save(self, view):
    	#print str(view.sel()[0].begin())+'-'+str(view.sel()[0].end())
    	#print view.file_name()
    	#edit = view.begin_edit('devunity')

    	
    	#print edit
    	#view.e
		CheckCodeWaiting().opencode(view, self.userid)
		


class CheckCodeWaiting():

	def opencode(self, view, userid):

		try:
			
			data = urllib.urlencode({'authorid': userid})  
			request = urllib2.Request('http://dev.watercooler.io/v1/code/pending', data, headers={"User-Agent": "Sublime Devunity"})
			http_file = urllib2.urlopen(request, timeout=30).read()
			activewindow = view.window()
			response = json.loads(http_file)

			for code in response:

				sublime.set_timeout(DevunityEventListener().createfile(activewindow, code['codeid'], code['code'], code['waitingid']), 300)

			
			return
		except (urllib2.HTTPError) as (e):  
			    err = '%s: HTTP error %s contacting API' % (__name__, str(e.code))  
		except (urllib2.URLError) as (e):  
			    err = '%s: URL error %s contacting API' % (__name__, str(e.reason))  
			    sublime.error_message(err)  
			    self.result = False

class WaitingListDelete(threading.Thread):
    def __init__(self, waitingid):
       
        self.waitingid = waitingid
        threading.Thread.__init__(self)

    def run(self):

		data = urllib.urlencode({'id': self.waitingid})
		request = urllib2.Request('http://dev.watercooler.io/v1/waitinglist/delete', data, headers={"User-Agent": "Sublime Devunity"})
		http_file = urllib2.urlopen(request, timeout=30).read()
		response = json.loads(http_file)
		#self.activeview.focus_view(self.newfileview)
		#view.insert(newfile, 0, 'kaka')

		print response

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
    
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False