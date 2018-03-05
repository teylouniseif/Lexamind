#! python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 15:45:54 2018
@author: Saif Kurdi-Teylouni
"""

import execnet

def call_python_version(Version, Module, Function, ArgumentList):
    gw      = execnet.makegateway("popen//py -%s" % Version)
    channel = gw.remote_exec("""
        from %s import %s as the_function
        channel.send(the_function(*channel.receive()))
    """ % (Module, Function))
    #channel.send(ArgumentList)
    channel.send(ArgumentList)
    return channel.receive()
