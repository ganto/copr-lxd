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
%global repo            testing
# https://github.com/juju/testing
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          2fe0e88cf2321d801acedd2b4f0d7f63735fb732
%global commitdate      20170608
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}
Version:        0
Release:        0.2.%{commitdate}git%{shortcommit}%{?dist}
Summary:        Testing gocheck suites and checkers used across juju projects
License:        LGPLv3
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
%{summary}.

%if 0%{?with_devel}
%package devel
Summary:        %{summary}
BuildArch:      noarch

%if 0%{?with_check}
BuildRequires:  golang(github.com/juju/errors)
BuildRequires:  golang(github.com/juju/loggo)
BuildRequires:  golang(github.com/juju/retry)
BuildRequires:  golang(github.com/juju/utils)
BuildRequires:  golang(github.com/juju/utils/clock)
BuildRequires:  golang(github.com/juju/version)
BuildRequires:  golang(gopkg.in/check.v1)
BuildRequires:  golang(gopkg.in/mgo.v2)
BuildRequires:  golang(gopkg.in/mgo.v2/bson)
BuildRequires:  golang(gopkg.in/yaml.v2)
BuildRequires:  mongodb-server
%endif

Requires:       golang(github.com/juju/errors)
Requires:       golang(github.com/juju/loggo)
Requires:       golang(github.com/juju/retry)
Requires:       golang(github.com/juju/utils)
Requires:       golang(github.com/juju/utils/clock)
Requires:       golang(github.com/juju/version)
Requires:       golang(gopkg.in/check.v1)
Requires:       golang(gopkg.in/mgo.v2)
Requires:       golang(gopkg.in/mgo.v2/bson)
Requires:       golang(gopkg.in/yaml.v2)
Requires:       mongodb-server

Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/checkers) = %{version}-%{release}
Provides:       golang(%{import_path}/filetesting) = %{version}-%{release}
Provides:       golang(%{import_path}/httptesting) = %{version}-%{release}

%description devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test}
%package unit-test-devel
Summary:        Unit tests for %{name} package
BuildArch:      noarch
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:       %{name}-devel = %{version}-%{release}

Requires:       golang(github.com/juju/errors)
Requires:       golang(github.com/juju/loggo)
Requires:       golang(github.com/juju/utils)
Requires:       golang(gopkg.in/check.v1)
Requires:       golang(gopkg.in/mgo.v2)
Requires:       golang(gopkg.in/mgo.v2/bson)

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
%gotest %{import_path}/checkers
%gotest %{import_path}/filetesting
%gotest %{import_path}/httptesting
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENCE
%doc README.md
%endif

%if 0%{?with_unit_test}
%files unit-test-devel -f unit-test.file-list
%license LICENCE
%doc README.md
%endif

%changelog
* Mon Jan 08 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.2.20170608git2fe0e88
- Enable test suite

* Fri Jan 05 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.1.20170608git2fe0e88
- Initial package

