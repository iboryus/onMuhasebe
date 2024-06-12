import win32gui
import win32api
import win32con
import win32process 
import pyautogui
import pyperclip

def getHandle():
    handle=[]
    def enumHandler(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            if "Firefox" in win32gui.GetWindowText(hwnd):
                print(win32gui.GetWindowText(hwnd))
                print(hwnd)
                handle.append(hwnd)
    win32gui.EnumWindows(enumHandler, None)
    return handle[0] if handle else None

def readTitles(fname):
    titles=[]
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        titles = ''.join(f.readlines()).split('\n')
    return titles

handle=getHandle()
print(handle)

firma_adi="Betmetre"
if handle is not None:
    print("working")
    win32gui.SetForegroundWindow(handle)
    remote_thread, _ = win32process.GetWindowThreadProcessId(handle)
    win32process.AttachThreadInput(win32api.GetCurrentThreadId(), remote_thread, True)
    win32gui.SetFocus(handle)
    titles=readTitles('titles.txt')
 
    # with pyautogui.hold("ctrl"):
    #     pyautogui.press(str(i))
    pyautogui.hotkey("ctrl", "1")
    win32gui.SetFocus(handle)

    for i in range(0,len(titles)):
        title=titles[i]
        print(i+1)
        win32api.Sleep(200)

        pyperclip.copy(firma_adi+" "+title)
        print(firma_adi+" "+title)

        # win32api.Sleep(100)
        # pyautogui.hotkey('f6')
        win32api.Sleep(100)
        pyautogui.hotkey('ctrl', 'v')
        win32api.Sleep(100)
        with pyautogui.hold("ctrl"):
            pyautogui.press("pagedown")
