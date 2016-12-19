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
Version:        2.2.2
Release:        1%{?dist}
Summary:        Python bindings for LXD
License:        ASL 2.0
URL:            https://linuxcontainers.org/lxd
Source0:        https://github.com/lxc/%{pkgname}/archive/%{version}/%{pkgname}-%{version}.tar.gz

%description
Python library for interacting with LXD REST API.

%package -n python2-%{pkgname}
Summary:        Python 2.x bindings for LXD
%{?python_provide:%python_provide python2-%{pkgname}}
BuildRequires:  python2-babel
BuildRequires:  python2-coverage
BuildRequires:  python2-cryptography
BuildRequires:  python2-dateutil
BuildRequires:  python2-ddt
BuildRequires:  python2-devel
BuildRequires:  python2-flake8
BuildRequires:  python2-mock
BuildRequires:  python2-mock-services
BuildRequires:  python2-nose
BuildRequires:  python2-pbr
BuildRequires:  python2-requests
BuildRequires:  python2-requests_unixsocket
BuildRequires:  python2-setuptools
BuildRequires:  python-six
BuildRequires:  python2-ws4py

Requires:       python2-babel
Requires:       python2-cryptography
Requires:       python2-dateutil
Requires:       python2-requests
Requires:       python2-requests_unixsocket
Requires:       python-six
Requires:       python2-ws4py

%description -n python2-%{pkgname}
Python library for interacting with LXD REST API.

Python 2 version.

%if %{with python3}
%package -n     python3-%{pkgname}
Summary:        Python 3.x bindings for LXD
%{?python_provide:%python_provide python3-%{pkgname}}
BuildRequires:  python3-babel
BuildRequires:  python3-coverage
BuildRequires:  python3-cryptography
BuildRequires:  python3-dateutil
BuildRequires:  python3-ddt
BuildRequires:  python3-devel
BuildRequires:  python3-flake8
BuildRequires:  python3-mock
BuildRequires:  python3-mock-services
BuildRequires:  python3-nose
BuildRequires:  python3-pbr
BuildRequires:  python3-requests
BuildRequires:  python3-requests_unixsocket
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-ws4py

Requires:       python3-babel
Requires:       python3-cryptography
Requires:       python3-dateutil
Requires:       python3-requests
Requires:       python3-requests_unixsocket
Requires:       python3-six
Requires:       python3-ws4py

%description -n python3-%{pkgname}
Python library for interacting with LXD REST API.

Python 3 version.
%endif

%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch
BuildRequires:  python-sphinx
Requires:       %{name} = %{version}-%{release}

%description    doc
Documentation for %{name}.

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
# unfortunately pbr will also install the tests and doesn't support
# excluding files, therefore they will be removed manually
rm -rf %{buildroot}%{python2_sitelib}/%{pkgname}/{tests,deprecated/tests}
%if %{with python3}
%py3_install
rm -rf %{buildroot}%{python3_sitelib}/%{pkgname}/{tests,deprecated/tests}
%endif

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

%if %{with python3}
%files -n python3-%{pkgname}
%doc AUTHORS README.rst
%license LICENSE
%{python3_sitelib}/%{pkgname}-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/%{pkgname}
%endif

%files doc
%doc doc/build/html
%license LICENSE

%changelog
* Mon Dec 19 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 2.2.2-1
- Initial packaging
