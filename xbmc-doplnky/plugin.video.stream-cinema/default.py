# -*- coding: UTF-8 -*-
#/*
# *      Copyright (C) 2017 bbaron
# *
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# */

sys.path.append( os.path.join ( os.path.dirname(__file__),'resources','lib') )
sys.path.append( os.path.join ( os.path.dirname(__file__),'myprovider') )

from Plugins.Extensions.archivCZSK.archivczsk import ArchivCZSK

import re
#import util,xbmcprovider,xbmcutil
from scinema import StreamCinemaContentProvider, StreamCinemaProvider, StaticDataSC, sclog


__scriptid__   = 'plugin.video.stream-cinema'
__scriptname__ = 'stream-cinema.online'
__addon__      = ArchivCZSK.get_xbmc_addon(__scriptid__)
__language__   = __addon__.getLocalizedString
__gets         = __addon__.getSetting
__sets         = __addon__.setSetting

sclog.logDebugEnabled = __gets('debug_enabled') == 'true'

def getDeviceUid():
    uid = str(__gets('deviceid'))
    try:
        if uid.startswith('e2-'):
            if not (uid.startswith("e2-mac-") or uid.startswith("e2-rnd-")):
                return uid
        uid = ''
           
        import uuid
        # save to settings and return
        uid = 'e2-'+str(uuid.uuid4())
        __sets('deviceid', uid)
        return uid
    except:
        if uid == '':
            import random
            import string
            uid = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32))
            uid = 'e2-'+uid
            __sets('deviceid', uid)
            return uid
        pass
    __sets('deviceid', 'e2-empty')
    return 'e2-empty'
def fixXcursor():
    try:
        login = __gets('wsuser')
        pwd = __gets('wspass')
        if 'XcursorX' in login:
            login = str(login).replace('XcursorX','')
            __sets('wsuser', login)
        if 'XcursorX' in pwd:
            pwd = str(pwd).replace('XcursorX','')
            __sets('wspass', pwd)
    except:
        pass
def checkSetVIP(u, p, https):
    try:
        tmp = StaticDataSC(username=u, password=p, useHttps=https)
        __sets('wsvipdays', tmp.vipDaysLeft)
    except:
        pass


settings = {'quality':__addon__.getSetting('quality')}

reverse_eps = __gets('order-episodes') == '0'
use_https = __gets('use_https') == 'true'

# fix crazy entry by virtual keyboard
fixXcursor()
# set number of days left for VIP account
checkSetVIP(__gets('wsuser'), __gets('wspass'), use_https)



scinema = StreamCinemaContentProvider(username=__gets('wsuser'),password=__gets('wspass'), useHttps=use_https,reverse_eps=reverse_eps)
# must set again (reason: singleton)
scinema.wsuser = __gets('wsuser')
scinema.wspass = __gets('wspass')
scinema.useHttps = use_https

# must set again (reason: singleton)
scinema.deviceUid = getDeviceUid()
scinema.itemOrderGenre = __gets('item_order_genre')
scinema.itemOrderCountry = __gets('item_order_country')
scinema.itemOrderQuality = __gets('item_order_quality')
#scinema.automaticSubs = __gets('auto_subs')=='true'
scinema.langFilter = __gets('item_filter_lang')
scinema.streamSizeFilter = __gets('stream_max_size')
scinema.streamHevc3dFilter = __gets('filter_hevc_3d') == 'true'

scinema.session = session


sclog.logDebug("PARAMS=%s"%params)
StreamCinemaProvider(scinema,settings,__addon__, session).run(params)

