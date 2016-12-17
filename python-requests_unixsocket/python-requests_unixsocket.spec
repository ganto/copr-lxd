%global srcname requests_unixsocket
%global gh_owner msabramo
%global gh_name requests-unixsocket

%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

Name:           python-%{srcname}
Version:        0.1.5
Release:        1%{?dist}
Summary:        Use requests to talk HTTP via a UNIX domain socket
License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{gh_name}
Source0:        https://github.com/%{gh_owner}/%{gh_name}/archive/%{version}/%{gh_name}-%{version}.tar.gz
BuildArch:      noarch

%description
%{summary}

%package -n python2-%{srcname}
Summary:        UNIX domain socket HTTP library for Python 2.x
%{?python_provide:%python_provide python2-%{srcname}}
BuildRequires:  python2-devel
BuildRequires:  python2-pbr
BuildRequires:  python-pytest-capturelog
BuildRequires:  python-pytest-pep8
BuildRequires:  python2-requests
BuildRequires:  python2-setuptools
BuildRequires:  python2-urllib3
BuildRequires:  python2-waitress
Requires:       python2-requests
Requires:       python2-urllib3

%description -n python2-%{srcname}
Use requests to talk HTTP via a UNIX domain socket.

Python 2 version.

%if %{with python3}
%package -n     python3-%{srcname}
Summary:        UNIX domain socket HTTP library for Python 3.x
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  python3-pytest-capturelog
BuildRequires:  python3-pytest-pep8
BuildRequires:  python3-requests
BuildRequires:  python3-setuptools
BuildRequires:  python3-urllib3
BuildRequires:  python3-waitress
Requires:       python3-requests
Requires:       python3-urllib3

%description -n python3-%{srcname}
Use requests to talk HTTP via a UNIX domain socket.

Python 3 version.
%endif

%prep
%autosetup -n %{gh_name}-%{version}
# Remove bundled egg-info
rm -rf %{srcname}.egg-info

%build
%py2_build
%if %{with python3}
%py3_build
%endif

%install
%py2_install
%if %{with python3}
%py3_install
%endif

%check
PYTHONPATH=. py.test
%if %{with python3}
PYTHONPATH=. py.test-3
%endif

%files -n python2-%{srcname}
%doc AUTHORS README.rst
%license LICENSE
%{python2_sitelib}/%{srcname}-%{version}-py%{python2_version}.egg-info
%{python2_sitelib}/%{srcname}

%files -n python3-%{srcname}
%doc AUTHORS README.rst
%license LICENSE
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/%{srcname}

%changelog
* Sat Dec 17 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 0.1.5-1
- Initial packaging
