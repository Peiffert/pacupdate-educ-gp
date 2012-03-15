#!/usr/bin/env python

from distutils.core import setup
import glob

images = glob.glob('src/img/*')
dfiles = ['LICENSE','README','ChangeLog','AUTHORS','TODO']

setup(name='Pacupdate',
      version='0.1',
      license='GPL2',
      description='a systray application that notifies that user about new updates for Arch Linux',
      author=['Hugo Doria','Kessia Pinheiro'],
      author_email=['hugo@archlinux.org','kessia@archlinux-br.org'],
      url='http://code.google.com/p/pacupdate/',
      package_dir={'pacupdate':'src/pacupdate'},
      packages=['pacupdate'],
      data_files=[('share/pacupdate/img', images),
                  ('share/pacupdate/', dfiles),
                  ('share/applications', ['pacupdate.desktop']),
                  ],
      scripts=['src/scripts/pacupdate']
)

