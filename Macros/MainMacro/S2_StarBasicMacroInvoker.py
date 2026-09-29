# -*- coding: utf-8 -*-
import uno

# Перед вызовом StarBasic-макроса, закомментировать в нём вызов данного Python-макроса, чтобы не было
# бесконечного цикла и краша системы.
def invoke():
    ctx = uno.getComponentContext()
    serviceManager = ctx.ServiceManager
    dispatchHelper = serviceManager.createInstanceWithContext("com.sun.star.frame.DispatchHelper", ctx)
    desktop = serviceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
    sMacroURL = "macro:///standard.GreekModule.Main"

    dispatchHelper.executeDispatch(desktop, sMacroURL, '', 0, tuple([]))

    return
