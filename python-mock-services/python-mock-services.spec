%global pkgname mock-services

%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

Name:           python-%{pkgname}
Version:        0.3
Release:        3%{?dist}
Summary:        Easy way of mocking API Services
License:        MIT
URL:            https://pypi.python.org/pypi/%{pkgname}
Source0:        https://github.com/novafloss/%{pkgname}/archive/%{version}/%{pkgname}-%{version}.tar.gz
BuildArch:      noarch

%description
%{summary}

%package -n python2-%{pkgname}
Summary:        Easy way of mocking API Services for Python 2.x
%{?python_provide:%python_provide python2-%{pkgname}}
BuildRequires:  python2-attrs
BuildRequires:  python2-devel
BuildRequires:  python2-flake8
BuildRequires:  python2-funcsigs
BuildRequires:  python2-nose
BuildRequires:  python2-requests
BuildRequires:  python-requests-mock
BuildRequires:  python2-setuptools
BuildRequires:  python-six

Requires:       python2-attrs
Requires:       python2-funcsigs
Requires:       python-requests-mock

%description -n python2-%{pkgname}
Aims to provide an easy way to mock an entire service
API based on requests-mock and a simple dict definition
of a service. 

Python 2 version.

%if %{with python3}
%package -n     python3-%{pkgname}
Summary:        Easy way of mocking API Services for Python 3.x
%{?python_provide:%python_provide python3-%{pkgname}}
BuildRequires:  python3-attrs
BuildRequires:  python3-devel
BuildRequires:  python3-flake8
BuildRequires:  python3-funcsigs
BuildRequires:  python3-nose
BuildRequires:  python3-requests
BuildRequires:  python3-requests-mock
BuildRequires:  python3-setuptools
BuildRequires:  python3-six

Requires:       python3-attrs
Requires:       python3-funcsigs
Requires:       python3-requests-mock

%description -n python3-%{pkgname}
Aims to provide an easy way to mock an entire service
API based on requests-mock and a simple dict definition
of a service. 

Python 3 version.
%endif

%prep
%autosetup -n %{pkgname}-%{version}

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
PYTHONPATH=. nosetests-%{python2_version}
%if %{with python3}
PYTHONPATH=. nosetests-%{python3_version}
%endif

%files -n python2-%{pkgname}
%doc AUTHORS README.rst
%license LICENSE
%{python2_sitelib}/mock_services-%{version}-py%{python2_version}.egg-info
%{python2_sitelib}/mock_services

%if %{with python3}
%files -n python3-%{pkgname}
%doc AUTHORS README.rst
%license LICENSE
%{python3_sitelib}/mock_services-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/mock_services
%endif

%changelog
* Fri Dec 30 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.3-3
- Rebuild for Python 3.6

* Sun Dec 18 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.3-2
- Fix python-requests-mock dependency definition

* Sun Dec 18 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> - 0.3-1
- Initial packaging
