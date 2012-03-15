#!/usr/bin/env python

import ConfigParser
from os import environ, path, mkdir
import i18n

class ConfPacupdate:

    pacman_conf_dir = environ['HOME'] + '/.config/'
    pacupdate_conf_file = pacman_conf_dir + 'pacupdate.conf'

    conf_options = [['update_interval', '60'],
                    ['notification_delay', '10']]


    def directoryExists(self, dir):
        if path.isdir(dir):
            return True
        else:
            return False

    def fileExists(self, file):
        if path.isfile(file):
            return True
        else:
            return False

    def createDefaultConf(self):
        if self.directoryExists(self.pacman_conf_dir):

            config = ConfigParser.ConfigParser()
            config.add_section('global')
            config.set('global','update_interval', 60)
            config.set('global','notification_delay', 10)

            try:
                pacupdate_conf_parser = open(self.pacupdate_conf_file,'w')
                config.write(pacupdate_conf_parser)
                pacupdate_conf_parser.close()

                print _('pacupdate default configuration created.')
                return True
            except:
                print _('Could not save your pacupdate configuration.')
                return False

        else:
            
            try:
                mkdir(self.pacman_conf_dir)
                print _('pacupdate directory (%s) created.') % self.pacman_conf_dir
                self.__init__()
                
            except:
                print _('Could not create pacupdate default configuration.')

    def writeConf(self, interval, delay):
        
        if self.fileExists(self.pacupdate_conf_file):

            config = ConfigParser.ConfigParser()
            config.add_section('global')
            config.set('global','update_interval', interval)
            config.set('global','notification_delay', delay)

            try:                
                pacupdate_conf_parser = open(self.pacupdate_conf_file,'w')
                config.write(pacupdate_conf_parser)
                pacupdate_conf_parser.close()

                print _('pacupdate configuration saved.')
                
            except:                
                print _('Could not save your pacupdate configuration.')


    def readConf(self):
        '''
		Read pacupdate.conf file and return config options
		'''
        try:
            if self.fileExists:
                
                config = ConfigParser.ConfigParser()
                config.read(self.pacupdate_conf_file)
                return config
            
            else:
                
                self.createDefaultConf()
                self.readConf()
                
        except:
            
            print _('There is a problem with your config file. Please, remove %s.') % self.pacupdate_conf_file

    def __init__(self):

        if not self.fileExists(self.pacupdate_conf_file):
            self.createDefaultConf()