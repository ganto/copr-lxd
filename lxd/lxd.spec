%if 0%{?fedora}
%global with_devel 1
%global with_debug 1
%global with_check 1
%global with_unit_test 1
%else
%global with_devel 1
%global with_debug 1
%global with_check 0
%global with_unit_test 0
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider github
%global provider_tld com
%global project lxc
%global repo lxd

# lxd
%global git0 https://%{provider}.%{provider_tld}/%{project}/%{repo}
%global commit c618e320301f00f7257b6c9752ae59f90447d430
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}

# lxc-go
%global git1 https://%{provider}.%{provider_tld}/%{project}/go-lxc
%global commit1 aeb7ce45882f9bcad11b421c9e612b4010e820bc
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global import_path1 gopkg.in/lxc/go-lxc.v2

Name:    lxd
Version: 2.9.3
Release: 1%{?dist}
Summary: Container hypervisor based on LXC
License: ASL 2.0
URL: https://linuxcontainers.org/lxd
Source0: %{git0}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1: %{git1}/archive/%{commit1}/go-lxc-%{shortcommit1}.tar.gz
Source2: lxd.socket
Source3: lxd.service
Source4: lxd.lxd-containers.service
Source5: lxd.dnsmasq
Source6: lxd.logrotate
Source7: shutdown

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

BuildRequires: pkgconfig(lxc)
BuildRequires: systemd-units
BuildRequires: help2man

%if ! 0%{?with_bundled}
BuildRequires: golang(github.com/dustinkirkland/golang-petname)
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/gorilla/mux)
BuildRequires: golang(github.com/gorilla/websocket)
BuildRequires: golang(github.com/gosexy/gettext)
BuildRequires: golang(github.com/mattn/go-runewidth)
BuildRequires: golang(github.com/mattn/go-sqlite3)
BuildRequires: golang(github.com/olekukonko/tablewriter)
BuildRequires: golang(github.com/pborman/uuid)
BuildRequires: golang(github.com/syndtr/gocapability/capability)
BuildRequires: golang(golang.org/x/crypto/scrypt)
BuildRequires: golang(golang.org/x/crypto/ssh/terminal)
BuildRequires: golang(gopkg.in/inconshreveable/log15.v2)
BuildRequires: golang(gopkg.in/flosch/pongo2.v3)
BuildRequires: golang(gopkg.in/tomb.v2)
BuildRequires: golang(gopkg.in/yaml.v2)
%endif

Requires: acl
Requires: dnsmasq
Requires: ebtables
Requires: iptables
Requires: lxd-client = %{version}-%{release}
Requires: lxcfs
Requires: rsync
Requires: shadow-utils
Requires: squashfs-tools
Requires: tar
Requires: xz

%if 0%{?fedora}
Suggests: criu
Suggests: device-mapper-persistent-data
Suggests: lvm2
Suggests: lxd-doc
Suggests: lxd-tools
%endif

%description
Container hypervisor based on LXC
LXD offers a REST API to remotely manage containers over the network,
using an image based workflow and with support for live migration.

This package contains the LXD daemon.

%if 0%{?with_devel}
%package devel
BuildArch: noarch
Summary: %{summary} - Source Libraries

%if 0%{?with_check}
BuildRequires: golang(github.com/dustinkirkland/golang-petname)
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/gorilla/mux)
BuildRequires: golang(github.com/gorilla/websocket)
BuildRequires: golang(github.com/gosexy/gettext)
BuildRequires: golang(github.com/mattn/go-runewidth)
BuildRequires: golang(github.com/mattn/go-sqlite3)
BuildRequires: golang(github.com/olekukonko/tablewriter)
BuildRequires: golang(github.com/pborman/uuid)
BuildRequires: golang(github.com/syndtr/gocapability/capability)
BuildRequires: golang(golang.org/x/crypto/scrypt)
BuildRequires: golang(golang.org/x/crypto/ssh/terminal)
BuildRequires: golang(gopkg.in/inconshreveable/log15.v2)
BuildRequires: golang(gopkg.in/inconshreveable/log15.v2/term)
BuildRequires: golang(gopkg.in/flosch/pongo2.v3)
BuildRequires: golang(gopkg.in/tomb.v2)
BuildRequires: golang(gopkg.in/yaml.v2)
%endif

Requires: golang(github.com/dustinkirkland/golang-petname)
Requires: golang(github.com/golang/protobuf/proto)
Requires: golang(github.com/gorilla/mux)
Requires: golang(github.com/gorilla/websocket)
Requires: golang(github.com/gosexy/gettext)
Requires: golang(github.com/mattn/go-runewidth)
Requires: golang(github.com/mattn/go-sqlite3)
Requires: golang(github.com/olekukonko/tablewriter)
Requires: golang(github.com/pborman/uuid)
Requires: golang(github.com/syndtr/gocapability/capability)
Requires: golang(golang.org/x/crypto/scrypt)
Requires: golang(golang.org/x/crypto/ssh/terminal)
Requires: golang(gopkg.in/inconshreveable/log15.v2)
Requires: golang(gopkg.in/inconshreveable/log15.v2/term)
Requires: golang(gopkg.in/flosch/pongo2.v3)
Requires: golang(gopkg.in/tomb.v2)
Requires: golang(gopkg.in/yaml.v2)

Provides: golang(%{import_path}) = %{version}-%{release}
Provides: golang(%{import_path}/lxd/types) = %{version}-%{release}
Provides: golang(%{import_path}/shared) = %{version}-%{release}
Provides: golang(%{import_path}/shared/api) = %{version}-%{release}
Provides: golang(%{import_path}/shared/gnuflag) = %{version}-%{release}
Provides: golang(%{import_path}/shared/i18n) = %{version}-%{release}
Provides: golang(%{import_path}/shared/ioprogress) = %{version}-%{release}
Provides: golang(%{import_path}/shared/logging) = %{version}-%{release}
Provides: golang(%{import_path}/shared/osarch) = %{version}-%{release}
Provides: golang(%{import_path}/shared/simplestreams) = %{version}-%{release}
Provides: golang(%{import_path}/shared/termios) = %{version}-%{release}
Provides: golang(%{import_path}/shared/version) = %{version}-%{release}

Provides: golang(%{import_path1}) = %{version}-%{release}

%description devel
LXD offers a REST API to remotely manage containers over the network,
using an image based workflow and with support for live migration.

This package contains library sources intended for
building other packages which use the import path
%{import_path} prefix.
%endif

%package client
Summary: %{summary} - Client 

%description client
LXD offers a REST API to remotely manage containers over the network,
using an image based workflow and with support for live migration.

This package contains the command line client.

%package tools
Summary: %{summary} - Extra Tools

BuildRequires: python3-lxc
Requires: python3-lxc

%description tools
LXD offers a REST API to remotely manage containers over the network,
using an image based workflow and with support for live migration.

This package contains extra tools provided with LXD.
 - fuidshift - A tool to map/unmap filesystem uids/gids
 - lxc-to-lxd - A tool to migrate LXC containers to LXD

%package doc
BuildArch: noarch
Summary: %{summary} - Documentation

%description doc
LXD offers a REST API to remotely manage containers over the network,
using an image based workflow and with support for live migration.

This package contains user documentation.

%prep
%setup -q -n %{repo}-%{commit}

# unpack go-lxc
tar zxf %{SOURCE1}

%build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}
mkdir -p src/gopkg.in/lxc
ln -s ../../../go-lxc-%{commit1} src/%{import_path1}

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

%gobuild -o bin/lxd %{import_path}/lxd
%gobuild -o bin/lxc %{import_path}/lxc
%gobuild -o bin/fuidshift %{import_path}/fuidshift

# generate man-pages
help2man bin/lxd -n "The container hypervisor - daemon" --no-info > lxd.1
help2man bin/lxc -n "The container hypervisor - client" --no-info > lxc.1
help2man bin/fuidshift -n "uid/gid shifter" --no-info > fuidshift.1
help2man scripts/lxc-to-lxd -n "Convert LXC containers to LXD" --no-info --version-string=%{version} > lxc-to-lxd.1

%pre
# check for existence of lxd group, create it if not found
getent group lxd > /dev/null || groupadd -f -r lxd
exit 0

%install
# install binaries
install -d %{buildroot}%{_bindir}
install -p -m 755 bin/lxd %{buildroot}%{_bindir}/lxd
install -p -m 755 bin/lxc %{buildroot}%{_bindir}/lxc
install -p -m 755 bin/fuidshift %{buildroot}%{_bindir}/fuidshift

# install extra script
install -p -m 755 scripts/lxc-to-lxd %{buildroot}%{_bindir}/lxc-to-lxd

# extra configs
install -d %{buildroot}%{_sysconfdir}/dnsmasq.d
install -p -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/dnsmasq.d/lxd
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -p -m 644 %{SOURCE6} %{buildroot}%{_sysconfdir}/logrotate.d/lxd

# install bash completion
install -dp %{buildroot}%{_datadir}/bash-completion/completions
install -p -m 644 config/bash/lxd-client %{buildroot}%{_datadir}/bash-completion/completions/lxd-client

# install systemd units
install -d %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE3} %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE4} %{buildroot}%{_unitdir}/%{name}-containers.service
install -d %{buildroot}/usr/lib/%{name}
install -p -m 755 %{SOURCE7} %{buildroot}/usr/lib/%{name}/shutdown

# install man-pages
install -d %{buildroot}%{_mandir}/man1
cp -p lxd.1 %{buildroot}%{_mandir}/man1/
cp -p lxc.1 %{buildroot}%{_mandir}/man1/
cp -p fuidshift.1 %{buildroot}%{_mandir}/man1/
cp -p lxc-to-lxd.1 %{buildroot}%{_mandir}/man1/

# cache and log directories
install -d -m 711 %{buildroot}%{_localstatedir}/lib/%{name}
install -d %{buildroot}%{_localstatedir}/log/%{name}

# source codes for building projects
%if 0%{?with_devel} || ! 0%{?with_bundled}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -path ./go-lxc-%{commit1} -prune -o -iname "*.go" \! -iname "*_test.go" -print) ; do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
install -d -p %{buildroot}/%{gopath}/src/%{import_path1}/
pushd go-lxc-%{commit1}
for file in $(find . -iname "*.h" -o -iname "*.go" \! -iname "*_test.go") ; do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path1}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path1}/$file
    echo "%%{gopath}/src/%%{import_path1}/$file" >> ../devel.file-list
done
popd
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license COPYING
%doc AUTHORS CONTRIBUTING.md README.md
%config(noreplace) %{_sysconfdir}/dnsmasq.d/lxd
%config(noreplace) %{_sysconfdir}/logrotate.d/lxd
%{_bindir}/%{name}
%{_unitdir}/*
%dir /usr/lib/%{name}
/usr/lib/%{name}/*
%{_mandir}/man1/%{name}.1.gz
%dir %{_localstatedir}/log/%{name}
%defattr(-, root, root, 0711)
%dir %{_localstatedir}/lib/%{name}

%if 0%{?with_devel} || ! 0%{?with_bundled}
%files devel -f devel.file-list
%license COPYING
%doc AUTHORS CONTRIBUTING.md README.md
%dir %{gopath}/src/%{import_path}
%dir %{gopath}/src/%{import_path1}
%endif

%files client
%license COPYING
%{_bindir}/lxc
%{_datadir}/bash-completion/completions/lxd-client
%{_mandir}/man1/lxc.1.gz

%files tools
%license COPYING
%{_bindir}/fuidshift
%{_bindir}/lxc-to-lxd
%{_mandir}/man1/fuidshift.1.gz
%{_mandir}/man1/lxc-to-lxd.1.gz

%files doc
%license COPYING
%doc doc/*

%changelog
* Tue Feb 21 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.9.2-1
- Version bump to lxd-2.9.2

* Mon Feb 20 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.9.1-1
- Version bump to lxd-2.9.1
- Update embedded go-lxc to commit aeb7ce4

* Thu Jan 26 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.8-1
- Version bump to lxd-2.8, fix some gopath requires/provides

* Tue Dec 27 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.7-1
- Version bump to lxd-2.7, set LXD_DIR to mode 0711
- Add lxc-to-lxd migration script to lxd-tools package

* Wed Dec 14 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.6.2-5
- Don't restrict world access to /var/{lib,log}/lxd

* Sun Dec 11 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.6.2-4
- Fix cache directory permissions, add more suggested packages

* Sat Dec 10 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.6.2-3
- Fix /var/lib/lxd, add shutdown script, new lxd-doc RPM

* Sat Dec 10 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.6.2-2
- Big spec file cleanup, fix devel RPM

* Sun Dec 4 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.6.2-1
- Initial packaging
