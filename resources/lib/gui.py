import sys
import os
import xbmc
import xbmcgui
import urllib
from Dilmaj import Dilmaj 
import socket

_              = sys.modules[ "__main__" ].__language__
__scriptname__ = sys.modules[ "__main__" ].__scriptname__
__version__    = sys.modules[ "__main__" ].__version__
__addon__      = sys.modules[ "__main__" ].__addon__


STATUS_LABEL   = 100
EDIT_BOX       = 122
SEARCH_BUTTON  = 123
LABLE_BOX = 124

CANCEL_DIALOG  = ( 9, 10, 92, 216, 247, 257, 275, 61467, 61448, )

class GUI( xbmcgui.WindowXMLDialog ):
    
    def __init__( self, *args, **kwargs ):       
      pass

    def onInit( self ):  
      self.setup_all()

    def _get_urlopener(self):
      urlopener = _FancyURLopener(__addon__.getSetting( "user" ), __addon__.getSetting( "pass" ))
      self.getControl( STATUS_LABEL ).setLabel( _(610) + "...")
      urlopener.addheaders = [('User-agent', "urllib/1.0 (urllib)")]
      return urlopener

    def setup_all( self ):
      self.setFocus( self.getControl( EDIT_BOX ) )
      self.getControl( STATUS_LABEL ).setLabel( _(614) ) 
     
      socket.setdefaulttimeout(None)
    
    def onClick( self, controlId ):
      if( controlId == SEARCH_BUTTON ) :
        search_word = self.getControl(EDIT_BOX).getText()
        self.getControl( STATUS_LABEL ).setLabel( _(613) )
        dictionary = Dilmaj()
        dictionary_result = dictionary.search(search_word)
        
        self.getControl( LABLE_BOX ).setLabel(dictionary_result)
        self.getControl( STATUS_LABEL ).setLabel( _(614) )
        
    def onFocus( self, controlId ):
      self.controlId = controlId

    def onAction( self, action ):
      if ( action.getId() in CANCEL_DIALOG):
        self.close()
