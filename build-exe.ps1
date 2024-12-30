# This wraps PyPostNote into an executable file.

$arguments = 'cli.py',
             '-w',
             '--noconfirm',
			 '--clean',
			 '--name',
			 'PyLogBook',
			 '--icon',
			 'Resources/PyLogBook.ico',
			 '--add-binary',
			 'Resources/Bold.png;Resources',
			 '--add-binary',
			 'Resources/Bullet Table.png;Resources',
			 '--add-binary',
			 'Resources/Center.png;Resources',
			 '--add-binary',
			 'Resources/Italic.png;Resources',
			 '--add-binary',
			 'Resources/Left.png;Resources',
			 '--add-binary',
			 'Resources/minus.png;Resources',
			 '--add-binary',
			 'Resources/No Color.png;Resources',
			 '--add-binary',
			 'Resources/Number Table.png;Resources',
			 '--add-binary',
			 'Resources/pencil.png;Resources',
			 '--add-binary',
			 'Resources/plus.png;Resources',
			 '--add-binary',
			 'Resources/Right.png;Resources',
			 '--add-binary',
			 'Resources/Text Background.png;Resources',
			 '--add-binary',
			 'Resources/Text Foreground.png;Resources',
			 '--add-binary',
			 'Resources/Underline.png;Resources'

pyinstaller $arguments 2>&1 > .\pyinstaller-build.log