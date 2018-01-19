# If any of the following macros should be set otherwise,
# you can wrap any of them with the following conditions:
# - %%if 0%%{centos} == 7
# - %%if 0%%{?rhel} == 7
# - %%if 0%%{?fedora} == 23
# Or just test for particular distribution:
# - %%if 0%%{centos}
# - %%if 0%%{?rhel}
# - %%if 0%%{?fedora}
#
# Be aware, on centos, both %%rhel and %%centos are set. If you want to test
# rhel specific macros, you can use %%if 0%%{?rhel} && 0%%{?centos} == 0 condition.
# (Don't forget to replace double percentage symbol with single one in order to apply a condition)

# Generate devel rpm
%global with_devel 1
# Build project from bundled dependencies
%global with_bundled 0
# Build with debug info rpm
%global with_debug 0
# Run tests in check section
%global with_check 1
# Generate unit-test rpm
%global with_unit_test 1

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         stretchr
%global repo            testify
# https://github.com/stretchr/testify
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          b91bfb9ebec76498946beb6af7c0230c7cc7ba6c
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}
Version:        1.2.0
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        Tools for testifying that your code will behave as you intend
License:        MIT
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
Thou Shalt Write Tests

Go code (golang) set of packages that provide many tools for testifying that
your code will behave as you intend.

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check}
BuildRequires: golang(github.com/stretchr/objx)
BuildRequires: golang(github.com/davecgh/go-spew/spew)
BuildRequires: golang(github.com/pmezard/go-difflib/difflib)
%endif

Requires:      golang(github.com/stretchr/objx)
Requires:      golang(github.com/davecgh/go-spew/spew)
Requires:      golang(github.com/pmezard/go-difflib/difflib)

Provides:      golang(%{import_path}) = %{version}-%{release}
Provides:      golang(%{import_path}/assert) = %{version}-%{release}
Provides:      golang(%{import_path}/http) = %{version}-%{release}
Provides:      golang(%{import_path}/mock) = %{version}-%{release}
Provides:      golang(%{import_path}/require) = %{version}-%{release}
Provides:      golang(%{import_path}/suite) = %{version}-%{release}

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test}
%package unit-test
Summary:         Unit tests for %{name} package

%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}

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
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/Godeps/_workspace:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}
%gotest %{import_path}/assert
%gotest %{import_path}/mock
%gotest %{import_path}/require
%gotest %{import_path}/suite
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%dir %{gopath}/src/%{import_path}
%endif

%if 0%{?with_unit_test}
%files unit-test -f unit-test.file-list
%license LICENSE
%doc README.md
%endif

%changelog
* Tue Sep 12 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.1.4-0.1.git69483b4
- Update to upstream v1.1.4
  resolves: #1490397

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.11.git976c720
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.10.git976c720
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Mar 16 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.0-0.9.git976c720
- Bump to upstream 976c720a22c8eb4eb6a0b4348ad85ad12491a506
  related: #1246684

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.8.git089c718
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 17 2016 Jan Chaloupka <jchaloup@redhat.com> - 1.0-0.7.git089c718
- Polish the spec file
  related: #1246684

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.6.git089c718
- https://fedoraproject.org/wiki/Changes/golang1.7

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.5.git089c718
- https://fedoraproject.org/wiki/Changes/golang1.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.4.git089c718
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 11 2015 jchaloup <jchaloup@redhat.com> - 1.0-0.3.git089c718
- Add missing license in unit-test, BR of devel can be uncommented out
  relates: #1246684

* Mon Aug 10 2015 Fridolin Pokorny <fpokorny@redhat.com> - 1.0-0.2.git089c718
- Update spec file to spec-2.0
  relates: #1246684

* Fri Jul 24 2015 jchaloup <jchaloup@redhat.com> - 1.0-0.1.git089c718
- Bump to upstream 089c7181b8c728499929ff09b62d3fdd8df8adff
  resolves: #1246684

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.8.gite4ec815
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 06 2015 jchaloup <jchaloup@redhat.com> - 0-0.7.gite4ec815
- update URL to point to github repository
  related: #1141872

* Thu Mar 05 2015 jchaloup <jchaloup@redhat.com> - 0-0.6.gite4ec815
- Bump to upstream e4ec8152c15fc46bd5056ce65997a07c7d415325
  related: #1141872

* Thu Oct 23 2014 jchaloup <jchaloup@redhat.com> - 0-0.5.gitd6577e0
- Bump to upstream d6577e08ec30538639ac0ea38b562b6f250e9055
- Spec file polishing to follow go draft
  related: #1141872

* Mon Sep 15 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.3.gitda775f0
- preserve timestamps of copied files

* Wed Aug 06 2014 Adam Miller <maxamillion@fedoraproject.org> - 0-0.2.gitda775f0
- Fix up devel package listing

* Wed Aug 06 2014 Adam Miller <maxamillion@fedoraproject.org> - 0-0.1.gitda775f0
- First package for Fedora.
