from xml.etree import ElementTree
from os.path import expanduser
import os, sys
__cwd__ = sys.modules[ "__main__" ].__cwd__

class Dilmaj():
    
    def __init__(self):
        home = expanduser('~')
        self.EnglishToPersian = self.ConvertXmlToDict(__cwd__ + '/resources/lib/generic.xdb')
    def search(self, search):
        word = self.word_search(search)
        return word
	
    def word_search(self,search):
        try:
            word = ""
            print "Searching Word " + search

            for resualt in self.EnglishToPersian['words']['word']:
                if resualt['in'] == search:
                    word = resualt['out'] 		 
           
            return word

        except ():
            print "Error : Word Not Found!"
            return "Word Not Found!"
            
            
    class XmlDictObject(dict):
			"""
			Adds object like functionality to the standard dictionary.
			"""

			def __init__(self, initdict=None):
				if initdict is None:
					initdict = {}
				dict.__init__(self, initdict)

			def __getattr__(self, item):
				return self.__getitem__(item)

			def __setattr__(self, item, value):
				self.__setitem__(item, value)

			def __str__(self):
				if self.has_key('_text'):
					return self.__getitem__('_text')
				else:
					return ''

			@staticmethod
			def Wrap(x):
				"""
				Static method to wrap a dictionary recursively as an XmlDictObject
				"""

				if isinstance(x, dict):
					return XmlDictObject((k, XmlDictObject.Wrap(v)) for (k, v) in x.iteritems())
				elif isinstance(x, list):
					return [XmlDictObject.Wrap(v) for v in x]
				else:
					return x

			@staticmethod
			def _UnWrap(x):
				if isinstance(x, dict):
					return dict((k, XmlDictObject._UnWrap(v)) for (k, v) in x.iteritems())
				elif isinstance(x, list):
					return [XmlDictObject._UnWrap(v) for v in x]
				else:
					return x
				
			def UnWrap(self):
				"""
				Recursively converts an XmlDictObject to a standard dictionary and returns the result.
				"""

				return XmlDictObject._UnWrap(self)


    def _ConvertXmlToDictRecurse(self, node, dictclass):
			nodedict = dictclass()
			
			if len(node.items()) > 0:
				# if we have attributes, set them
				nodedict.update(dict(node.items()))
			
			for child in node:
				# recursively add the element's children
				newitem = self._ConvertXmlToDictRecurse(child, dictclass)
				if nodedict.has_key(child.tag):
					# found duplicate tag, force a list
					if type(nodedict[child.tag]) is type([]):
						# append to existing list
						nodedict[child.tag].append(newitem)
					else:
						# convert to list
						nodedict[child.tag] = [nodedict[child.tag], newitem]
				else:
					# only one, directly set the dictionary
					nodedict[child.tag] = newitem

			if node.text is None: 
				text = ''
			else: 
				text = node.text.strip()
			
			if len(nodedict) > 0:            
				# if we have a dictionary add the text as a dictionary value (if there is any)
				if len(text) > 0:
					nodedict['_text'] = text
			else:
				# if we don't have child nodes or attributes, just set the text
				nodedict = text
				
			return nodedict
			
    def ConvertXmlToDict(self, root, dictclass=XmlDictObject):
			"""
			Converts an XML file or ElementTree Element to a dictionary
			"""

			# If a string is passed in, try to open it as a file
			if type(root) == type(''):
				root = ElementTree.parse(root).getroot()
			elif not isinstance(root, ElementTree.Element):
				raise TypeError, 'Expected ElementTree.Element or file path string'

			return dictclass({root.tag: self._ConvertXmlToDictRecurse(root, dictclass)})

