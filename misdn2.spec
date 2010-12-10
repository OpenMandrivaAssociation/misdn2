%define name    misdn2
%define version 1.6
%define	epoch	2
%define libname %mklibname %{name}
%define snap    20090906
%define release %mkrel %{snap}.2

%define build_qmisdnwatch 0
%{?_without_qmisdnwatc:	%global build_qmisdnwatch 0}
%{?_with_qmisdnwatch:	%global build_qmisdnwatch 1}

%define libname2 %mklibname misdn

Summary:	Modular ISDN (mISDN) version 2
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		%{epoch}
Group:		System/Libraries
License:	GPL
URL:		http://www.misdn.org/index.php/Main_Page
Source0:	http://www.linux-call-router.de/download/lcr-%{version}/mISDNuser_%{snap}.tar.gz
Provides:	misdn
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
mISDN supports a complete BRI and PRI ETSI compliant DSS1 protocol stack for
the TE mode and for the NT mode. It is the successor of the "old" isdn4linux
subsystem, in particular its "HiSax" family of drivers. It has growing
support for the interface cards of hisax and additionally supports
the cool HFCmulti chip based cards

%package -n	%{libname}
Summary:	Modular ISDN (mISDN) libraries
Group:		System/Libraries
Epoch:		%{epoch}
Provides:	%{libname2}

%description -n	%{libname}
Modular ISDN (mISDN) is the new ISDN stack of the linux kernel
version 2.6.

This package provides the shared mISDN libraries.

%package -n	%{libname}-devel
Summary:	Static library and header files for the mISDN libraries
Group:		Development/C
Provides:	%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	lib%{name}-devel = %{epoch}:%{version}-%{release}
Provides:	misdn-devel, libmisdn-devel, %{libname2}-devel
Provides:	misdn2-devel, libmisdn2-devel
Requires:	%{libname} = %{epoch}:%{version}-%{release}
Epoch:		%{epoch}

%description -n	%{libname}-devel
Modular ISDN (mISDN) is the new ISDN stack of the linux kernel
version 2.6.

This package provides shared and static libraries and header
files.

%if %{build_qmisdnwatch}
%package -n	qmisdnwatch
Summary:	Modular ISDN (mISDN) watch tool
Group:		System/Configuration/Networking 
Epoch:		1
Requires:	qt4, misdn2 = 2:
BuildRequires:	qt4-devel

%description -n	qmisdnwatch
This tool is combining mISDNuser cmdline tools in unified Qt4 GUI 
and it monitoring D/B-Channel state with colored bullets.
%endif

%prep

%setup -q -n mISDNuser

# fix strange perms
find . -type f -exec chmod 644 {} \;
find . -type d -exec chmod 755 {} \;

# cvs cleanup
for i in `find . -type d -name CVS` `find . -type d -name .svn` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
	if [ -e "$i" ]; then rm -r $i; fi >&/dev/null
done

%build
CFLAGS="${CFLAGS:-%optflags}" ; export CFLAGS
LDFLAGS="${LDFLAGS}"  ; export LDFLAGS
%make INSTALL_PREFIX=%{buildroot} INSTALL_LIBDIR=%{_libdir}

%if %{build_qmisdnwatch}
pushd guitools/qmisdnwatch
	qmake
	%make
popd
%endif

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall INSTALL_PREFIX=%{buildroot} INSTALL_LIBDIR=%{_libdir}

%if %{build_qmisdnwatch}
cp guitools/qmisdnwatch/qmisdnwatch %{buildroot}/%{_bindir}/
install -d %{buildroot}/usr/share/icons/qmisdnwatch
install guitools/qmisdnwatch/res/*.png %{buildroot}/usr/share/icons/qmisdnwatch
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/mISDNuser/*.*
%{_libdir}/*.a

%if %{build_qmisdnwatch}
%files -n qmisdnwatch
%defattr(-,root,root)
%{_bindir}/qmisdnwatch
%{_iconsdir}/qmisdnwatch/*.png
%endif

