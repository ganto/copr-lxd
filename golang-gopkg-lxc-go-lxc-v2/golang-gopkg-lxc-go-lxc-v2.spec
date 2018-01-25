%if 0%{?fedora} || 0%{?rhel}
%global with_devel 1
%global with_bundled 0
%global with_debug 0
# Test suite needs permission to start LXC containers
%global with_check 0
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
%global project         lxc
%global repo            go-lxc
# https://github.com/lxc/go-lxc
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     gopkg.in/lxc/go-lxc.v2
%global gimport_path    %{provider_prefix}
%global commit          a7d112aed2f5f57f565d6e557671eeef7e76811c
%global commitdate      20171215
%global shortcommit     %(c=%{commit}; echo ${c:0:7})



Name:           golang-gopkg-%{project}-%{repo}-v2
Version:        2
Release:        0.2.%{commitdate}git%{shortcommit}%{?dist}
Summary:        Go bindings for liblxc
License:        LGPLv2 with exceptions
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
%endif

Requires:      lxc-devel

Provides:      golang(%{import_path}) = %{version}-%{release}

Conflicts:     lxd-devel <= 2.19-2%{?dist}

%description devel
This package implements Go bindings for the LXC C
API (liblxc).

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
# find C source and header files and add them to devel.file-list
for file in $(find . -iname "*.h" -o -iname "*.c") ; do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

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

%gotest %{import_path}
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

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
* Thu Jan 25 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2-0.2.20171215gita7d112a
- Update to commit a7d112a

* Mon Jan 15 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2-0.1.20171109git99ba61b
- Initial package

