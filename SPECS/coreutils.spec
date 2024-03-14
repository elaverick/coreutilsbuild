Summary:        Basic system utilities
Name:           coreutils
Version:        %{version}
Release:        3%{PKG_RELEASE}
License:        GPLv3
URL:            http://www.gnu.org/software/coreutils
Group:          System Environment/Base
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://ftp.gnu.org/gnu/coreutils/%{name}-%{version}.tar.xz

# Patches are taken from:
# www.linuxfromscratch.org/patches/downloads/coreutils/
Patch0: coreutils-i18n.patch

Requires:       gmp

Provides:       sh-utils

%description
The Coreutils package contains utilities for showing and setting
the basic system

%package lang
Summary:    Additional language files for coreutils
Group:      System Environment/Base
Requires:   %{name} = %{version}-%{release}

%description lang
These are the additional language files of coreutils.

%prep
%autosetup -p1

%build
autoreconf -fiv
export FORCE_UNSAFE_CONFIGURE=1
%configure \
    --enable-no-install-program=kill,uptime \
    --disable-silent-rules

%make_build

%install
%make_install %{?_smp_mflags}
install -vdm 755 %{buildroot}%{_bindir}
install -vdm 755 %{buildroot}%{_sbindir}
install -vdm 755 %{buildroot}%{_mandir}/man8
mv -v %{buildroot}%{_bindir}/chroot %{buildroot}%{_sbindir}
mv -v %{buildroot}%{_mandir}/man1/chroot.1 %{buildroot}%{_mandir}/man8/chroot.8
sed -i 's/\"1\"/\"8\"/1' %{buildroot}%{_mandir}/man8/chroot.8
rm -rf %{buildroot}%{_infodir}
install -vdm755 %{buildroot}%{_sysconfdir}/profile.d

%find_lang %{name}

%if 0%{?with_check}
%check
sed -i '37,40d' tests/df/df-symlink.sh
sed -i '/mb.sh/d' Makefile
chown -Rv nobody .
env PATH="$PATH" NON_ROOT_USERNAME=nobody make -k check-root %{?_smp_mflags}
make NON_ROOT_USERNAME=nobody check %{?_smp_mflags}
%endif

%clean
rm -rf %{buildroot}/*

%post
/sbin/ldconfig
mkdir -p %{_sharedstatedir}/rpm-state
touch %{coreutils_present}

%postun
/sbin/ldconfig
[ $1 = 0 ] && rm -f %{coreutils_present}

%files
%defattr(-,root,root)
%{_sysconfdir}/profile.d/serial-console.sh
%{_libexecdir}/*
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/*/*

%files lang -f %{name}.lang
%defattr(-,root,root)