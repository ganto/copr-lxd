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
%global project         juju
%global repo            idmclient
# https://github.com/juju/idmclient
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          15392b0e99abe5983297959c737b8d000e43b34c
%global commitdate      20171110
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}
Version:        0
Release:        0.1.%{commitdate}git%{shortcommit}%{?dist}
Summary:        Client for USSO to macaroons bridge server
License:        LGPLv3
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

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
BuildRequires: golang(github.com/juju/httprequest)
BuildRequires: golang(github.com/juju/testing)
BuildRequires: golang(github.com/juju/testing/checkers)
BuildRequires: golang(github.com/juju/usso)
BuildRequires: golang(github.com/juju/utils/cache)
BuildRequires: golang(golang.org/x/net/context)
BuildRequires: golang(gopkg.in/check.v1)
BuildRequires: golang(gopkg.in/errgo.v1)
BuildRequires: golang(gopkg.in/juju/environschema.v1)
BuildRequires: golang(gopkg.in/juju/environschema.v1/form)
BuildRequires: golang(gopkg.in/juju/names.v2)
BuildRequires: golang(gopkg.in/macaroon.v2)
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/bakery)
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/bakery/checkers)
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/bakery/identchecker)
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/bakerytest)
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/httpbakery)
BuildRequires: golang(gopkg.in/macaroon-bakery.v2/httpbakery/agent)
%endif

Requires:      golang(github.com/juju/httprequest)
Requires:      golang(github.com/juju/usso)
Requires:      golang(github.com/juju/utils/cache)
Requires:      golang(golang.org/x/net/context)
Requires:      golang(gopkg.in/errgo.v1)
Requires:      golang(gopkg.in/juju/environschema.v1)
Requires:      golang(gopkg.in/juju/environschema.v1/form)
Requires:      golang(gopkg.in/juju/names.v2)
Requires:      golang(gopkg.in/macaroon.v2)
Requires:      golang(gopkg.in/macaroon-bakery.v2/bakery)
Requires:      golang(gopkg.in/macaroon-bakery.v2/bakery/checkers)
Requires:      golang(gopkg.in/macaroon-bakery.v2/bakery/identchecker)
Requires:      golang(gopkg.in/macaroon-bakery.v2/bakerytest)
Requires:      golang(gopkg.in/macaroon-bakery.v2/httpbakery)
Requires:      golang(gopkg.in/macaroon-bakery.v2/httpbakery/agent)

Provides:      golang(%{import_path}) = %{version}-%{release}
Provides:      golang(%{import_path}/idmtest) = %{version}-%{release}
Provides:      golang(%{import_path}/params) = %{version}-%{release}
Provides:      golang(%{import_path}/ussodischarge) = %{version}-%{release}
Provides:      golang(%{import_path}/usslogin) = %{version}-%{release}

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

Requires:      golang(github.com/juju/httprequest)
Requires:      golang(github.com/juju/testing)
Requires:      golang(github.com/juju/testing/checkers)
Requires:      golang(github.com/juju/usso)
Requires:      golang(golang.org/x/net/context)
Requires:      golang(gopkg.in/check.v1)
Requires:      golang(gopkg.in/juju/environschema.v1/form)
Requires:      golang(gopkg.in/macaroon-bakery.v2/bakery)
Requires:      golang(gopkg.in/macaroon-bakery.v2/bakery/identchecker)
Requires:      golang(gopkg.in/macaroon-bakery.v2/httpbakery)

%description unit-test-devel
%{summary}.

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%autosetup -n %{repo}-%{commit}

%build

%install
# source codes for building projects
%if 0%{?with_devel}
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

%gotest %{import_path}
%gotest %{import_path}/idmtest
%gotest %{import_path}/params
%gotest %{import_path}/ussodischarge
%gotest %{import_path}/ussologin
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENCE
%doc README.md
%doc docs/login.txt
%endif

%if 0%{?with_unit_test}
%files unit-test-devel -f unit-test.file-list
%license LICENCE
%doc README.md
%endif

%changelog
* Fri Jan 12 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.1.20171110git15392b0
- Initial package

