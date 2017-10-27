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
%global with_unit_test 1
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         inconshreveable
%global repo            log15
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit          b105bd37f74e5d9dc7b6ad7806715c7a2b83fd3f
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

%global import_path     gopkg.in/inconshreveable/log15.v2

Name:           golang-gopkg-inconshreveable-log15
Version:        2.11
Release:        0.1%{?dist}
Summary:        Structured, composable logging for Go
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/log15-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if ! 0%{?with_bundled}
BuildRequires:  golang(github.com/mattn/go-colorable)
%endif

%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:        %{summary}
BuildArch:      noarch

%if 0%{?with_check}
BuildRequires:  golang(github.com/mattn/go-colorable)
%endif

Requires:       golang(github.com/mattn/go-colorable)

Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/ext) = %{version}-%{release}
Provides:       golang(%{import_path}/stack) = %{version}-%{release}
Provides:       golang(%{import_path}/term) = %{version}-%{release}

%description devel
Package log15 provides an opinionated, simple toolkit
for best-practice logging in Go (golang) that is both
human and machine readable. It is modeled after the
Go standard library's io and net/http packages and is
an alternative to the standard library's log package.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test}
%package unit-test-devel
Summary:         Unit tests for %{name} package
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if 0%{?with_check}
BuildRequires:  golang(github.com/mattn/go-colorable)
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test-devel
Package log15 provides an opinionated, simple toolkit
for best-practice logging in Go (golang) that is both
human and machine readable. It is modeled after the
Go standard library's io and net/http packages and is
an alternative to the standard library's log package.

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n log15-%{commit}

%build

%install
# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
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
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test.file-list
done
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc README.md
%dir %{gopath}/src/%{import_path}
%endif

%if 0%{?with_unit_test}
%files unit-test-devel -f unit-test.file-list
%license LICENSE
%doc README.md
%endif

%changelog
* Fri Oct 27 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.11-0.1
- Remove sub-package for v1 API
- Rebuild for Fedora 27

* Fri Dec 09 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1-2
- new package built with tito

* Sun Nov 27 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 1-1
- Initial package
