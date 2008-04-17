# most of the descriptions are stolen from the debian package

%define name nx
%define version 3.2.0
%define release %mkrel 1

Summary: 	NoMachine NX
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source0: 	nx-X11-%{version}-1.tar.bz2
Source1:	nxagent-%{version}-3.tar.bz2
Source2:	nxauth-%{version}-1.tar.bz2
Source4:	nxcompext-%{version}-1.tar.bz2
Source5:	nxcompshad-%{version}-1.tar.bz2
Source6:	nxwin-%{version}-3.tar.bz2
Source7:	nxcomp-%{version}-6.tar.bz2
Source8:	nxproxy-%{version}-1.tar.bz2
Source9:	nxssh-%{version}-1.tar.bz2

Source10:	GUUG-Presentation-NX.pdf

# rename libs with nx perfix => allow us to put them in %{_libdir} (from debian)
# rediffed for 2.0
Patch0:		nx-X11-3.1-libdir.patch

Patch3:		nxviewer-2.0-lib.patch
#allow compilation for x86_64
Patch4:		nx-X11-2.0-x86_64.patch

License: 	MIT/GPL
Group: 		Networking/Remote access
Url: 		http://www.nomachine.com/sources.php
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	X11-devel libfontconfig-devel
BuildRequires:	zlib-devel
BuildRequires:	libpng-devel
BuildRequires:	libjpeg-devel
BuildRequires:	automake1.7, automake1.4
BuildRequires:  openssl-devel
BuildRequires:	imake

%description
NoMachine NX is the next-generation X compression and roundtrip
suppression scheme. It can operate remote X11 sessions over 
56k modem dialup links or anything better. 

####################
#   xcompext lib   #
####################
%define lib_name_orig_xcompext libxcompext
%define lib_major_xcompext 3
%define lib_name_xcompext %mklibname xcompext %{lib_major_xcompext}
%package -n     %{lib_name_xcompext}
Summary:	Xcompext/Xcompshad library for NX
Group:		System/Libraries
Provides:	xcompext = %{version}-%{release}
Provides:	xcompshad = %{version}-%{release}

%description -n %{lib_name_xcompext}
Xcompext and Xcompshad library needed by the NX framework

%post -n %{lib_name_xcompext} -p /sbin/ldconfig
%postun -n %{lib_name_xcompext}
/sbin/ldconfig


###############
# nx-X11 lib  #
###############
%define lib_name_orig_nxx11 libnxX11
%define lib_major_nxx11 0
%define lib_name_nxx11 %mklibname nxX11_ %{lib_major_nxx11}
%package -n     %{lib_name_nxx11}
Summary:	Nx-X11 lib for NX
Group:		System/Libraries
Provides:	nxX11 = %{version}-%{release}

%description -n %{lib_name_nxx11}
NX-X11 lib for the NX framework

%post -n %{lib_name_nxx11} -p /sbin/ldconfig
%postun -n %{lib_name_nxx11}
/sbin/ldconfig

##########
# nxcomp #
##########
%define lib_name_orig_nxcomp libxcomp
%define lib_major_nxcomp 3
%define lib_name_nxcomp %mklibname xcomp %{lib_major_nxcomp}

%package -n	%{lib_name_nxcomp}
Summary:	Xcomp library for NX
Group:		System/Libraries
Provides:	xcomp = %{version}-%{release}

%description -n %{lib_name_nxcomp}
Xcomp library for NX subsystem

%post -n %{lib_name_nxcomp} -p /sbin/ldconfig
%postun -n %{lib_name_nxcomp}
/sbin/ldconfig

#############
# nxdesktop #
#############

%package -n	nxdesktop
Summary:	NX rdesktop agent
Group:		Networking/Remote access

%description -n nxdesktop
The nxdesktop is a rdesktop agent, for connecting to windows machines through
a nx tunnel.

############
# nxviewer #
############
%package -n	nxviewer	
Summary:	NX vnc agent
Group:		Networking/Remote access

%description -n nxviewer
The nxviewer is a vnc agent, for connecting to vnc servers (windows or linux)
through a nx tunnel.

###########
# nxproxy #
###########
%package -n	nxproxy
Summary:	Provide the protocol compression and caching part of the NX scheme
Group:		Networking/Remote access

%description -n nxproxy
The nxproxy runs on the X server side of the wire and thus accompanies 
the nxagent running on X client side. It provides the protocol
compression and caching part of the NX scheme.

###########
# nxagent #
###########
%package -n 	nxagent
Summary:	NX X server based on Xnest
Group:		Networking/Remote access

%description -n nxagent
The nxagent is an X server based on Xnest, but modified
for the purpose of reducing roundtrips over high-latency
networks significantly. It is run on the client side of X,
that is, on the machine where X clients run. It connects,
over the wire, to your regular X server, possibly through nxproxy.

#########
# nxssh #
#########

%package -n	nxssh
Summary:	NX ssh client 
Group:		Networking/Remote access

%description -n nxssh
Nx ssh client

%prep
%setup -q -c -a 1 -a 2 -a 4 -a 5 -a 6 -a 7 -a 8 -a 9
%patch0
#%patch3
#%patch4

%build
# documentation explainig how NX works
cp %{SOURCE10} ./

# the build system Sux, or I haven't understand how it works
# We must build all the lib, and somes binaries at the same shot
# because -I ../nxFOO <-- It *sux*

#-------- Build nxcomp

pushd nxcomp
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
export CXXFLAGS="$RPM_OPT_FLAGS -fPIC"
export CPPFLAGS="$RPM_OPT_FLAGS -fPIC"
%configure
# configure script doesn't care of CFLAGS
perl -pi -e "s/CXXFLAGS    = -O3/CXXFLAGS = $RPM_OPT_FLAGS -fPIC/" Makefile
perl -pi -e "s/LDFLAGS     = /LDFLAGS = -fPIC/" Makefile
perl -pi -e "s/CCFLAGS\s+=/CCFLAGS = $RPM_OPT_FLAGS -fPIC/" Makefile
make clean
%make
popd

#-------- build nxcompext lib
pushd nxcompext
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
export CXXFLAGS="$RPM_OPT_FLAGS -fPIC"
export CPPFLAGS="$RPM_OPT_FLAGS -fPIC"
%configure
perl -pi -e "s/CXXFLAGS    = -O3/CXXFLAGS = $RPM_OPT_FLAGS -fPIC/" Makefile
perl -pi -e "s|LDFLAGS     = |LDFLAGS = -fPIC -L/usr/X11R6/%{_lib}|" Makefile
make clean
%make
popd

#-------- build nxcompshad lib
pushd nxcompshad
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
export CXXFLAGS="$RPM_OPT_FLAGS -fPIC"
export CPPFLAGS="$RPM_OPT_FLAGS -fPIC"
%configure
perl -pi -e "s/CXXFLAGS    = -O3/CXXFLAGS = $RPM_OPT_FLAGS -fPIC/" Makefile
perl -pi -e "s|LDFLAGS     = |LDFLAGS = -fPIC -L/usr/X11R6/%{_lib}|" Makefile
make clean
%make
popd

#-------- Build nx X11 libs
pushd nx-X11
make World
popd

#-------- build nxproxy
pushd nxproxy
%configure
%make
popd

#-------- build nxssh
pushd nxssh
%configure
%make
popd 

%install
rm -rf $RPM_BUILD_ROOT
#create the directory tree
install -d -m 755 $RPM_BUILD_ROOT%{_libdir}/pkgconfig
install -d -m 755 $RPM_BUILD_ROOT%{_bindir}
install -d -m 755 $RPM_BUILD_ROOT%{_includedir}
install -d -m 755 $RPM_BUILD_ROOT%{_includedir}/nxcompsh

#----------- nxcomp 
install -m 755 nxcomp/libXcomp.so.* $RPM_BUILD_ROOT%{_libdir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libXcomp.so.3
ln -s libXcomp.so.3.1.0 $RPM_BUILD_ROOT%{_libdir}/libXcomp.so.3

#----------- nxX11
install -m 755 nx-X11/lib/X11/libX11-nx.so.* $RPM_BUILD_ROOT%{_libdir}
install -m 755 nx-X11/lib/Xext/libXext-nx.so.*  $RPM_BUILD_ROOT%{_libdir}
install -m 755 nx-X11/lib/Xrender/libXrender-nx.so.* $RPM_BUILD_ROOT%{_libdir}
install -m 755 nx-X11/programs/Xserver/nxagent $RPM_BUILD_ROOT%{_bindir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libX11-nx.so.6
ln -s libX11.so.6.2 $RPM_BUILD_ROOT%{_libdir}/libX11-nx.so.6
rm -f $RPM_BUILD_ROOT%{_libdir}/libXext-nx.so.6
ln -s libXext.so.6.4 $RPM_BUILD_ROOT%{_libdir}/libXext-nx.so.6
rm -f $RPM_BUILD_ROOT%{_libdir}/libXrender-nx.so.1
ln -s libXrender.so.1.2.2 $RPM_BUILD_ROOT%{_libdir}/libXrender-nx.so.1

#----------- nxcompext
install -m 755 nxcompext/libXcompext.so.* $RPM_BUILD_ROOT%{_libdir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libXcompext.so.3
ln -s libXcompext.so.3.1.0 $RPM_BUILD_ROOT%{_libdir}/libXcompext.so.3
install -m 755 nxcompshad/libXcompshad.so.* $RPM_BUILD_ROOT%{_libdir}
rm -f $RPM_BUILD_ROOT%{_libdir}/libXcompshad.so.3
ln -s libXcompshad.so.3.1.0 $RPM_BUILD_ROOT%{_libdir}/libXcompshad.so.3

#----------- nxproxy 
install -m 755 nxproxy/nxproxy $RPM_BUILD_ROOT%{_bindir}

#----------- nxssh
install -m 755 nxssh/nxssh $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files -n nxproxy
%defattr(-,root,root)
%{_bindir}/nxproxy

%files -n nxagent
%defattr(-,root,root)
%{_bindir}/nxagent

#---------- nxcomp
%files -n %{lib_name_nxcomp}
%defattr(-,root,root)
%{_libdir}/libXcomp.so.*

#---------- nx-x11
%files -n  %{lib_name_nxx11}
%defattr(-,root,root)
%doc GUUG-Presentation-NX.pdf
%{_libdir}/libX11-nx.so.*
%{_libdir}/libXext-nx.so.*
%{_libdir}/libXrender-nx.so.*

#-------- lib xcompext
%files -n  %{lib_name_xcompext}
%defattr(-,root,root)
%{_libdir}/libXcompext.so.*
%{_libdir}/libXcompshad.so.*

#-------- nxssh
%files -n nxssh
%defattr(-,root,root)
%{_bindir}/nxssh


