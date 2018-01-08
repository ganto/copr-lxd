%if 0%{?fedora} || 0%{?rhel}
%global with_devel 1
%global with_bundled 0
%global with_debug 0
# disable tests for now due to circular dependencies
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
%global project         juju
%global repo            utils
# https://github.com/juju/utils
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          9b65c33e54c793d74a4ed99c15111c44faddb8e4
%global commitdate      20171025
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}
Version:        0
Release:        0.1.%{commitdate}git%{shortcommit}%{?dist}
Summary:        General utility functions
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
BuildRequires:  golang(github.com/juju/cmd)
BuildRequires:  golang(github.com/juju/errors)
BuildRequires:  golang(github.com/juju/httpprof)
BuildRequires:  golang(github.com/juju/httprequest)
BuildRequires:  golang(github.com/juju/loggo)
BuildRequires:  golang(github.com/juju/mutex)
BuildRequires:  golang(github.com/juju/testing)
BuildRequires:  golang(github.com/juju/testing/checkers)
BuildRequires:  golang(github.com/juju/testing/filetesting)
BuildRequires:  golang(github.com/juju/testing/httptesting)
BuildRequires:  golang(github.com/julienschmidt/httprouter)
BuildRequires:  golang(github.com/masterzen/winrm)
BuildRequires:  golang(golang.org/x/crypto/pbkdf2)
BuildRequires:  golang(gopkg.in/check.v1)
BuildRequires:  golang(gopkg.in/errgo.v1)
BuildRequires:  golang(gopkg.in/juju/names.v2)
BuildRequires:  golang(gopkg.in/mgo.v2)
BuildRequires:  golang(gopkg.in/tomb.v1)
BuildRequires:  golang(gopkg.in/yaml.v2)
%endif

Requires:       golang(github.com/juju/cmd)
Requires:       golang(github.com/juju/errors)
Requires:       golang(github.com/juju/httpprof)
Requires:       golang(github.com/juju/httprequest)
Requires:       golang(github.com/juju/loggo)
Requires:       golang(github.com/juju/mutex)
Requires:       golang(github.com/masterzen/winrm)
Requires:       golang(golang.org/x/crypto/pbkdf2)
Requires:       golang(gopkg.in/errgo.v1)
Requires:       golang(gopkg.in/mgo.v2)
Requires:       golang(gopkg.in/tomb.v1)
Requires:       golang(gopkg.in/yaml.v2)

Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/arch) = %{version}-%{release}
Provides:       golang(%{import_path}/bzr) = %{version}-%{release}
Provides:       golang(%{import_path}/cache) = %{version}-%{release}
Provides:       golang(%{import_path}/cert) = %{version}-%{release}
provides:       golang(%{import_path}/clock) = %{version}-%{release}
provides:       golang(%{import_path}/clock/monotonic) = %{version}-%{release}
Provides:       golang(%{import_path}/debugstatus) = %{version}-%{release}
Provides:       golang(%{import_path}/deque) = %{version}-%{release}
Provides:       golang(%{import_path}/du) = %{version}-%{release}
Provides:       golang(%{import_path}/exec) = %{version}-%{release}
Provides:       golang(%{import_path}/featureflag) = %{version}-%{release}
Provides:       golang(%{import_path}/filepath) = %{version}-%{release}
Provides:       golang(%{import_path}/filestorage) = %{version}-%{release}
Provides:       golang(%{import_path}/fs) = %{version}-%{release}
Provides:       golang(%{import_path}/hash) = %{version}-%{release}
Provides:       golang(%{import_path}/jsonhttp) = %{version}-%{release}
Provides:       golang(%{import_path}/keyvalues) = %{version}-%{release}
Provides:       golang(%{import_path}/mgokv) = %{version}-%{release}
Provides:       golang(%{import_path}/os) = %{version}-%{release}
Provides:       golang(%{import_path}/packaging) = %{version}-%{release}
Provides:       golang(%{import_path}/packaging/commands) = %{version}-%{release}
Provides:       golang(%{import_path}/packaging/config) = %{version}-%{release}
Provides:       golang(%{import_path}/packaging/manager) = %{version}-%{release}
Provides:       golang(%{import_path}/parallel) = %{version}-%{release}
Provides:       golang(%{import_path}/proxy) = %{version}-%{release}
Provides:       golang(%{import_path}/readpass) = %{version}-%{release}
Provides:       golang(%{import_path}/registry) = %{version}-%{release}
Provides:       golang(%{import_path}/series) = %{version}-%{release}
Provides:       golang(%{import_path}/set) = %{version}-%{release}
Provides:       golang(%{import_path}/shell) = %{version}-%{release}
Provides:       golang(%{import_path}/ssh) = %{version}-%{release}
Provides:       golang(%{import_path}/symlink) = %{version}-%{release}
Provides:       golang(%{import_path}/tailer) = %{version}-%{release}
Provides:       golang(%{import_path}/tar) = %{version}-%{release}
Provides:       golang(%{import_path}/uptime) = %{version}-%{release}
Provides:       golang(%{import_path}/voyeur) = %{version}-%{release}
Provides:       golang(%{import_path}/winrm) = %{version}-%{release}
Provides:       golang(%{import_path}/zip) = %{version}-%{release}

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

Requires:       golang(github.com/juju/cmd)
Requires:       golang(github.com/juju/testing)
Requires:       golang(github.com/juju/testing/checkers)
Requires:       golang(github.com/juju/testing/filetesting)
Requires:       golang(github.com/juju/testing/httptesting)
Requires:       golang(github.com/julienschmidt/httprouter)
Requires:       golang(gopkg.in/check.v1)
Requires:       golang(gopkg.in/errgo.v1)
Requires:       golang(gopkg.in/juju/names.v2)
Requires:       golang(gopkg.in/mgo.v2)

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
%gotest %{import_path}/arch
%gotest %{import_path}/bzr
%gotest %{import_path}/cache
%gotest %{import_path}/cert
%gotest %{import_path}/clock/monotonic
%gotest %{import_path}/debugstatus
%gotest %{import_path}/deque
%gotest %{import_path}/exec
%gotest %{import_path}/featureflag
%gotest %{import_path}/filepath
%gotest %{import_path}/filestorage
%gotest %{import_path}/fs
%gotest %{import_path}/hash
%gotest %{import_path}/jsonhttp
%gotest %{import_path}/keyvalues
%gotest %{import_path}/mgokv
%gotest %{import_path}/os
%gotest %{import_path}/packaging/commands
%gotest %{import_path}/packaging/config
%gotest %{import_path}/packaging/manager
%gotest %{import_path}/parallel
%gotest %{import_path}/proxy
%gotest %{import_path}/registry
%gotest %{import_path}/series
%gotest %{import_path}/set
%gotest %{import_path}/shell
%gotest %{import_path}/ssh
%gotest %{import_path}/symlink
%gotest %{import_path}/tailer
%gotest %{import_path}/tar
%gotest %{import_path}/voyeur
%gotest %{import_path}/winrm
%gotest %{import_path}/zip
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
* Mon Jan 08 2018 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0-0.1.20171025git9b65c33
- Initial package
