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

%global v1_commit       a127215f557c6b7b673e4bcf12ecf3c093ead09a
%global v1_shortcommit  %(c=%{v1_commit}; echo ${c:0:7})
%global v1_import_path  gopkg.in/inconshreveable/log15.v1

%global devel_main      golang-gopkg-inconshreveable-log15-devel-v2

Name:           golang-gopkg-inconshreveable-log15
Version:        1
Release:        2%{?dist}
Summary:        Structured, composable logging for Go
License:        APL-2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/log15-%{shortcommit}.tar.gz
Source1:        https://%{provider_prefix}/archive/%{v1_commit}/log15-%{v1_commit}.tar.gz

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

Provides:       golang(%{v1_import_path}) = %{version}-%{release}
Provides:       golang(%{v1_import_path}/ext) = %{version}-%{release}
Provides:       golang(%{v1_import_path}/term) = %{version}-%{release}

%description devel
Package log15 provides an opinionated, simple toolkit
for best-practice logging in Go (golang) that is both
human and machine readable. It is modeled after the
Go standard library's io and net/http packages and is
an alternative to the standard library's log package.

This package contains library source intended for
building other packages which use import path with
%{v1_import_path} prefix.

%package devel-v2
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

%description devel-v2
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
%package unit-test
Summary:         Unit tests for %{name} package
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if 0%{?with_check}
BuildRequires:  golang(github.com/mattn/go-colorable)
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}
Requires:        %{name}-devel-v2 = %{version}-%{release}

%description unit-test
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
%setup -q -n log15-%{v1_commit} -T -b 1

%build

%install
# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path}/
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{v1_import_path}/$file
    echo "%%{gopath}/src/%%{v1_import_path}/$file" >> v1_devel.file-list
done
pushd ../log15-%{commit}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> ../log15-%{v1_commit}/devel.file-list
done
popd
%endif

# testing files for this project
%if 0%{?with_unit_test}
install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path}/
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    install -d -p %{buildroot}/%{gopath}/src/%{v1_import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{v1_import_path}/$file
    echo "%%{gopath}/src/%%{v1_import_path}/$file" >> unit-test.file-list
done
pushd ../log15-%{commit}
for file in $(find . -iname "*_test.go"); do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> ../log15-%{v1_commit}/unit-test.file-list
done
popd
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}
pushd ../log15-%{v1_commit}
# test fail:
# --- FAIL: TestCtx: (0.00s)
#         log15_test.go:80: Expecting Ctx tansformed into 6 ctx args, got 0: []
#%gotest %{v1_import_path}
popd
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%if 0%{?with_devel}
%files devel -f v1_devel.file-list
%license LICENSE
%doc README.md
%dir %{gopath}/src/%{v1_import_path}

%files devel-v2 -f devel.file-list
%license LICENSE
%doc README.md
%dir %{gopath}/src/%{import_path}
%endif

%if 0%{?with_unit_test}
%files unit-test -f unit-test.file-list
%license LICENSE
%doc README.md
%endif

%changelog
* Fri Dec 09 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1-2
- new package built with tito

* Sun Nov 27 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 1-1
- Initial package
