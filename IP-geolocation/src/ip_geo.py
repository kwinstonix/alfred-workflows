#!/usr/bin/env python
# encoding: utf-8

import sys
import re
import json
import urllib
from workflow import Workflow


def taobao_api(ip=''):
    '''
    '''
    url = "http://ip.taobao.com/service/getIpInfo.php?ip=%s" % ip
    json_keys = ('isp', 'city', 'region', 'country')
    desc = []
    reply_dict = []
    try:
        ret_str = urllib.urlopen(url).read()
        reply_dict = json.loads(ret_str)
    except:
        print 'json decode error: %s' % ret_str
        return None
    for key in json_keys:
        item = reply_dict['data'].get(key)
        if item :
            desc.append(item)
    return u' | '.join(desc)


def ipinfo_io(ip=''):
    '''
    '''
    url = "http://ipinfo.io/%s/json" % ip
    json_keys = ('org', 'city', 'region', 'country')
    desc = []
    reply_dict = []
    try:
        ret_str = urllib.urlopen(url).read()
        reply_dict = json.loads(ret_str)
    except:
        print 'json decode error: %s' % ret_str
        return None
    for key in json_keys:
        item = reply_dict.get(key)
        if item :
            desc.append(item)
    return u' | '.join(desc)

def freegeoip_net(ip=''):
    '''
    '''
    desc = []
    reply_dict = []
    json_keys = ('city', 'region_name', 'country_name')
    url = "http://freegeoip.net/json/%s" % ip
    try:
        ret_str = urllib.urlopen(url).read()
        reply_dict = json.loads(ret_str)
    except:
        print 'json decode error: %s' % ret_str
        return None
    for key_name in json_keys:
        item = reply_dict[key_name]
        if item :
            desc.append(item)
    return u' | '.join(desc)

def main(wf):
    # Get args from Workflow, already in normalized Unicode
    args = wf.args

    ip = args[0].strip()
    #check ipaddr
    if not re.match('^([0-9]{1,3}\.){3}[0-9]{1,3}$', ip):
        return None
    # Add an item to Alfred feedback
    taobao_ret = taobao_api(ip)
    ipinfo_ret = ipinfo_io(ip)
    freegeoip_ret = freegeoip_net(ip)

    wf.add_item(title=u'ip.taobao:', subtitle=taobao_ret, icon='ip_taobao.jpg')
    wf.add_item(title=u'ipinfo.io:', subtitle=ipinfo_ret, icon='ipinfo_log.jpg')
    wf.add_item(title=u'freegeoip.net:', subtitle=freegeoip_ret, icon='freegoip.net_favicon.ico')

    # Send output to Alfred. You can only call this once.
    wf.send_feedback()

if __name__ == '__main__':
    # Create a global `Workflow` object
    wf = Workflow()
    sys.exit(wf.run(main))
