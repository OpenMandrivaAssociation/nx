# most of the descriptions are stolen from the debian package
%global _hardened_build 1
%define _pkglibdir %{_libdir}/nx
%define _pkgdatadir %{_datadir}/nx
%define _pkglibexecdir %{_libexecdir}/nx

%define Werror_cflags %nil

Summary: 	NoMachine NX
Name: 		nx
Version: 	3.5.0
Release: 	%mkrel 1
Source0: 	http://code.x2go.org/releases/source/nx-libs/nx-X11/%{name}-X11-%{version}-2.tar.gz
Source1:	http://code.x2go.org/releases/source/nx-libs/nxagent/nxagent-%{version}-7.tar.gz
Source2:	http://code.x2go.org/releases/source/nx-libs/nxauth/nxauth-%{version}-1.tar.gz
Source4:	http://code.x2go.org/releases/source/nx-libs/nxcompext/nxcompext-%{version}-1.tar.gz
Source5:	http://code.x2go.org/releases/source/nx-libs/nxcompshad/nxcompshad-%{version}-2.tar.gz
Source6:	http://64.34.173.142/download/%{version}/sources/nxwin-%{version}-4.tar.gz
Source7:	http://code.x2go.org/releases/source/nx-libs/nxcomp/nxcomp-%{version}-2.tar.gz
Source8:	http://code.x2go.org/releases/source/nx-libs/nxproxy/nxproxy-%{version}-1.tar.gz
Source9:	http://64.34.173.142/download/%{version}/sources/nxssh-%{version}-2.tar.gz

Source10:	GUUG-Presentation-NX.pdf

# rename libs with nx prefix => allow us to put them in %{_libdir} (from debian)
# rediffed for 2.0
Patch0:		nx-X11-3.1-libdir.patch
Patch1:		nx-X11-fix-format-errors.patch
Patch2:		nxssh-fix-format-errors.patch

Patch3:		nx-3.5.0-optflags.patch
Patch4:		nx-3.5.0-syslibs.patch
Patch5:		http://sources.gentoo.org/cgi-bin/viewvc.cgi/gentoo-x86/net-misc/nx/files/nx-3.5.0-libpng15.patch

License: 	GPLv2+ and MIT
Group: 		Networking/Remote access
URL: 		http://www.nomachine.com/sources.php
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	jpeg-devel
#BuildRequires:	automake1.7, automake1.4
BuildRequires:  pkgconfig(openssl)
BuildRequires:	imake
BuildRequires:	pkgconfig(lbxutil)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(expat)

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
%patch0 -p 0
%patch1 -p 0
%patch2 -p 0
%patch3 -p1
%patch4 -p1
%patch5 -p0

cat <<EOF >>nx-X11/config/cf/host.def
#define UseRpath YES
#define UsrLibDir %{_pkglibdir}
EOF
find nx-X11 -name "*.[ch]" -print0 | xargs -0 chmod -c -x

%build
# documentation explainig how NX works
cp %{SOURCE10} ./

# the build system Sux, or I haven't understand how it works
# We must build all the lib, and somes binaries at the same shot
# because -I ../nxFOO <-- It *sux*

export CFLAGS="%{optflags}"
%ifarch x86_64 ppc64
export CFLAGS="$CFLAGS -fPIC -DPIC"
%endif
export CXXFLAGS="$CFLAGS"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%{?__global_ldflags} -Wl,-rpath,%{_pkglibdir}"

# The commented parts show how the build would proceed step by step.
# This information is important in case someone wants to split this package
# (which would be the proper thing to do).
# Within the commented area the make World invocation does all for
# you. It isn't placed by accident in the middle of the commented
# build instructions, as this is where the X11 libs would be built

# build Compression Library and Proxy
for i in nxcompshad nxcomp nxproxy; do
  pushd $i; ./configure; perl -pi -e "s/CXXFLAGS    = -O3/CXXFLAGS = %{optflags} -fPIC/" Makefile && perl -pi -e "s|LDFLAGS     = |LDFLAGS = -fPIC -L/usr/X11R6/%{_lib}|" Makefile && perl -pi -e "s|LIBS        =   |LIBS        =   -lXext |" Makefile && make clean && make %{?_smp_mflags} CCFLAGS="$CFLAGS"; popd
done
# build X11 Support Libraries and Agents
SHLIBGLOBALSFLAGS="$LDFLAGS" LOCAL_LDFLAGS="$LDFLAGS" make %{?_smp_mflags} -C nx-X11 World
%if 0
# build Extended Compression Library
pushd nxcompext
  ./configure; make %{?_smp_mflags}
popd
%endif
pushd nxssh
./configure --without-zlib-version-check
make %{?_smp_mflags} nxssh
popd

%install
rm -rf %{buildroot}
#create the directory tree
install -d -m 755 %{buildroot}%{_libdir}/pkgconfig
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_includedir}
install -d -m 755 %{buildroot}%{_includedir}/nxcompsh

#----------- nxcomp 
install -m 755 nxcomp/libXcomp.so.* %{buildroot}%{_libdir}
rm -f %{buildroot}%{_libdir}/libXcomp.so.3
ln -s libXcomp.so.3.1.0 %{buildroot}%{_libdir}/libXcomp.so.3

#----------- nxX11
install -m 755 nx-X11/lib/X11/libX11-nx.so.* %{buildroot}%{_libdir}
install -m 755 nx-X11/lib/Xext/libXext-nx.so.*  %{buildroot}%{_libdir}
install -m 755 nx-X11/lib/Xrender/libXrender-nx.so.* %{buildroot}%{_libdir}
install -m 755 nx-X11/programs/Xserver/nxagent %{buildroot}%{_bindir}
rm -f %{buildroot}%{_libdir}/libX11-nx.so.6
ln -s libX11.so.6.2 %{buildroot}%{_libdir}/libX11-nx.so.6
rm -f %{buildroot}%{_libdir}/libXext-nx.so.6
ln -s libXext.so.6.4 %{buildroot}%{_libdir}/libXext-nx.so.6
rm -f %{buildroot}%{_libdir}/libXrender-nx.so.1
ln -s libXrender.so.1.2.2 %{buildroot}%{_libdir}/libXrender-nx.so.1

#----------- nxcompext
install -m 755 nxcompext/libXcompext.so.* %{buildroot}%{_libdir}
rm -f %{buildroot}%{_libdir}/libXcompext.so.3
ln -s libXcompext.so.3.1.0 %{buildroot}%{_libdir}/libXcompext.so.3
install -m 755 nxcompshad/libXcompshad.so.* %{buildroot}%{_libdir}
rm -f %{buildroot}%{_libdir}/libXcompshad.so.3
ln -s libXcompshad.so.3.1.0 %{buildroot}%{_libdir}/libXcompshad.so.3

#----------- nxproxy 
install -m 755 nxproxy/nxproxy %{buildroot}%{_bindir}

#----------- nxssh
install -m 755 nxssh/nxssh %{buildroot}%{_bindir}

%files -n nxproxy
%{_bindir}/nxproxy

%files -n nxagent
%{_bindir}/nxagent

#---------- nxcomp
%files -n %{lib_name_nxcomp}
%{_libdir}/libXcomp.so.*

#---------- nx-x11
%files -n  %{lib_name_nxx11}
%doc GUUG-Presentation-NX.pdf
%{_libdir}/libX11-nx.so.*
%{_libdir}/libXext-nx.so.*
%{_libdir}/libXrender-nx.so.*

#-------- lib xcompext
%files -n  %{lib_name_xcompext}
%{_libdir}/libXcompext.so.*
%{_libdir}/libXcompshad.so.*

#-------- nxssh
%defattr(-,root,root)
%{_bindir}/nxssh
