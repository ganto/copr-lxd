%global srcname ws4py
%global gh_owner Lawouach
%global gh_name WebSocket-for-Python

%if 0%{?rhel} && 0%{?rhel} <= 7
%bcond_with python3
%else
%bcond_without python3
%endif

Name:           python-%{srcname}
Version:        0.4.2
Release:        1%{?dist}
Summary:        WebSocket client and server library for Python
License:        BSD
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://github.com/%{gh_owner}/%{gh_name}/archive/%{version}/%{gh_name}-%{version}.tar.gz
# Thanks to https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=834921
Patch0:         ws4py-0.3.4-Fix-tests.patch
BuildArch:      noarch

%description
%{summary}

%package -n python2-%{srcname}
Summary:        WebSocket client and server library for Python 2.x
%{?python_provide:%python_provide python2-%{srcname}}
BuildRequires:  python-cherrypy
BuildRequires:  python2-devel
BuildRequires:  python2-gevent
BuildRequires:  python2-mock
BuildRequires:  python2-nose
BuildRequires:  python2-setuptools
BuildRequires:  python2-tornado

%if 0%{?fedora}
Suggests:       python-cherrypy
Suggests:       python2-gevent
Suggests:       python2-tornado
%endif

%description -n python2-%{srcname}
Python library providing an implementation of the
WebSocket protocol defined in RFC 6455.

Python 2 version.

%if %{with python3}
%package -n     python3-%{srcname}
Summary:        WebSocket client and server library for Python 3.x
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-cherrypy
BuildRequires:  python3-devel
BuildRequires:  python3-gevent
BuildRequires:  python3-mock
BuildRequires:  python3-nose
BuildRequires:  python3-setuptools
BuildRequires:  python3-tornado

%if 0%{?fedora}
Suggests:       python3-cherrypy
Suggests:       python3-gevent
Suggests:       python3-tornado
%endif

%description -n python3-%{srcname}
Python library providing an implementation of the
WebSocket protocol defined in RFC 6455.

Python 3 version.
%endif

%prep
# There are some modules which are specific to Python 3. Therefore we
# must use two different build directories.
%if %{with python3}
%setup -q -T -a 0 -c -n python3-%{srcname}
pushd %{gh_name}-%{version}
# Obviously the patches also have to be applied individually
%patch0 -p1
popd
cd ..
%endif
%setup -q -T -a 0 -c -n python2-%{srcname}
pushd %{gh_name}-%{version}
%patch0 -p1
popd

%build
pushd %{gh_name}-%{version}
%{__python2} setup.py build
popd
%if %{with python3}
pushd ../python3-%{srcname}/%{gh_name}-%{version}
%{__python3} setup.py build
popd
%endif

%install
pushd %{gh_name}-%{version}
%py2_install
popd
%if %{with python3}
pushd ../python3-%{srcname}/%{gh_name}-%{version}
%py3_install
popd
%endif

%check
pushd %{gh_name}-%{version}
nosetests-2
popd
%if %{with python3}
pushd ../python3-%{srcname}/%{gh_name}-%{version}
nosetests-3
popd
%endif

%files -n python2-%{srcname}
%doc %{gh_name}-%{version}/README.md
%license %{gh_name}-%{version}/LICENSE
%{python2_sitelib}/%{srcname}-%{version}-py%{python2_version}.egg-info
%{python2_sitelib}/%{srcname}

%if %{with python3}
%files -n python3-%{srcname}
%doc %{gh_name}-%{version}/README.md
%license %{gh_name}-%{version}/LICENSE
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info
%{python3_sitelib}/%{srcname}
%endif

%changelog
* Fri Dec 30 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.3.4-2
- Rebuild for Python 3.6

* Sat Dec 17 2016 Reto Gantenbein <reto.gantenbein@linuxmonk.ch> 0.3.4-1
- Initial packaging
