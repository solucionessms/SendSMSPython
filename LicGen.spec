# -*- mode: python -*-
a = Analysis(['licconfig.py'],
             pathex=['C:\\Users\\Administrador\\Desktop\\AlertSMS 0.7'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='LicGen.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
