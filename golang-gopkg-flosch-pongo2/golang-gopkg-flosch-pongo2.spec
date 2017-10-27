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
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}

%global commit       8b9568efa76dbade04e58e4b568ff97362183835
%global shortcommit  %(c=%{commit}; echo ${c:0:7})
%global import_path  gopkg.in/flosch/pongo2.v2

Name:           golang-gopkg-flosch-pongo2
Version:        2
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        Django-syntax like template-engine for Go
License:        MIT
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/pongo2-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if 0%{?with_check}
BuildRequires:  golang(gopkg.in/check.v1)
%endif

%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:        Django-syntax like template-engine for Go
BuildArch:      noarch

Provides:       golang(%{import_path}) = %{version}-%{release}

%description devel
Django-syntax like template-engine for Go.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%prep
%setup -q -n pongo2-%{commit}

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
%dir %{gopath}/src/%{import_path}
%endif

%changelog
* Thu Dec 08 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 1-2
- new package built with tito

* Sun Nov 27 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 1-1
- Initial package
