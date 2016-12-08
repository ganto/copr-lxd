Name:       lxcfs
Version:    2.0.5
Release:    2%{?dist}
Summary:    FUSE filesystem for LXC

License:    Apache-2.0
URL:        https://linuxcontainers.org
Source0:    https://linuxcontainers.org/downloads/%{name}/%{name}-%{version}.tar.gz
Patch0:     lxcfs-2.0.5-Fix-systemd-unit-directory.patch

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: help2man
BuildRequires: libtool
BuildRequires: pam-devel
BuildRequires: pkgconfig
BuildRequires: pkgconfig(fuse)
BuildRequires: systemd

AutoProv:      no
Provides:      %{name} = %{version}%{?dist}

%description
LXCFS is a simple userspace filesystem designed to work
around some current limitations of the Linux kernel.

Specifically, it's providing two main things

- A set of files which can be bind-mounted over their
  /proc originals to provide CGroup-aware values.
- A cgroupfs-like tree which is container aware. The
  code is pretty simple, written in C using libfuse
  and glib.

%package -n pam_cgfs
Summary:    CGroup file system PAM module

%description -n pam_cgfs
When a user logs in, this pam module will create
cgroups which the user may administer, either for
all controllers or for any controllers listed on the
command line.

%prep
%setup -q
%patch0 -p1

%build
autoreconf --force --install
# RHEL still defaults to sysvinit
%configure --with-init-script=systemd
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} %{?_smp_mflags}
install -d -m 0755 %{buildroot}%{_localstatedir}/lib/%{name}/

# The shared library liblxcfs.so used by lxcfs is not supposed to be used by
# any other program. So we follow best practice and install it in
# /usr/lib/lxcfs. Note that lxcfs *expects* liblxcfs.so to be found in
# /usr/lib/lxcfs when it cannot find it in the lib.so path.
mkdir -p %{buildroot}/usr/lib/%{name}/
install -p -m 0755 .libs/liblxcfs.so %{buildroot}/usr/lib/%{name}/
rm -f %{buildroot}%{_libdir}/liblxcfs.so*
rm -f %{buildroot}%{_libdir}/liblxcfs.la

%pre
# check for existence of mock group, create it if not found
getent group mock > /dev/null || groupadd -f -g %mockgid -r mock
exit 0

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog README COPYING
%{_bindir}/*
%{_datadir}/lxc
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_unitdir}/%{name}.service
%dir %{_localstatedir}/lib/%{name}

# The lxcfs executable requires liblxcfs.so be installed. It calls dlopen() to
# dynamically reload the shared library on upgrade. This is important. Do *not*
# split into a separate package and do not turn this into a versioned shared
# library! (This shared library allows lxcfs to be updated without having to
# restart it which is good when you have important system containers running!)
%dir /usr/lib/%{name}
/usr/lib/%{name}/liblxcfs.so

%files -n pam_cgfs
%defattr(-,root,root)
/%{_lib}/security/pam_cgfs.so

%changelog
* Wed Nov 30 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.0.5-1
- Initial package
