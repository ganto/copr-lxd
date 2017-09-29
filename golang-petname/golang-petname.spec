%if 0%{?fedora} || 0%{?rhel} == 7
%global with_devel 1
# no bundled dependencies so far
%global with_bundled 0
%global with_debug 1
%global with_check 1
%else
%global with_devel 0
# no bundled dependencies so far
%global with_bundled 0
%global with_debug 0
%global with_check 0
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

%global provider        github
%global provider_tld    com
%global project         dustinkirkland
%global repo            golang-petname
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit          de18eb50a5ef51d38e0629d0e4c0fccbd1db1731
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

%global import_path     %{provider_prefix}

Name:           golang-petname
Version:        2.8
Release:        2%{?dist}
Summary:        A utility to generate "pet names"
License:        ASL 2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
A utility to generate "pet names", consisting of a random combination of\n
adverbs, an adjective, and an animal name. These are useful for unique\n
hostnames or container names, for instance.\n
The default packaging contains about 2000 names, 1300 adjectives and\n
4000 adverbs, yielding nearly 10 billion unique combinations, covering over\n
32 bits of unique namespace.\n
As such, PetName tries to follow the tenets of Zooko's triangle: names are\n
human meaningful, decentralized, and secure.

%if 0%{?with_devel} || ! 0%{?with_bundled}
%package -n golang-%{provider}-%{project}-%{repo}-devel
Summary:        %{summary}
BuildArch:      noarch

Provides:       golang(%{import_path}) = %{version}-%{release}

%description -n golang-%{provider}-%{project}-%{repo}-devel
%{summary}

This package contains library source intended for building other packages\n
which use %{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package -n golang-%{provider}-%{project}-%{repo}-unit-test
Summary:        Unit tests for %{name} package
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        golang-%{provider}-%{project}-%{repo}-devel = %{version}-%{release}

%description -n golang-%{provider}-%{project}-%{repo}-unit-test
%{summary}

This package contains unit tests for project providing packages with\n
%{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}

%build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{provider}.%{provider_tld}/%{project}/%{repo}

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

export LDFLAGS="-X %{import_path}/version.GitSHA=%{shortcommit}"
%gobuild -o bin/%{name} %{import_path}/cmd/petname

%install
install -D -p -m 0755 bin/%{name} %{buildroot}%{_bindir}/%{name}

# man-pages
install -D -p -m 0644 %{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

# source codes for building projects
%if 0%{?with_devel} || ! 0%{?with_bundled}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
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
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc *.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%if 0%{?with_devel} || ! 0%{?with_bundled}
%files -n golang-%{provider}-%{project}-%{repo}-devel -f devel.file-list
%license LICENSE
%doc README.md
%dir %{gopath}/src/%{import_path}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files -n golang-%{provider}-%{project}-%{repo}-unit-test -f unit-test.file-list
%license LICENSE
%doc README.md
%endif

%changelog
* Thu Sep 28 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.8-1
- Update to 2.8.

* Wed Dec 07 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.5-2
- new package built with tito

* Sun Nov 27 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.5-1
- Initial package
