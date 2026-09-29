# -*- coding: utf-8 -*-
import uno
import os
import subprocess

def show_messagebox(title, message):
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    toolkit = smgr.createInstance("com.sun.star.awt.Toolkit")
    parent = toolkit.getDesktopWindow()

    box_type = uno.getConstantByName("com.sun.star.awt.MessageBoxType.MESSAGEBOX")
    buttons = uno.getConstantByName("com.sun.star.awt.MessageBoxButtons.BUTTONS_OK")

    box = toolkit.createMessageBox(parent, box_type, buttons, title, message)
    box.execute()

def run_python3_script():
    python3_path = r"C:\Program Files\Python311\python.exe"
    script_path = r"C:\Users\user\AppData\Roaming\OpenOffice\4\user\Scripts\python\say_hello.py"
    method_name = "hello_world"

    try:
        env = os.environ.copy()
        env.pop("PYTHONHOME", None)
        env.pop("PYTHONPATH", None)
        env["PYTHONIOENCODING"] = "utf-8"

        process = subprocess.Popen(
            [python3_path, script_path, method_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env
        )

        stdout, stderr = process.communicate()
        stdout = stdout.decode('utf-8').strip()
        stderr = stderr.decode('utf-8').strip()

        show_messagebox("Result", stdout if stdout else stderr)

    except Exception as e:
        show_messagebox("Error", unicode(str(e), 'utf-8') if isinstance(e, str) else str(e))
