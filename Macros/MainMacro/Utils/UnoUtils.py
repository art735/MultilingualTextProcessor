# -*- coding: utf-8 -*-

import uno

import PyVerUtils


def show_messagebox(title, message):
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager

    if PyVerUtils.is_python2():
        toolkit = smgr.createInstance("com.sun.star.awt.Toolkit")
        parent = toolkit.getDesktopWindow()
        box_type = uno.getConstantByName("com.sun.star.awt.MessageBoxType.MESSAGEBOX")
        buttons = uno.getConstantByName("com.sun.star.awt.MessageBoxButtons.BUTTONS_OK")
        box = toolkit.createMessageBox(parent, box_type, buttons, title, message)
    else:
        from com.sun.star.awt.MessageBoxButtons import BUTTONS_OK
        from com.sun.star.awt.MessageBoxType import MESSAGEBOX

        toolkit = smgr.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)
        desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        model = desktop.getCurrentComponent()
        window = model.CurrentController.Frame.ContainerWindow
        box = toolkit.createMessageBox(window, MESSAGEBOX, BUTTONS_OK, title, message)
    # Вызов отображения коробочки за пределами if-else-блока
    box.execute()
