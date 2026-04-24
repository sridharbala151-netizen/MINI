[buildozer]
title = Bill Generator
package.name = billgenerator
package.domain = org.example
version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.accept_sdk_license = True
android.allow_backup = True

# Source files
source.include_exts = py,json,png

# Keep original directory structure
presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png