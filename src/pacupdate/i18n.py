# -*- coding: utf-8 -*-

program = 'pacupdate'

import locale
LC_ALL = locale.setlocale(locale.LC_ALL, '')

import gettext
from gettext import gettext as _, ngettext
gettext.install(program, unicode=True)
gettext.textdomain(program)
