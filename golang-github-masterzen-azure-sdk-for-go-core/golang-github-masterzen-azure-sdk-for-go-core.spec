%if 0%{?fedora} || 0%{?rhel}
%global with_devel 1
%global with_bundled 0
%global with_debug 0
# unit tests are broken
%global with_check 0
%global with_unit_test 0
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
%global project         masterzen
%global repo            azure-sdk-for-go
# https://github.com/masterzen/azure-sdk-for-go
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}/core
%global commit          ee4f0065d00cd12b542f18f5bc45799e88163b12
%global commitdate      20161016
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}-core
Version:        5.0.0.beta
Release:        0.1.%{commitdate}git%{shortcommit}
Summary:        Microsoft Azure SDK for Go
License:        ASL 2.0
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
%endif

Provides:       golang(%{import_path}/http) = %{version}-%{release}
Provides:       golang(%{import_path}/tls) = %{version}-%{release}

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
Requires:        %{name}-devel = %{version}-%{release}

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
for file in $(find . -iname "*.go" \! -iname "*_test.go" | grep \./core | sed 's/\/core//'); do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav core/$file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go" | grep \.core | sed 's/\/core//'); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav core/$file %{buildroot}/%{gopath}/src/%{import_path}/$file
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

%gotest %{import_path}/http
%gotest %{import_path}/tls
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
* Wed Jan 03 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 5.0.0.beta-0.1.20161016gitee4f006
- Initial package

