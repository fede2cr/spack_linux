Name:        mozilla
Summary:     Web browser and mail reader
Version:     0.9.1
Release:     0
Serial:      20
Copyright:   MPL
Source0:     mozilla-source-0.9.1.tar.bz2
Source1:     mozilla.sh
Source2:     mozilla-icon.png
Source3:     migrate-icon.gif
Source4:     mozilla.desktop
Source5:     mozilla-profile.desktop
Source6:     mozilla-ns-upgrade.desktop
Source7:     mozilla-make-package.pl
Source8:     mozilla-copy-package-files.sh
Source9:     mozicon16.xpm
Source10:    mozicon50.xpm
Source11:    rebuild-databases.sh
Patch0:      mozilla-navigator-overlay-menu.patch
Patch1:      mozilla-editor-overlay-menu.patch
Patch6:      mozilla-prefs-debug.patch
Patch7:      mozilla-redhat-home-page.patch
Patch8:      mozilla-redhat-mail-home-page.patch
Patch9:      mozilla-alpha-compiler.patch
Patch10:     mozilla-redhat-home-page-6.2.patch
Patch11:     mozilla-taskbar-nomozilla.patch
Buildroot:   /var/tmp/mozilla-root
Prefix:      /opt/gnome
Group:       Applications/Internet
Provides:    webclient
BuildPrereq: libpng-devel, libjpeg-devel, zlib-devel, zip, perl, autoconf, indexhtml, ORBit-devel, glib-devel, gtk+-devel
ExcludeArch: ia64
Prereq:      fileutils

%description
Mozilla is an open-source web browser, designed for standards
compliance, performance and portability.

%package devel
Summary: Development files for Mozilla
Group: Development/Libraries

%description devel
Development header files for mozilla.

%package mail
Summary: Mozilla-based mail system
Group: Applications/Internet
Prereq:      fileutils mozilla = %{version}-%{release}

%description mail
Mail/news client based on the Mozilla web browser.  The mail/news
client supports IMAP, POP, and NNTP and has an easy to use interface.

%package psm
Summary: SSL support for Mozilla.
Group: Applications/Internet
Prereq:      fileutils mozilla = %{version}-%{release}

%description psm
SSL support for Mozilla.

%package chat
Summary: IRC client integrated with Mozilla
Group: Applications/Internet
Prereq: fileutils mozilla = %{version}-%{release}

%description chat
IRC client that is integrated with the Mozilla web browser.

%prep

%setup -q -n mozilla

%patch0 -p1
%patch0 -p1 -R

%patch1 -p1
%patch1 -p1 -R

%patch6 -p1
%patch6 -p1 -R

## is it a RH 7.0 system?
#if [ -f /usr/share/doc/HTML/index.html ]; then
#%patch7 -p1
#%patch7 -p1 -R
#else
#%patch10 -p1
#%patch10 -p1 -R
#fi

#%patch8 -p1
#%patch8 -p1 -R

#%patch9 -p1 -b .alpha-compiler

%patch11 -p1
%patch11 -p1 -R

%build

if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
if test "x$CPUS" = "x" -o "x$CPUS" = "x0"; then
  CPUS=1
fi

# build mozilla
BUILD_OFFICIAL=1 ./configure --prefix=%{_prefix} --enable-optimize \
	--disable-debug \
	--with-default-mozilla-five-home=/opt/gnome/lib/mozilla \
	--enable-strip-libs --disable-tests --disable-short-wchar \
	--enable-nspr-autoconf --with-extensions --without-mng \
	--enable-crypto

#BUILD_OFFICIAL=1 make -j$CPUS -s export
#BUILD_OFFICIAL=1 make -j$CPUS -s install
BUILD_OFFICIAL=1 make -s

%install
/bin/rm -rf $RPM_BUILD_ROOT
/bin/mkdir -p $RPM_BUILD_ROOT/%{prefix}/lib/mozilla
/bin/mkdir -p $RPM_BUILD_ROOT/%{prefix}/bin
/bin/mkdir -p $RPM_BUILD_ROOT/%{prefix}/include/mozilla/idl

# create a list of all of the different package and the files that
# will hold them

# build all of the default browser components
/bin/rm -f /tmp/mozilla.list
/bin/rm -f /tmp/mozilla.list.shared
/bin/rm -f /tmp/mozilla.package
%{SOURCE7} --package langenus --output-file /tmp/mozilla.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --source $RPM_BUILD_DIR/mozilla/dist
%{SOURCE7} --package langenus --output-file /tmp/mozilla.list.shared \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --source $RPM_BUILD_DIR/mozilla/dist -shared

%{SOURCE7} --package regus --output-file /tmp/mozilla.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --source $RPM_BUILD_DIR/mozilla/dist
%{SOURCE7} --package regus --output-file /tmp/mozilla.list.shared \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --source $RPM_BUILD_DIR/mozilla/dist --shared

%{SOURCE7} --package deflenus --output-file /tmp/mozilla.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --source $RPM_BUILD_DIR/mozilla/dist
%{SOURCE7} --package deflenus --output-file /tmp/mozilla.list.shared \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --source $RPM_BUILD_DIR/mozilla/dist

%{SOURCE7} --package xpcom --output-file /tmp/mozilla.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --source $RPM_BUILD_DIR/mozilla/dist
%{SOURCE7} --package xpcom --output-file /tmp/mozilla.list.shared \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --source $RPM_BUILD_DIR/mozilla/dist --shared

%{SOURCE7} --package browser --output-file /tmp/mozilla.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --source $RPM_BUILD_DIR/mozilla/dist
%{SOURCE7} --package browser --output-file /tmp/mozilla.list.shared \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --source $RPM_BUILD_DIR/mozilla/dist --shared

/bin/rm -f /tmp/mozilla-mail.list
/bin/rm -f /tmp/mozilla-mail.list.shared
/bin/rm -f /tmp/mozilla-mail.package
%{SOURCE7} --package mail --output-file /tmp/mozilla-mail.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --source $RPM_BUILD_DIR/mozilla/dist
%{SOURCE7} --package mail --output-file /tmp/mozilla-mail.list.shared \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --source $RPM_BUILD_DIR/mozilla/dist --shared

/bin/rm -f /tmp/mozilla-psm.list
/bin/rm -f /tmp/mozilla-psm.list.shared
/bin/rm -f /tmp/mozilla-psm.package
%{SOURCE7} --package psm --output-file /tmp/mozilla-psm.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --source $RPM_BUILD_DIR/mozilla/dist


# we don't actually build the shared list since the only one in the
# package, libnssckbi.so, needs to be in /usr/lib/mozilla because it's
# loaded by hand.  Just throw it into the regular list.

echo libnssckbi.so >> /tmp/mozilla-psm.list

#%{SOURCE7} --package psm --output-file /tmp/mozilla-psm.list.shared \
#    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
#    --source $RPM_BUILD_DIR/mozilla/dist --shared

/bin/rm -f /tmp/mozilla-chat.list
/bin/rm -f /tmp/mozilla-chat.list.shared
/bin/rm -f /tmp/mozilla-chat.package
%{SOURCE7} --package chatzilla --output-file /tmp/mozilla-chat.list \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --source $RPM_BUILD_DIR/mozilla/dist
%{SOURCE7} --package chatzilla --output-file /tmp/mozilla-chat.list.shared \
    --package-file $RPM_BUILD_DIR/mozilla/xpinstall/packager/packages-unix \
    --source $RPM_BUILD_DIR/mozilla/dist --shared

# copy all of the files
%{SOURCE8} /tmp/mozilla.list /tmp/mozilla.package \
    $RPM_BUILD_ROOT/%{prefix}/lib/mozilla \
    $RPM_BUILD_DIR/mozilla/dist/bin \
    %{prefix}/lib/mozilla
%{SOURCE8} /tmp/mozilla.list.shared /tmp/mozilla.package \
    $RPM_BUILD_ROOT/%{prefix}/lib \
    $RPM_BUILD_DIR/mozilla/dist/bin \
    %{prefix}/lib

# build our initial component and chrome registry
# we don't need to do this anymore

pushd `pwd`
  cd $RPM_BUILD_ROOT/%{prefix}/lib/mozilla
  # register our components
  LD_LIBRARY_PATH=`pwd`:`pwd`/.. MOZILLA_FIVE_HOME=`pwd` ./regxpcom
  # set up the default skin and locale to trigger the generation of
  # the user-locales and users-skins.rdf
  echo "skin,install,select,classic/1.0" >> chrome/installed-chrome.txt
  echo "locale,install,select,en-US" >> chrome/installed-chrome.txt
  # set up the chrome rdf files
  LD_LIBRARY_PATH=`pwd`:`pwd`/.. MOZILLA_FIVE_HOME=`pwd` ./regchrome
  # fix permissions of the chrome directories
  /usr/bin/find . -type d -perm 0700 -exec chmod 755 {} \; || :
popd

%{SOURCE8} /tmp/mozilla-mail.list /tmp/mozilla-mail.package \
    $RPM_BUILD_ROOT/%{prefix}/lib/mozilla \
    $RPM_BUILD_DIR/mozilla/dist/bin \
    %{prefix}/lib/mozilla
%{SOURCE8} /tmp/mozilla-mail.list.shared /tmp/mozilla-mail.package \
    $RPM_BUILD_ROOT/%{prefix}/lib \
    $RPM_BUILD_DIR/mozilla/dist/bin \
    %{prefix}/lib

%{SOURCE8} /tmp/mozilla-psm.list /tmp/mozilla-psm.package \
    $RPM_BUILD_ROOT/%{prefix}/lib/mozilla \
    $RPM_BUILD_DIR/mozilla/dist/bin \
    %{prefix}/lib/mozilla
#%{SOURCE8} /tmp/mozilla-psm.list.shared /tmp/mozilla-psm.package \
#    $RPM_BUILD_ROOT/%{prefix}/lib \
#    $RPM_BUILD_DIR/mozilla/dist/bin \
#    %{prefix}/lib

%{SOURCE8} /tmp/mozilla-chat.list /tmp/mozilla-chat.package \
    $RPM_BUILD_ROOT/%{prefix}/lib/mozilla \
    $RPM_BUILD_DIR/mozilla/dist/bin \
    %{prefix}/lib/mozilla
%{SOURCE8} /tmp/mozilla-chat.list.shared /tmp/mozilla-chat.package \
    $RPM_BUILD_ROOT/%{prefix}/lib \
    $RPM_BUILD_DIR/mozilla/dist/bin \
    %{prefix}/lib

# cp -L (dereference all symlinks) is required for fileutils >= 2.0.27
# (POSIX compliance); prior versions don't understand -L, so fall back...

# copy include and idl files
/bin/cp -rL dist/include/* $RPM_BUILD_ROOT/%{prefix}/include/mozilla || \
    /bin/cp -r dist/include/* $RPM_BUILD_ROOT/%{prefix}/include/mozilla

/bin/cp -rL dist/idl/* $RPM_BUILD_ROOT/%{prefix}/include/mozilla/idl || \
    /bin/cp -r dist/idl/* $RPM_BUILD_ROOT/%{prefix}/include/mozilla/idl

# copy our devel tools
/bin/cp -rL dist/bin/xpcshell $RPM_BUILD_ROOT/%{prefix}/bin/ || \
    /bin/cp -r dist/bin/xpcshell $RPM_BUILD_ROOT/%{prefix}/bin/

/bin/cp -rL dist/bin/xpidl $RPM_BUILD_ROOT/%{prefix}/bin/ || \
    /bin/cp -r dist/bin/xpidl $RPM_BUILD_ROOT/%{prefix}/bin/

/bin/cp -rL dist/bin/xpt_dump $RPM_BUILD_ROOT/%{prefix}/bin/ || \
    /bin/cp -r dist/bin/xpt_dump $RPM_BUILD_ROOT/%{prefix}/bin/

/bin/cp -rL dist/bin/xpt_link $RPM_BUILD_ROOT/%{prefix}/bin/ || \
    /bin/cp -r dist/bin/xpt_link $RPM_BUILD_ROOT/%{prefix}/bin/

install -c -m 755 %{SOURCE1} $RPM_BUILD_ROOT/%{prefix}/bin/mozilla
install -c -m 755 %{SOURCE11} $RPM_BUILD_ROOT/%{prefix}/lib/mozilla/

# set up our desktop files
/bin/mkdir -p $RPM_BUILD_ROOT/%{prefix}/share/pixmaps/
/bin/mkdir -p $RPM_BUILD_ROOT/opt/gnome/share/gnome/apps/Internet

/bin/cp %{SOURCE2} $RPM_BUILD_ROOT/%{prefix}/share/pixmaps/
/bin/cp %{SOURCE3} $RPM_BUILD_ROOT/%{prefix}/share/pixmaps/
/bin/cp %{SOURCE4} $RPM_BUILD_ROOT/opt/gnome/share/gnome/apps/Internet
/bin/cp %{SOURCE5} $RPM_BUILD_ROOT/opt/gnome/share/gnome/apps/Internet
/bin/cp %{SOURCE6} $RPM_BUILD_ROOT/opt/gnome/share/gnome/apps/Internet

# our icons are better!
/bin/cp %{SOURCE9}  $RPM_BUILD_ROOT/opt/gnome/lib/mozilla/icons/
/bin/cp %{SOURCE10} $RPM_BUILD_ROOT/opt/gnome/lib/mozilla/icons/

%clean
/bin/rm -rf $RPM_BUILD_ROOT

%post
# run ldconfig before regxpcom
/sbin/ldconfig >/dev/null 2>/dev/null

if [ -f /opt/gnome/lib/mozilla/rebuild-databases.sh ]; then
    /opt/gnome/lib/mozilla/rebuild-databases.sh
fi

%postun
/sbin/ldconfig >/dev/null 2>/dev/null

%preun
/bin/rm -rf /opt/gnome/lib/mozilla/chrome/overlayinfo
/bin/rm -f /opt/gnome/lib/mozilla/chrome/*.rdf

%post mail
/sbin/ldconfig >/dev/null 2>/dev/null

if [ -f /opt/gnome/lib/mozilla/rebuild-databases.sh ]; then
    /opt/gnome/lib/mozilla/rebuild-databases.sh
fi

%postun mail

# run ldconfig before regxpcom
/sbin/ldconfig >/dev/null 2>/dev/null

if [ -f /opt/gnome/lib/mozilla/rebuild-databases.sh ]; then
    /opt/gnome/lib/mozilla/rebuild-databases.sh
fi

%post psm
# run ldconfig before regxpcom
/sbin/ldconfig >/dev/null 2>/dev/null

if [ -f /opt/gnome/lib/mozilla/rebuild-databases.sh ]; then
    /opt/gnome/lib/mozilla/rebuild-databases.sh
fi

%postun psm
# run ldconfig before regxpcom
/sbin/ldconfig >/dev/null 2>/dev/null

if [ -f /opt/gnome/lib/mozilla/rebuild-databases.sh ]; then
    /opt/gnome/lib/mozilla/rebuild-databases.sh
fi

%post chat
# run ldconfig before regxpcom
/sbin/ldconfig >/dev/null 2>/dev/null

if [ -f /opt/gnome/lib/mozilla/rebuild-databases.sh ]; then
    /opt/gnome/lib/mozilla/rebuild-databases.sh
fi

%postun chat
# run ldconfig before regxpcom
/sbin/ldconfig >/dev/null 2>/dev/null

if [ -f /opt/gnome/lib/mozilla/rebuild-databases.sh ]; then
    /opt/gnome/lib/mozilla/rebuild-databases.sh
fi

%files -f /tmp/mozilla.package
%defattr(-,root,root)
%{prefix}/bin/mozilla
%{prefix}/lib/mozilla/rebuild-databases.sh
%{prefix}/share/pixmaps/mozilla-icon.png
%{prefix}/share/pixmaps/migrate-icon.gif

%{prefix}/lib/mozilla/component.reg
%{prefix}/lib/mozilla/components/xptitemp.dat
%{prefix}/lib/mozilla/components/xpti.dat
%dir %{prefix}/lib/mozilla/defaults/pref
%dir %{prefix}/lib/mozilla/defaults/profile
%dir %{prefix}/lib/mozilla/defaults/wallet
%dir %{prefix}/lib/mozilla/defaults
%dir %{prefix}/lib/mozilla/chrome
%dir %{prefix}/lib/mozilla/components
%dir %{prefix}/lib/mozilla/res/builtin
%dir %{prefix}/lib/mozilla/res/rdf
%dir %{prefix}/lib/mozilla/res
%dir %{prefix}/lib/mozilla/icons
%dir %{prefix}/lib/mozilla/defaults/profile/US
%dir %{prefix}/lib/mozilla/searchplugins

%dir %{prefix}/lib/mozilla/plugins
%dir %{prefix}/lib/mozilla/res/html
%dir %{prefix}/lib/mozilla/res/samples
%dir %{prefix}/lib/mozilla/res/entityTables

/opt/gnome/share/gnome/apps/Internet/mozilla.desktop
/opt/gnome/share/gnome/apps/Internet/mozilla-profile.desktop
/opt/gnome/share/gnome/apps/Internet/mozilla-ns-upgrade.desktop

%files mail -f /tmp/mozilla-mail.package
%defattr(-,root,root)

%files psm -f /tmp/mozilla-psm.package
%defattr(-,root,root)

%files chat -f /tmp/mozilla-chat.package
%defattr(-,root,root)

%files devel
%defattr(-,root,root)
%dir %{prefix}/include/mozilla
%{prefix}/include/mozilla/*
%{prefix}/bin/xpcshell
%{prefix}/bin/xpidl
%{prefix}/bin/xpt_dump
%{prefix}/bin/xpt_link


%changelog
* Mon Jun 04 2001 Christopher Blizzard <blizzard@redhat.com>
- Fix problems with the default SSL CA list not being loaded.  This
  would cause certificate warnings on sites that would normally have a
  recognized certificate authority.  This was fixed by putting
  libnssckbi.so into /usr/lib/mozilla instead of /usr/lib.
- Use --enable-crypto instead of a second build with
  BUILD_MODULES=psm2

* Wed May 16 2001 Christopher Blizzard <blizzard@redhat.com>
- Add missing --shared on the second pass of the chatzilla package.

* Sat Apr 28 2001 Christopher Blizzard <blizzard@redhat.com>
- Add script to do all the db rebuilds for us.
- Add versioned prereqs

* Tue Apr 24 2001 Christopher Blizzard <blizzard@redhat.com>
- Move .so libraries that aren't components to /usr/lib
- Move devel tools to /usr/bin

* Wed Apr 18 2001 Christopher Blizzard <blizzard@redhat.com>
- Add /usr/lib/mozilla/plugins to LD_LIBRARY_PATH in mozilla.sh

* Thu Mar 29 2001 Christopher Blizzard <blizzard@redhat.com>
- Add --without-mng to configure lines to avoid picking up the mng
library in rawhide.

* Tue Mar 20 2001 Christopher Blizzard <blizzard@redhat.com>
- Ignore the return value of regxpcom and regchrome.  They will
  segfault because of binary incompatible changes during upgrades but
  the last upgrade bits will always work so we should be OK.

* Mon Mar 12 2001 Christopher Blizzard <blizzard@redhat.com>
- Add chatzilla rpms.

* Wed Mar 07 2001 Christopher Blizzard <blizzard@redhat.com>
- Add LD_ASSUME_KERNEL hack to mozilla.sh so that the JVM will work.

* Tue Feb 27 2001 Christopher Blizzard <blizzard@redhat.com>
- Add missing directories to file sections for mozilla and
  mozilla-psm.

* Fri Feb 16 2001 Christopher Blizzard <blizzard@redhat.com>
- Remove requires since we have prereq.

* Sat Feb 10 2001 Christopher Blizzard <blizzard@redhat.com>
- Add xpidl compiler + related tools to the devel package.
- Check that regxpcom exists in postun sections.  There's no ordering
  guarantee when you uninstall rpms.

* Mon Feb 05 2001 Christopher Blizzard <blizzard@redhat.com>
- Turn of parallel builds again.

* Sun Jan 28 2001 Christopher Blizzard <blizzard@redhat.com>
- Try with parallel builds again.
- Use --enable-nspr-autoconf
- In the clean section don't delete the building area.

* Sat Jan 27 2001 Christopher Blizzard <blizzard@redhat.com>
- Remove hacks for installed-chrome.txt and regchrome.  They are
  listed in the packages files now.

* Thu Jan 18 2001 Christopher Blizzard <blizzard@redhat.com>
- Add proper prereq for psm, mail and base package
- Remove checks for programs before running post and postun

* Tue Jan 16 2001 Christopher Blizzard <blizzard@redhat.com>
- Check the existence of programs before running post and postun
  scripts for sub-packages.

* Mon Jan 15 2001 Christopher Blizzard <blizzard@redhat.com>
- Remove mozilla-specific rdf toolbar items

* Thu Jan 11 2001 Christopher Blizzard <blizzard@redhat.com>
- Re-add rm in clean

* Tue Jan 09 2001 Christopher Blizzard <blizzard@redhat.com>
- Change tip serial to 8 and 0.7 release serial to 7.  This way we can
  do upgrades properly.

* Mon Jan 08 2001 Christopher Blizzard <blizzard@redhat.com>
- Add explicit paths for rm and mkdir

* Sat Jan 06 2001 Christopher Blizzard <blizzard@redhat.com>
- Remove patch for -fshort-wchar problems and use
  --disable-short-wchar until the next compiler release.
- Use cooler icons.

* Tue Jan 02 2001 Christopher Blizzard <blizzard@redhat.com>
- Add patch to get default home page on 6.2 builds, too.

* Mon Jan 01 2001 Christopher Blizzard <blizzard@redhat.com>
- Add patch to point default page at local file system and to point
  mailnews at about:blank.

* Mon Jan 01 2001 Christopher Blizzard <blizzard@redhat.com>
- Add patch to remove debug menu from preferences.

* Sun Dec 31 2000 Christopher Blizzard <blizzard@redhat.com>
- Add patch to support building psm on ppc.

* Fri Dec 29 2000 Christopher Blizzard <blizzard@redhat.com>
- Add autoconf check for bad -fshort-wchar support in compiler.  
- Clean up a lot of cruft in the spec file that I don't need anymore.
- Make regxpcom generated files non-config so that they aren't saved
  as .rpmsave files.

* Thu Dec 28 2000 Christopher Blizzard <blizzard@redhat.com>
- Change the sparc patch to support sparc + sparc64.

* Thu Dec 28 2000 Christopher Blizzard <blizzard@redhat.com>
- Don't remove the CVS directories anymore since we're using the
  package files now.

* Thu Dec 28 2000 Christopher Blizzard <blizzard@redhat.com>
- Breakout psm
- Re-add the sparc config patch.

* Wed Dec 20 2000 Christopher Blizzard <blizzard@redhat.com>
- Add a bunch of dir entries to make sure that we don't leave a lot of
  crap behind when we uninstall the rpm.

* Tue Dec 19 2000 Christopher Blizzard <blizzard@redhat.com>
- Finish with mail/news breakout.
- Move component registration to package install time instead of at
  package build time.

* Wed Dec 13 2000 Christopher Blizzard <blizzard@redhat.com>
- Break out mail/news

* Tue Dec 12 2000 Christopher Blizzard <blizzard@redhat.com>
- Remove Debug menus from mail/news, browser and editor.

* Mon Dec 11 2000 Christopher Blizzard <blizzard@redhat.com>
- Add new mozilla.sh script that tries to send commands to a running
  instance first.
- Add desktop files and icons.

* Tue Dec 05 2000 Christopher Blizzard <blizzard@redhat.com>
- Build on only one CPU until the parallel build problems are worked
  out.
- Don't try to build on ai64

* Thu Oct 26 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build with new fileutils

* Fri Oct 13 2000 Christopher Blizzard <blizzard@redhat.com>
- Move to post M18 builds

* Mon Oct 2 2000 Christopher Blizzard <blizzard@redhat.com>
- start daily builds - remove the old patches
- delete installed directories for chrome since everything
  is in jar files now.

* Fri Aug 18 2000 Matt Wilson <msw@redhat.com>
- added patch to work around va_arg mess on gcc 2.96

* Wed Aug  9 2000 Christopher Blizzard <blizzard@redhat.com>
- Use official M17 source tarball

* Tue Aug  8 2000 Christopher Blizzard <blizzard@redhat.com>
- Add patch to fix crash when viewing some rgba images
- Add patch to fix sign warnings in gtkmozembed.h header

* Mon Aug  7 2000 Christopher Blizzard <blizzard@redhat.com>
- Build M17 official
- Add patch to fix crash when viewing some png images
- Add patch to fix context menu popup grab behaviour
- Add patch to fix focus problems with the file upload widget

* Thu Jul 27 2000 Christopher Blizzard <blizzard@redhat.com>
- Update to M17 snapshot

* Mon Jul 24 2000 Christopher Blizzard <blizzard@redhat.com>
- Update to most recent snapshot
- Added chrome rdf hacks

* Tue Mar 14 2000 Bernhard Rosenkränzer <bero@redhat.com>
- initial RPM
