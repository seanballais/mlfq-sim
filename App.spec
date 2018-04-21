# -*- mode: python -*-

block_cipher = None


a = Analysis(['src/mlfq_sim/App.py'],
             pathex=['/home/seanballais/Documents/School/UPVTC/3rd Year - Second Sem/CMSC 125/MP/mlfq-sim'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='App',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
