Summary:        Intrusion detection environment
Name:           aide
Version:        0.19.2
Release:        4%{?dist}.1
URL:            https://github.com/aide/aide
License:        GPL-2.0-or-later
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz.asc
# gpg2 --recv-keys 2BBBD30FAAB29B3253BCFBA6F6947DAB68E7B931
# gpg2 --export --export-options export-minimal 2BBBD30FAAB29B3253BCFBA6F6947DAB68E7B931 >gpgkey-aide.gpg
Source2:        gpgkey-aide.gpg
Source3:        aide.conf
Source4:        README.quickstart
Source5:        aide.logrotate
Source6:        aide-tmpfiles.conf
Source7:        aide-migrate-config
Patch0:         aide-0.19.2-syslog-format.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  bison flex
BuildRequires:  pcre2-devel
BuildRequires:  libgpg-error-devel nettle-devel
BuildRequires:  zlib-devel
BuildRequires:  libcurl-devel
BuildRequires:  libacl-devel
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  libattr-devel
BuildRequires:  e2fsprogs-devel
BuildRequires:  audit-libs-devel
BuildRequires:  autoconf autoconf-archive
BuildRequires:  automake libtool systemd-rpm-macros
# For verifying signatures
BuildRequires:  gnupg2

%description
AIDE (Advanced Intrusion Detection Environment) is a file integrity
checker and intrusion detection program.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1
cp -a %{SOURCE4} .

%build
autoreconf -ivf
%configure  \
  --disable-static \
  --with-config_file=%{_sysconfdir}/aide.conf \
  --without-gcrypt \
  --with-nettle \
  --with-zlib \
  --with-curl \
  --with-posix-acl \
  --with-selinux \
  --with-xattr \
  --with-e2fsattrs \
  --with-audit
%make_build

%install
%make_install bindir=%{_sbindir}
install -Dpm0644 -t %{buildroot}%{_sysconfdir} %{SOURCE3}
install -Dpm0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/aide
mkdir -p %{buildroot}%{_localstatedir}/log/aide
mkdir -p -m0700 %{buildroot}%{_localstatedir}/lib/aide
# Install tmpfiles config
install -Dpm0644 %{SOURCE6} %{buildroot}%{_tmpfilesdir}/aide.conf
install -Dpm0755 %{SOURCE7} %{buildroot}%{_sbindir}/aide-migrate-config

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README
%doc README.quickstart
%{_sbindir}/aide
%{_sbindir}/aide-migrate-config
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%config(noreplace) %attr(0600,root,root) %{_sysconfdir}/aide.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/aide
%dir %attr(0700,root,root) %{_localstatedir}/lib/aide
%dir %attr(0700,root,root) %{_localstatedir}/log/aide
%{_tmpfilesdir}/aide.conf

%post
if [ $1 -ge 2 ]; then
    /usr/sbin/aide-migrate-config /etc/aide.conf 2>&1 | \
        tee -a /var/log/aide/aide-migrate.log || :
fi

%changelog
* Tue May 26 2026 Attila Lakatos <alakatos@redhat.com> - 0.19.2-4.1
- Re-add syslog_format config option dropped during rebase to 0.19.2
Resolves: RHEL-178845
- Add aide-migrate-config to automate config migration from pre-0.19 syntax

* Wed Oct 15 2025 Attila Lakatos <alakatos@redhat.com> - 0.19.2-4
- Adjust default config to avoid false positives in /etc
Resolves: RHEL-39970

* Thu Oct 09 2025 Attila Lakatos <alakatos@redhat.com> - 0.19.2-3
- /boot/grub2/grubenv is excluded from check due to boot_success implementation
- Do not monitor link count in /var/log/journal
Resolves: RHEL-39970

* Thu Sep 25 2025 Attila Lakatos <alakatos@redhat.com> - 0.19.2-2
- Modernize aide config file
Resolves: RHEL-39970
- No path reference ends with '/'
Resolves: RHEL-39959

* Tue Aug 05 2025 Attila Lakatos <alakatos@redhat.com> - 0.19.2-1
- rebase to 0.19.2
Resolves: RHEL-110572
- exclude directory but include subitems
Resolves: RHEL-1382
- prevent aide from exiting if a file is truncated during check
Resolves: RHEL-1383
- Switch to libnettle for hashing
Resolves: RHEL-59170

* Wed Jan 29 2025 Radovan Sroka <rsroka@redhat.com> - 0.18.6-8
RHEL 10.0 ERRATUM
Resolves: RHEL-4320

* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 0.18.6-7
- Bump release for October 2024 mass rebuild:
  Resolves: RHEL-64018

* Mon Jun 24 2024 Troy Dawson <tdawson@redhat.com> - 0.18.6-6
- Bump release for June 2024 mass rebuild

* Fri May 17 2024 Radovan Sroka <rsroka@redhat.com> - 0.18.6-5
REDHAT 10.0 ERRATUM
- fix verbose patch
- get rid of libgcrypt
Resolves: RHEL-36780

* Mon Feb 12 2024 Radovan Sroka <rsroka@redhat.com> - 0.18.6-4
- rebase to 0.18.6

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 24 2023 Radovan Sroka <rsroka@redhat.com> - 0.18.6-1
- rebase to 0.18.6

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 21 2023 Radovan Sroka <rsroka@redhat.com> - 0.18.4-1
- aide-0.18.4 is available
Resolves: rhbz#1910486
- Please port your pcre dependency to pcre2. Pcre has been deprecated
Resolves: rhbz#2128267

* Tue Jun 13 2023 Radovan Sroka <rsroka@redhat.com> - 0.16-23
- migrated to SPDX license

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Nov 25 2022 Florian Weimer <fweimer@redhat.com> - 0.16-21
- Apply upstream patches to port configure to C99

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jul 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-16
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 24 2020 Radovan Sroka <rsroka@redhat.com> 0.16-14
- AIDE breaks when setting report_ignore_e2fsattrs
  Resolves: rhbz#1850276

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 31 2019 Radovan Sroka <rsroka@redhat.com> - 0.16-12
- backport some patches
  Resolves: rhbz#1717140

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Feb 20 2019 Daniel Kopecek <dkopecek@redhat.com> - 0.16-10
- Fix building with curl
  Resolves: rhbz#1674637

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.16-8
- Rebuild with fixed binutils

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.16-6
- Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr 05 2017 Radovan Sroka <rsroka@redhat.com> - 0.16-2
- fixed upstream link

* Tue Apr 04 2017 Radovan Sroka <rsroka@redhat.com> - 0.16-1
- rebase to stable v0.16
- specfile cleanup
- make doc readable
  resolves: #1421355
- make aide binary runable for any user
  resolves: #1421351

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-0.3.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 12 2016 Tomas Sykora <tosykora@redhat.com> - 0.16-0.2.rc1
- New upstream devel version

* Mon Jun 20 2016 Tomas Sykora <tosykora@redhat.com> - 0.16-0.1.b1
- New upstream devel version

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jul 25 2015 Till Maas <opensource@till.name> - 0.15.1-11
- Remove prelink dependency because prelink was retired

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Yaakov Selkowitz <yselkowi@redhat.com> - 0.15.1-8
- Fix FTBFS with -Werror=format-security (#1036983, #1105942)
- Avoid prelink BR on aarch64, ppc64le (#924977, #1078476)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Daniel Kopecek <dkopecek@redhat.com> - 0.15.1-4
- added patch to fix aide in FIPS mode
- use only FIPS approved digest algorithms in aide.conf so that
  aide works by default in FIPS mode

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 11 2010 Steve Grubb <sgrubb@redhat.com> - 0.15.1-1
- New upstream release

* Tue May 18 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-5
- Apply 2 upstream bug fixes

* Tue May 18 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-4
- Use upstream's patch to fix bz 590566

* Sat May 15 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-3
- Fix bz 590561 aide does not detect the change of SElinux context
- Fix bz 590566 aide reports a changed file when it has not been changed

* Wed Apr 28 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-2
- Fix bz 574764 by replacing abort calls with exit
- Apply libgcrypt init patch

* Tue Mar 16 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-1
- New upstream release final 0.14

* Thu Feb 25 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-0.4.rc3
- New upstream release

* Thu Feb 25 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-0.3.rc2
- New upstream release

* Tue Feb 23 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-0.2.rc1
- Fix dirent detection on 64bit systems

* Mon Feb 22 2010 Steve Grubb <sgrubb@redhat.com> - 0.14-0.1.rc1
- New upstream release

* Fri Feb 19 2010 Steve Grubb <sgrubb@redhat.com> - 0.13.1-16
- Add logrotate script and spec file cleanups

* Fri Dec 11 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-15
- Get rid of .dedosify files

* Wed Dec 09 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-14
- Revise patch for Initialize libgcrypt correctly (#530485)

* Sat Nov 07 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-13
- Initialize libgcrypt correctly (#530485)

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.13.1-12
- rebuilt with new audit

* Wed Aug 19 2009 Steve Grubb <sgrubb@redhat.com> 0.13.1-11
- rebuild for new audit-libs
- Correct regex for root's dot files (#509370)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 08 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-9
- Make aide smarter about prelinked files (Peter Vrabec)
- Add /lib64 to default config

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 30 2009 Steve Grubb <sgrubb@redhat.com> - 0.13.1-6
- enable xattr support and update config file

* Fri Sep 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.13.1-5
- fix selcon patch to apply without fuzz

* Fri Feb 15 2008 Steve Conklin <sconklin@redhat.com>
- rebuild for gcc4.3

* Tue Aug 21 2007 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Jul 22 2007 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.13.1-2
- Apply Steve Conklin's patch to increase displayed portion of
  selinux context.

* Sun Dec 17 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.13.1-1
- Update to 0.13.1 release.

* Sun Dec 10 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.13-1
- Update to 0.13 release.
- Include default aide.conf from RHEL5 as doc example file.

* Sun Oct 29 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.12-3.20061027cvs
- CAUTION! This changes the database format and results in a report of
  false inconsistencies until an old database file is updated.
- Check out CVS 20061027 which now contains Red Hat's
  acl/xattr/selinux/audit patches.
- Patches merged upstream.
- Update manual page substitutions.

* Mon Oct 23 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.12-2
- Add "memory leaks and performance updates" patch as posted
  to aide-devel by Steve Grubb.

* Sat Oct 07 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.12-1
- Update to 0.12 release.
- now offers --disable-static, so -no-static patch is obsolete
- fill last element of getopt struct array with zeroes

* Mon Oct 02 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.11-3
- rebuilt

* Mon Sep 11 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.11-2
- rebuilt

* Sun Feb 19 2006 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.11-1
- Update to 0.11 release.
- useless-includes patch merged upstream.
- old Russian man pages not available anymore.
- disable static linking.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Fri Nov 28 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.10-0.fdr.1
- Update to 0.10 release.
- memleaks patch merged upstream.
- rootpath patch merged upstream.
- fstat patch not needed anymore.
- Updated URL.

* Thu Nov 13 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.10-0.fdr.0.2.cvs20031104
- Added buildreq m4 to work around incomplete deps of bison package.

* Tue Nov 04 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.10-0.fdr.0.1.cvs20031104
- Only tar.gz available upstream.
- byacc not needed when bison -y is available.
- Installed Russian manual pages.
- Updated with changes from CVS (2003-11-04).
- getopt patch merged upstream.
- bison-1.35 patch incorporated upstream.

* Tue Sep 09 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.9-0.fdr.0.2.20030902
- Added fixes for further memleaks.

* Sun Sep 07 2003 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.9-0.fdr.0.1.20030902
- Initial package version.
