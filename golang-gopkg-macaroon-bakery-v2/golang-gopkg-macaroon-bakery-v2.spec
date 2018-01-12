%if 0%{?fedora} || 0%{?rhel}
%global with_devel 1
%global with_bundled 0
%global with_debug 0
%global with_check 1
%global with_unit_test 1
%else
%global with_devel 1
%global with_bundled 0
%global with_debug 0
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
%global project         go-macaroon-bakery
%global repo            macaroon-bakery
# https://github.com/go-macaroon-bakery/macaroon-bakery
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     gopkg.in/macaroon-bakery.v2
%global gimport_path    %{provider_prefix}
%global commit          e7ab980e9bb658272c1b5bca7fb42e4d65b1cf2d
%global commitdate      20171026
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-gopkg-%{repo}-v2
Version:        2
Release:        0.1.%{commitdate}git%{shortcommit}%{?dist}
Summary:        Macaroon implementation in Go
License:        LGPL 3.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Patch0:         macaroon-bakery-e7ab980-Allow-localhost-to-be-resolved-via-IPv6.patch

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
%{summary}.

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check}
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/juju/httprequest)
BuildRequires: golang(github.com/juju/loggo)
BuildRequires: golang(github.com/juju/testing)
BuildRequires: golang(github.com/juju/testing/checkers)
BuildRequires: golang(github.com/juju/testing/httptesting)
BuildRequires: golang(github.com/juju/utils)
BuildRequires: golang(github.com/juju/webbrowser)
BuildRequires: golang(github.com/julienschmidt/httprouter)
BuildRequires: golang(github.com/rogpeppe/fastuuid)
BuildRequires: golang(golang.org/x/crypto/nacl/box)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(golang.org/x/net/context/ctxhttp)
BuildRequires: golang(golang.org/x/net/publicsuffix)
BuildRequires: golang(gopkg.in/check.v1)
BuildRequires: golang(gopkg.in/errgo.v1)
BuildRequires: golang(gopkg.in/juju/environschema.v1)
BuildRequires: golang(gopkg.in/juju/environschema.v1/form)
BuildRequires: golang(gopkg.in/macaroon.v2)
BuildRequires: golang(gopkg.in/mgo.v2)
BuildRequires: golang(gopkg.in/mgo.v2/bson)
BuildRequires: golang(gopkg.in/yaml.v2)
%endif

Requires:      golang(github.com/golang/protobuf/proto)
Requires:      golang(github.com/juju/httprequest)
Requires:      golang(github.com/juju/loggo)
Requires:      golang(github.com/juju/webbrowser)
Requires:      golang(github.com/julienschmidt/httprouter)
Requires:      golang(github.com/rogpeppe/fastuuid)
Requires:      golang(golang.org/x/crypto/nacl/box)
Requires:      golang(golang.org/x/net/context)
Requires:      golang(golang.org/x/net/context/ctxhttp)
Requires:      golang(golang.org/x/net/publicsuffix)
Requires:      golang(gopkg.in/errgo.v1)
Requires:      golang(gopkg.in/juju/environschema.v1)
Requires:      golang(gopkg.in/juju/environschema.v1/form)
Requires:      golang(gopkg.in/macaroon.v2)
Requires:      golang(gopkg.in/mgo.v2)
Requires:      golang(gopkg.in/mgo.v2/bson)

Provides:      golang(%{import_path}) = %{version}-%{release}
Provides:      golang(%{import_path}/bakery) = %{version}-%{release}
Provides:      golang(%{import_path}/bakery/checkers) = %{version}-%{release}
Provides:      golang(%{import_path}/bakery/example) = %{version}-%{release}
Provides:      golang(%{import_path}/bakery/example/meeting) = %{version}-%{release}
Provides:      golang(%{import_path}/bakery/identchecker) = %{version}-%{release}
Provides:      golang(%{import_path}/bakery/internal/macaroonpb) = %{version}-%{release}
Provides:      golang(%{import_path}/bakery/mgorootkeystore) = %{version}-%{release}
Provides:      golang(%{import_path}/bakerytest) = %{version}-%{release}
Provides:      golang(%{import_path}/httpbakery) = %{version}-%{release}
Provides:      golang(%{import_path}/httpbakery/agent) = %{version}-%{release}
Provides:      golang(%{import_path}/httpbakery/form) = %{version}-%{release}
Provides:      golang(%{import_path}/internal/httputil) = %{version}-%{release}
Provides:      golang(%{gimport_path}) = %{version}-%{release}
Provides:      golang(%{gimport_path}/bakery) = %{version}-%{release}
Provides:      golang(%{gimport_path}/bakery/checkers) = %{version}-%{release}
Provides:      golang(%{gimport_path}/bakery/example) = %{version}-%{release}
Provides:      golang(%{gimport_path}/bakery/example/meeting) = %{version}-%{release}
Provides:      golang(%{gimport_path}/bakery/identchecker) = %{version}-%{release}
Provides:      golang(%{gimport_path}/bakery/internal/macaroonpb) = %{version}-%{release}
Provides:      golang(%{gimport_path}/bakery/mgorootkeystore) = %{version}-%{release}
Provides:      golang(%{gimport_path}/bakerytest) = %{version}-%{release}
Provides:      golang(%{gimport_path}/httpbakery) = %{version}-%{release}
Provides:      golang(%{gimport_path}/httpbakery/agent) = %{version}-%{release}
Provides:      golang(%{gimport_path}/httpbakery/form) = %{version}-%{release}
Provides:      golang(%{gimport_path}/internal/httputil) = %{version}-%{release}


%description devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test}
%package unit-test-devel
Summary:       Unit tests for %{name} package
BuildArch:     noarch
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:      %{name}-devel = %{version}-%{release}

Requires:      golang(github.com/juju/loggo)
Requires:      golang(github.com/juju/testing)
Requires:      golang(github.com/juju/testing/checkers)
Requires:      golang(github.com/juju/testing/httptesting)
Requires:      golang(golang.org/x/crypto/nacl/box)
Requires:      golang(golang.org/x/net/context)
Requires:      golang(gopkg.in/check.v1)
Requires:      golang(gopkg.in/errgo.v1)
Requires:      golang(gopkg.in/httprequest.v1)
Requires:      golang(gopkg.in/juju/environschema.v1)
Requires:      golang(gopkg.in/juju/environschema.v1/form)
Requires:      golang(gopkg.in/macaroon.v2)
Requires:      golang(gopkg.in/mgo.v2)
Requires:      golang(gopkg.in/yaml.v2)

%description unit-test-devel
%{summary}.

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%package keygen
Summary:        Utility to generate a bakery keypair
# If go_arches not defined fall through to implicit golang archs
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description keygen
%{summary}

%prep
%autosetup -n %{repo}-%{commit} -p1

%build
mkdir -p src/gopkg.in
ln -s ../../ src/%{import_path}

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

%gobuild -o bakery-keygen %{import_path}/cmd/bakery-keygen

%install
# install binary
install -d %{buildroot}%{_bindir}
install -p -m 755 bakery-keygen %{buildroot}%{_bindir}/bakery-keygen

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
install -d -p %{buildroot}/%{gopath}/src/%{gimport_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
echo "%%dir %%{gopath}/src/%%{gimport_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    echo "%%dir %%{gopath}/src/%%{gimport_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{gimport_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{gimport_path}/$file
    echo "%%{gopath}/src/%%{gimport_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
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

%gotest %{import_path}/bakery
%gotest %{import_path}/bakery/checkers
%gotest %{import_path}/bakery/identchecker
%gotest %{import_path}/bakery/mgorootkeystore
%gotest %{import_path}/bakerytest
%gotest %{import_path}/httpbakery
%gotest %{import_path}/httpbakery/agent
%gotest %{import_path}/httpbakery/form
%gotest %{import_path}/internal/httputil
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files keygen
%license LICENSE
%{_bindir}/bakery-keygen

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc README.md
%endif

%if 0%{?with_unit_test}
%files unit-test-devel -f unit-test.file-list
%license LICENSE
%doc README.md
%endif

%changelog
* Fri Jan 12 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2-0.1.20171026gite7ab980
- Initial package

