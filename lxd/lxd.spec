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

%global provider        github
%global provider_tld    com
%global project         lxc
%global repo            lxd
# https://github.com/lxc/lxd
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}

Name:          lxd
Version:       2.20
Release:       1%{?dist}
Summary:       Container hypervisor based on LXC
License:       ASL 2.0
URL:           https://linuxcontainers.org/lxd
Source0:       https://linuxcontainers.org/downloads/lxd/lxd-%{version}.tar.gz
Source1:       lxd.socket
Source2:       lxd.service
Source3:       lxd.lxd-containers.service
Source4:       lxd.dnsmasq
Source5:       lxd.logrotate
Source6:       shutdown
Patch0:        lxd-2.20-000-Fix-TestEndpoints_LocalUnknownUnixGroup-test.patch
Patch1:        lxd-2.20-001-lxd-daemon-Fix-unsetting-https-address.patch

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

BuildRequires: libacl-devel
BuildRequires: sqlite-devel
BuildRequires: pkgconfig(lxc)
BuildRequires: systemd-units
BuildRequires: help2man

BuildRequires: golang(github.com/dustinkirkland/golang-petname)
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/gorilla/mux)
BuildRequires: golang(github.com/gorilla/websocket) >= 1.1.0
BuildRequires: golang(github.com/gosexy/gettext)
BuildRequires: golang(github.com/juju/idmclient)
BuildRequires: golang(github.com/juju/persistent-cookiejar)
BuildRequires: golang(github.com/mattn/go-colorable)
BuildRequires: golang(github.com/mattn/go-sqlite3) >= 1.2.0
BuildRequires: golang(github.com/olekukonko/tablewriter)
BuildRequires: golang(github.com/pborman/uuid)
BuildRequires: golang(github.com/syndtr/gocapability/capability)
BuildRequires: golang(golang.org/x/crypto/scrypt)
BuildRequires: golang(golang.org/x/crypto/ssh/terminal)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(gopkg.in/flosch/pongo2.v3)
# Change to golang(gopkg.in/lxc/go-lxc.v2) once lxd-devel providing this is gone
BuildRequires: golang-gopkg-lxc-go-lxc-v2-devel
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/bakery)
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/bakery/checkers)
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/bakery/identchecker)
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/httpbakery)
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/httpbakery/form)
BuildRequires: golang(gopkg.in/tomb.v2)
BuildRequires: golang(gopkg.in/yaml.v2)

Requires: acl
Requires: dnsmasq
Requires: ebtables
Requires: iptables
Requires: lxd-client = %{version}-%{release}
Requires: lxcfs
Requires: rsync
Requires: shadow-utils >= 4.1.5
Requires: squashfs-tools
Requires: tar
Requires: xdelta
Requires: xz

%if 0%{?fedora}
Suggests: btrfs-progs
Suggests: criu
Suggests: device-mapper-persistent-data
Suggests: lvm2
Suggests: lxd-doc
Suggests: lxd-tools
%endif

%description
Container hypervisor based on LXC
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains the LXD daemon.

%if 0%{?with_devel}
%package devel
Summary:       Container hypervisor based on LXC - Source Libraries
BuildArch:     noarch

%if 0%{?with_check}
BuildRequires: btrfs-progs
BuildRequires: dnsmasq

BuildRequires: golang(github.com/dustinkirkland/golang-petname)
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/gorilla/mux)
BuildRequires: golang(github.com/gorilla/websocket) >= 1.1.0
BuildRequires: golang(github.com/gosexy/gettext)
BuildRequires: golang(github.com/juju/idmclient)
BuildRequires: golang(github.com/juju/persistent-cookiejar)
BuildRequires: golang(github.com/mattn/go-colorable)
BuildRequires: golang(github.com/mattn/go-sqlite3) >= 1.2.0
BuildRequires: golang(github.com/mpvl/subtest)
BuildRequires: golang(github.com/olekukonko/tablewriter)
BuildRequires: golang(github.com/pborman/uuid)
BuildRequires: golang(github.com/stretchr/testify/assert) >= 1.2.0
BuildRequires: golang(github.com/stretchr/testify/require) >= 1.2.0
BuildRequires: golang(github.com/stretchr/testify/suite) >= 1.2.0
BuildRequires: golang(github.com/syndtr/gocapability/capability)
BuildRequires: golang(golang.org/x/crypto/scrypt)
BuildRequires: golang(golang.org/x/crypto/ssh/terminal)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(gopkg.in/flosch/pongo2.v3)
BuildRequires: golang(gopkg.in/juju/environschema.v1/form)
# Change to golang(gopkg.in/lxc/go-lxc.v2) once lxd-devel providing this is gone
BuildRequires: golang-gopkg-lxc-go-lxc-v2-devel
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/bakery)
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/bakery/checkers)
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/bakery/identchecker)
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/httpbakery)
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/httpbakery/form)
BuildRequires: golang(gopkg.in/tomb.v2)
BuildRequires: golang(gopkg.in/yaml.v2)
%endif

Requires:      golang(github.com/dustinkirkland/golang-petname)
Requires:      golang(github.com/golang/protobuf/proto)
Requires:      golang(github.com/gorilla/mux)
Requires:      golang(github.com/gorilla/websocket) >= 1.1.0
Requires:      golang(github.com/gosexy/gettext)
Requires:      golang(github.com/juju/idmclient)
Requires:      golang(github.com/juju/persistent-cookiejar)
Requires:      golang(github.com/mattn/go-colorable)
Requires:      golang(github.com/mattn/go-sqlite3) >= 1.2.0
Requires:      golang(github.com/olekukonko/tablewriter)
Requires:      golang(github.com/pborman/uuid)
Requires:      golang(github.com/stretchr/testify/require) >= 1.2.0
Requires:      golang(github.com/syndtr/gocapability/capability)
Requires:      golang(golang.org/x/crypto/scrypt)
Requires:      golang(golang.org/x/crypto/ssh/terminal)
Requires:      golang(golang.org/x/net/context)
Requires:      golang(gopkg.in/flosch/pongo2.v3)
Requires:      golang(gopkg.in/juju/environschema.v1/form)
# Change to golang(gopkg.in/lxc/go-lxc.v2) once lxd-devel providing this is gone
Requires:      golang-gopkg-lxc-go-lxc-v2-devel
Requires:      golang(gopkg.in/macaroon-bakery.v2/bakery)
Requires:      golang(gopkg.in/macaroon-bakery.v2/bakery/checkers)
Requires:      golang(gopkg.in/macaroon-bakery.v2/bakery/identchecker)
Requires:      golang(gopkg.in/macaroon-bakery.v2/httpbakery)
Requires:      golang(gopkg.in/macaroon-bakery.v2/httpbakery/form)
Requires:      golang(gopkg.in/tomb.v2)
Requires:      golang(gopkg.in/yaml.v2)

Provides:      golang(%{import_path}/client) = %{version}-%{release}
Provides:      golang(%{import_path}/lxc/config) = %{version}-%{release}
Provides:      golang(%{import_path}/lxd/config) = %{version}-%{release}
Provides:      golang(%{import_path}/lxd/db) = %{version}-%{release}
Provides:      golang(%{import_path}/lxd/db/node) = %{version}-%{release}
Provides:      golang(%{import_path}/lxd/db/query) = %{version}-%{release}
Provides:      golang(%{import_path}/lxd/db/schema) = %{version}-%{release}
Provides:      golang(%{import_path}/lxd/debug) = %{version}-%{release}
Provides:      golang(%{import_path}/lxd/endpoints) = %{version}-%{release}
Provides:      golang(%{import_path}/lxd/node) = %{version}-%{release}
Provides:      golang(%{import_path}/lxd/state) = %{version}-%{release}
Provides:      golang(%{import_path}/lxd/sys) = %{version}-%{release}
Provides:      golang(%{import_path}/lxd/task) = %{version}-%{release}
Provides:      golang(%{import_path}/lxd/types) = %{version}-%{release}
Provides:      golang(%{import_path}/lxd/util) = %{version}-%{release}
Provides:      golang(%{import_path}/lxd-benchmark/benchmark) = %{version}-%{release}
Provides:      golang(%{import_path}/shared) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/api) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/cancel) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/cmd) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/gnuflag) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/i18n) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/idmap) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/ioprogress) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/log15) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/log15/stack) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/log15/term) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/logger) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/logging) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/osarch) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/simplestreams) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/subtest) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/termios) = %{version}-%{release}
Provides:      golang(%{import_path}/shared/version) = %{version}-%{release}

%description devel
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains library sources intended for
building other packages which use the import path
%{import_path} prefix.
%endif

%if 0%{?with_unit_test}
%package unit-test-devel
Summary:       Unit tests for %{name} package
BuildArch:     noarch

# test subpackage tests code from devel subpackage
Requires:      %{name}-devel = %{version}-%{release}

Requires:      golang(github.com/mattn/go-sqlite3)
Requires:      golang(github.com/mpvl/subtest)
Requires:      golang(github.com/stretchr/testify/assert) >= 1.2.0
Requires:      golang(github.com/stretchr/testify/require) >= 1.2.0
Requires:      golang(github.com/stretchr/testify/suite) >= 1.2.0

%description unit-test-devel
%{summary}.

This package contains unit tests for project providing packages
with %{import_path} prefix.
%endif

%package client
Summary:       Container hypervisor based on LXC - Client

%description client
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains the command line client.

%package tools
Summary:       Container hypervisor based on LXC - Extra Tools

BuildRequires: python3-lxc
Requires:      python3-lxc

%description tools
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains extra tools provided with LXD.
 - fuidshift - A tool to map/unmap filesystem uids/gids
 - lxc-to-lxd - A tool to migrate LXC containers to LXD
 - lxd-benchmark - A LXD benchmark utility

%package doc
Summary:       Container hypervisor based on LXC - Documentation
BuildArch:     noarch

%description doc
LXD offers a REST API to remotely manage containers over the network,
using an image based work-flow and with support for live migration.

This package contains user documentation.

%prep
%autosetup -n %{name}-%{version} -p1

%build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

# work-around RHBZ #1409931
go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\\n')" -a -v -x -o bin/lxd -tags libsqlite3 %{import_path}/lxd

%gobuild -o bin/lxc %{import_path}/lxc
%gobuild -o bin/fuidshift %{import_path}/fuidshift
%gobuild -o bin/lxd-benchmark %{import_path}/lxd-benchmark

# generate man-pages
help2man bin/lxd -n "The container hypervisor - daemon" --no-info --no-discard-stderr > lxd.1
bin/lxc manpage .
help2man bin/fuidshift -n "uid/gid shifter" --no-info > fuidshift.1
help2man bin/lxd-benchmark -n "The container lightervisor - benchmark" --no-info --version-string=%{version} --no-discard-stderr > lxd-benchmark.1
help2man scripts/lxc-to-lxd -n "Convert LXC containers to LXD" --no-info --version-string=%{version} > lxc-to-lxd.1

%install
# install binaries
install -d %{buildroot}%{_bindir}
install -p -m 755 bin/lxd %{buildroot}%{_bindir}/lxd
install -p -m 755 bin/lxc %{buildroot}%{_bindir}/lxc
install -p -m 755 bin/fuidshift %{buildroot}%{_bindir}/fuidshift
install -p -m 755 bin/lxd-benchmark %{buildroot}%{_bindir}/lxd-benchmark

# install extra script
install -p -m 755 scripts/lxc-to-lxd %{buildroot}%{_bindir}/lxc-to-lxd

# extra configs
install -d %{buildroot}%{_sysconfdir}/dnsmasq.d
install -p -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/dnsmasq.d/lxd
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -p -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/logrotate.d/lxd

# install bash completion
install -dp %{buildroot}%{_datadir}/bash-completion/completions
install -p -m 644 config/bash/lxd-client %{buildroot}%{_datadir}/bash-completion/completions/lxd-client

# install systemd units
install -d %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE1} %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE2} %{buildroot}%{_unitdir}
install -p -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/%{name}-containers.service
install -d %{buildroot}/usr/lib/%{name}
install -p -m 755 %{SOURCE6} %{buildroot}/usr/lib/%{name}/shutdown

# install man-pages
install -d %{buildroot}%{_mandir}/man1
cp -p lxd.1 %{buildroot}%{_mandir}/man1/
cp -p lxc*.1 %{buildroot}%{_mandir}/man1/
cp -p fuidshift.1 %{buildroot}%{_mandir}/man1/
cp -p lxd-benchmark.1 %{buildroot}%{_mandir}/man1/
cp -p lxc-to-lxd.1 %{buildroot}%{_mandir}/man1/

# cache and log directories
install -d -m 711 %{buildroot}%{_localstatedir}/lib/%{name}
install -d %{buildroot}%{_localstatedir}/log/%{name}

# source codes for building projects
%if 0%{?with_devel} || ! 0%{?with_bundled}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go" -o -type f -wholename "./test/deps/s*"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test.file-list
done

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if 0%{?with_bundled}
export GOPATH=$(pwd)/Godeps/_workspace:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/lxc
%gotest %{import_path}/lxd
%gotest %{import_path}/lxd/config
%gotest %{import_path}/lxd/db
%gotest %{import_path}/lxd/db/node
%gotest %{import_path}/lxd/db/query
%gotest %{import_path}/lxd/db/schema
%gotest %{import_path}/lxd/debug
%gotest %{import_path}/lxd/endpoints
%gotest %{import_path}/lxd/node
%gotest %{import_path}/lxd/task
%gotest %{import_path}/lxd/types
%gotest %{import_path}/lxd/util
%gotest %{import_path}/shared
%gotest %{import_path}/shared/cmd
%gotest %{import_path}/shared/gnuflag
%gotest %{import_path}/shared/idmap
%gotest %{import_path}/shared/osarch
%gotest %{import_path}/shared/version
%endif

%pre
# check for existence of lxd group, create it if not found
getent group lxd > /dev/null || groupadd -f -r lxd
exit 0

%post
%systemd_post %{name}.socket
%systemd_post %{name}.service
%systemd_post %{name}-container.service

%postun
%systemd_postun %{name}.socket
%systemd_postun %{name}.service
%systemd_postun %{name}-container.service

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license COPYING
%doc AUTHORS
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
%doc AUTHORS
%endif

%if 0%{?with_unit_test}
%files unit-test-devel -f unit-test.file-list
%license COPYING
%endif

%files client
%license COPYING
%{_bindir}/lxc
%{_datadir}/bash-completion/completions/lxd-client
%{_mandir}/man1/lxc.*1.gz

%files tools
%license COPYING
%{_bindir}/fuidshift
%{_bindir}/lxd-benchmark
%{_bindir}/lxc-to-lxd
%{_mandir}/man1/fuidshift.1.gz
%{_mandir}/man1/lxd-benchmark.1.gz
%{_mandir}/man1/lxc-to-lxd.1.gz

%files doc
%license COPYING
%doc doc/*

%changelog
* Fri Nov 03 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.19-2
- Work-around syntax issue on Fedora 27.
- Runtime detect liblxc version.

* Mon Oct 30 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.19-1
- Update to 2.19.
- Update embedded go-lxc to commit 74fb852
- Drop hard dependency to lxc-2.1
- Various RPM metadata fixes

* Wed Oct 04 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.18-3
- Link against libsqlite3
- Update go-sqlite3 dependency to fix startup issue on Fedora 26
- Add upstream patches according to lxd-2.18-0ubuntu3

* Thu Sep 28 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.18-2
- Add upstream patches according to lxd-2.18-0ubuntu2
- Fix xdelta dependency, tighten liblxc version dependency

* Thu Sep 21 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.18-1
- Version bump to lxd-2.18
- Update embedded go-lxc to commit 89b06ca

* Mon Aug 28 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.17-3
- Add upstream patches according to lxd-2.17-0ubuntu2

* Thu Aug 24 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.17-2
- Fix man pages wrongly added to multiple packages

* Thu Aug 24 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.17-1
- Version bump to lxd-2.17

* Wed Jul 26 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.16-1
- Version bump to lxd-2.16

* Wed Jul 19 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.15-3
- Tweak timeouts for systemd units
- Add upstream patches according to lxd-2.15-0ubuntu6

* Mon Jul 03 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.15-2
- Rebuild with latest golang-github-gorilla-websocket

* Mon Jul 03 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.15-1
- Version bump to lxd-2.15
- Add upstream patches according to lxd-2.15-0ubuntu4

* Sat Jun 10 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.14-2
- Add some upstream patches according to lxd-2.14-0ubuntu3

* Wed Jun 07 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.14-1
- Version bump to lxd-2.14
- Update embedded go-lxc to commit de2c8bf
- "infinity" for NOFILE doesn't work, set fixed value

* Mon May 01 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.13-1
- Version bump to lxd-2.13
- Add lxc-benchmark to lxd-tools package

* Fri Mar 24 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.12-1
- Version bump to lxd-2.12
- Update embedded go-lxc to commit 8304875

* Thu Mar 09 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.11-1
- Version bump to lxd-2.11
- Add 'lvm-use-ff-with-vgremove.patch' from lxd-2.11-0ubuntu2

* Tue Mar 07 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.10.1-1
- Version bump to lxd-2.10.1

* Thu Mar 02 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.10-1
- Version bump to lxd-2.10, bump websocket dependency due to build errors

* Fri Feb 24 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.9.3-1
- Version bump to lxd-2.9.3

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
