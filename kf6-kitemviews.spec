#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	6.10
%define		qtver		5.15.2
%define		kfname		kitemviews

Summary:	Set of item views extending the Qt model-view framework
Name:		kf6-%{kfname}
Version:	6.10.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	882a45b7e070a8e498a475d2b6de94b1
URL:		https://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6Widgets >= %{qtver}
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KItemViews includes a set of views, which can be used with item
models. It includes views for categorizing lists and to add search
filters to flat and hierarchical lists.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Widgets-devel >= %{qtver}
Requires:	cmake >= 3.16
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6ItemViews.so.6
%attr(755,root,root) %{_libdir}/libKF6ItemViews.so.*.*
%attr(755,root,root) %{_libdir}/qt6/plugins/designer/kitemviews6widgets.so
%{_datadir}/qlogging-categories6/kitemviews.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KItemViews
%{_libdir}/cmake/KF6ItemViews
%{_libdir}/libKF6ItemViews.so
