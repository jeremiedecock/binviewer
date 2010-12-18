.PHONY: debian clean

dist: tarball debian

tarball: 
	tar -czvf binviewer.tar.gz *

debian: binviewer.deb
	
binviewer.deb: binviewer.py
	mkdir -p        debian/usr/bin
	cp binviewer.py debian/usr/bin/binviewer
	chmod 755       debian/usr/bin/binviewer
	
	mkdir -p        debian/usr/share/doc/binviewer/
	cp COPYING      debian/usr/share/doc/binviewer/copyright
	chmod 644       debian/usr/share/doc/binviewer/copyright
	
	mkdir -p debian/DEBIAN
	echo "Package: binviewer"                                              >  debian/DEBIAN/control
	echo "Version: 0.1"                                                    >> debian/DEBIAN/control
	echo "Section: utils"                                                  >> debian/DEBIAN/control # list : http://packages.debian.org/stable/
	echo "Priority: optional"                                              >> debian/DEBIAN/control
	echo "Maintainer: Jérémie DECOCK <gremy@tuxfamily.org>"                >> debian/DEBIAN/control
	echo "Architecture: all"                                               >> debian/DEBIAN/control
	echo "Depends: python (>= 2.5)"                                        >> debian/DEBIAN/control
	echo "Description: Create a graphical representation of a binary file" >> debian/DEBIAN/control
	fakeroot dpkg-deb -b debian

	mv debian.deb binviewer_0.1_all.deb

clean:
	rm -rf debian

init: clean
	rm -f  binviewer_0.1_all.deb
	rm -f  binviewer.tar.gz

