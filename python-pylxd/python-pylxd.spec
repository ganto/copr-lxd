%global pkgname pylxd

# RHEL doesn't support python-3
%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

# don't try to build debug package
%global debug_package %{nil}

Name:           python-%{pkgname}
Version:        2.2.4
Release:        2%{?dist}
Summary:        Python library for interacting with LXD REST API

Group:          Development/Languages
License:        ASL 2.0
URL:            https://linuxcontainers.org/lxd
Source0:        https://pypi.python.org/packages/74/4e/8874500407e457d400a80c8b99682e25ea7e9ff9c2109bff831874c45f2f/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch

%description
%{summary}

%package -n python2-%{pkgname}
Summary:        Python 2 library for interacting with LXD REST API
%{?python_provide:%python_provide python2-%{pkgname}}

BuildRequires:  python2-cryptography
BuildRequires:  python2-dateutil
BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python2-requests
BuildRequires:  python2-requests_unixsocket
BuildRequires:  python2-setuptools
BuildRequires:  python-six
BuildRequires:  python2-ws4py
# Required for tests
BuildRequires:  python2-coverage
BuildRequires:  python2-ddt
BuildRequires:  python2-flake8
BuildRequires:  python2-mock
BuildRequires:  python2-mock-services
BuildRequires:  python2-nose

Requires:       python2-cryptography
Requires:       python2-dateutil
Requires:       python2-pbr
Requires:       python2-requests
Requires:       python2-requests_unixsocket
Requires:       python-six
Requires:       python2-ws4py

%description -n python2-%{pkgname}
LXD offers a REST API to remotely manage containers over the network,
using an image based workflow and with support for live migration.

pylxd is a small Python library for interacting the with the
LXD REST API.

This package contains the Python 2 module.

%package        doc
Summary:        Documentation for %{name}
Group:          Documentation
BuildRequires:  python-sphinx

%description    doc
Documentation for %{name}.

%package -n python2-%{pkgname}-tests
Summary:        Tests for the pylxd Python 2 library

Requires:       python2-%{pkgname} = %{version}-%{release}
Requires:       python2-coverage
Requires:       python2-ddt
Requires:       python2-flake8
Requires:       python2-mock
Requires:       python2-mock-services
Requires:       python2-nose

%description -n python2-%{pkgname}-tests
Tests for the pylxd Python 2 library.

%if %{with python3}
%package -n     python3-%{pkgname}
Summary:        Python 3 library for interacting with LXD REST API
%{?python_provide:%python_provide python3-%{pkgname}}

BuildRequires:  python3-cryptography
BuildRequires:  python3-dateutil
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-requests
BuildRequires:  python3-requests_unixsocket
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-ws4py
# Required for tests
BuildRequires:  python3-coverage
BuildRequires:  python3-ddt
BuildRequires:  python3-flake8
BuildRequires:  python3-mock
BuildRequires:  python3-mock-services
BuildRequires:  python3-nose

Requires:       python3-cryptography
Requires:       python3-dateutil
Requires:       python3-pbr
Requires:       python3-requests
Requires:       python3-requests_unixsocket
Requires:       python3-six
Requires:       python3-ws4py

%description -n python3-%{pkgname}
LXD offers a REST API to remotely manage containers over the network,
using an image based workflow and with support for live migration.

pylxd is a small Python library for interacting the with the
LXD REST API.

This package contains the Python 3 module.

%package -n python3-%{pkgname}-tests
Summary:        Tests for the pylxd Python 3 library

Requires:       python3-%{pkgname} = %{version}-%{release}
Requires:       python3-coverage
Requires:       python3-ddt
Requires:       python3-flake8
Requires:       python3-mock
Requires:       python3-mock-services
Requires:       python3-nose

%description -n python3-%{pkgname}-tests
Tests for the pylxd Python 3 library.
%endif

%prep
%autosetup -n %{pkgname}-%{version} -p1

%build
%py2_build
%{__python2} setup.py build_sphinx -b html
%if %{with python3}
%py3_build
%endif

%install
%py2_install
%if %{with python3}
%py3_install
%endif
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.buildinfo

%check
nosetests-%{python2_version} pylxd
%if %{with python3}
nosetests-%{python3_version} pylxd
%endif

%files -n python2-%{pkgname}
%doc AUTHORS README.rst
%license LICENSE
%{python2_sitelib}/%{pkgname}-%{version}-py%{python2_version}.egg-info
%{python2_sitelib}/%{pkgname}
%exclude %{python2_sitelib}/%{pkgname}/tests
%exclude %{python2_sitelib}/%{pkgname}/deprecated/tests

%files doc
%doc doc/build/html
%license LICENSE

%files -n python2-%{pkgname}-tests
%license LICENSE
%{python2_sitelib}/%{pkgname}/tests
%{python2_sitelib}/%{pkgname}/deprecated/tests

%if %{with python3}
%files -n python3-%{pkgname}
%doc AUTHORS README.rst
%license LICENSE
%{python3_sitelib}/%{pkgname}-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/%{pkgname}
%exclude %{python3_sitelib}/%{pkgname}/tests
%exclude %{python3_sitelib}/%{pkgname}/deprecated/tests

%files -n python3-%{pkgname}-tests
%license LICENSE
%{python3_sitelib}/%{pkgname}/tests
%{python3_sitelib}/%{pkgname}/deprecated/tests
%endif

%changelog
* Tue Jul 11 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 2.2.4-2
- Version bump to upstream release pylxd-2.2.4

* Tue Jun 13 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.2.4-1.gitfcc823d
- Add fix for lxc/pylxd#230, build from unmerged/released source

* Fri Mar 24 2017 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.2.3-1
- Version bump to pylxd-2.2.3

* Tue Dec 20 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.2.2-2
- Fix runtime dependencies, fix arch, generate separate test packages

* Mon Dec 19 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.2.2-1
- Initial packaging
