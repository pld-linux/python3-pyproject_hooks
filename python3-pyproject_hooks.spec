# Conditional build:
%bcond_without	doc	# API documentation
%bcond_without	tests	# unit tests

%define		module	pyproject_hooks
Summary:	Wrappers to call pyproject.toml-based build backend hooks
Name:		python3-%{module}
Version:	1.2.0
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.debian.net/pyproject_hooks/%{module}-%{version}.tar.gz
# Source0-md5:	ed3dd1b984339e83e35f676d7169c192
URL:		https://pypi.org/project/pyproject-hooks/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.2
%if %{with tests}
#BuildRequires:	python3-
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
# or
BuildRequires:	python3-tox
%endif
# replace with other requires if defined in setup.py
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a low-level library for calling build-backends in
pyproject.toml-based project. It provides the basic functionality to
help write tooling that generates distribution files from Python
projects.

%package apidocs
Summary:	API documentation for Python %{module} module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona %{module}
Group:		Documentation

%description apidocs
API documentation for Python %{module} module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%{__python3} -m build --wheel --no-isolation --outdir build-3

%if %{with tests}
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
rm -rf docs/_build/html/_sources

# or

%{_bindir}/tox -e docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__python3} -m installer --destdir=$RPM_BUILD_ROOT build-3/*.whl

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
