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
%global project         flosch
%global repo            pongo2
# https://github.com/flosch/pongo2
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     gopkg.in/flosch/pongo2.v3
%global gimport_path    %{provider_prefix}
%global commit          5e81b817a0c48c1c57cdf1a9056cf76bdee02ca9
%global commitdate      20141028
%global shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           golang-gopkg-%{project}-%{repo}-v3
Version:        3
Release:        0.1.%{commitdate}git%{shortcommit}%{?dist}
Summary:        Django-syntax like template-engine for Go
License:        MIT
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
BuildRequires: golang(gopkg.in/check.v1)
%endif

Requires:      golang(gopkg.in/check.v1)

Provides:      golang(%{import_path}) = %{version}-%{release}

Obsoletes:     golang-gopkg-flosch-pongo2-devel <= 3-0.1.git5e81b81%{?dist}

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
%autosetup -n %{repo}-%{commit}

%build

%install
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
for file in $(find . -type f -iname "*_test.go" -o -type f -wholename "./template_tests/*"); do
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
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc README.md
%doc docs/*.md
%endif

%if 0%{?with_unit_test}
%files unit-test-devel -f unit-test.file-list
%license LICENSE
%doc README.md
%endif

%changelog
* Wed Jan 17 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3-0.1.20141028git5e81b81
- Cleanup spec file
- Rename to golang-gopkg-flosch-pongo2-v3

* Mon Oct 30 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 3-0.1.git5e81b81
- Change package to v3 API

* Fri Oct 27 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2-0.1.git8b9568e
- Remove sub-package for v3 API
- Rebuild for Fedora 27

* Thu Dec 08 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1-2
- new package built with tito

* Sun Nov 27 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 1-1
- Initial package
