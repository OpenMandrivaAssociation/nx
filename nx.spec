
%define srcname %{name}-libs

# most of the descriptions are stolen from the debian package
%global _hardened_build 1
%define _pkglibdir %{_libdir}/nx
%define _pkgdatadir %{_datadir}/nx
%define _pkglibexecdir %{_libexecdir}/nx

%define Werror_cflags %nil

Summary: 	NoMachine NX
Name: 		nx
Version: 	3.5.0.33
Release: 	1
Source0: 	http://code.x2go.org/releases/source/%{srcname}/%{srcname}-%{version}-full.tar.gz

Source10:	GUUG-Presentation-NX.pdf

License: 	GPLv2+ and MIT
Group: 		Networking/Remote access
URL: 		http://www.nomachine.com/sources.php
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(xdamage)
BuildRequires:	jpeg-devel
BuildRequires:  pkgconfig(openssl)
BuildRequires:	pkgconfig(lbxutil)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(libtirpc)

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
%setup -q -n %{srcname}-%{version}
%apply_patches

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
export LDFLAGS="%{?__global_ldflags} -Wl,-rpath,%{_pkglibdir} -ltirpc"

# The commented parts show how the build would proceed step by step.
# This information is important in case someone wants to split this package
# (which would be the proper thing to do).
# Within the commented area the make World invocation does all for
# you. It isn't placed by accident in the middle of the commented
# build instructions, as this is where the X11 libs would be built

make CDEBUGFLAGS="$CFLAGS -I/usr/include/tirpc" LOCAL_LDFLAGS="$LDFLAGS" SHLIBGLOBALSFLAGS="$LDFLAGS"

%install
rm -rf %{buildroot}
#create the directory tree
install -d -m 755 %{buildroot}%{_libdir}/pkgconfig
install -d -m 755 %{buildroot}%{_bindir}
install -d -m 755 %{buildroot}%{_includedir}
install -d -m 755 %{buildroot}%{_includedir}/nxcompsh

#----------- nxX11
install -m 0755 \
    nx-X11/lib/X11/libNX_X11.so.*.* \
    nx-X11/lib/Xau/libNX_Xau.so.*.* \
    nx-X11/lib/Xcomposite/libNX_Xcomposite.so.*.* \
    nx-X11/lib/Xdamage/libNX_Xdamage.so.*.* \
    nx-X11/lib/Xdmcp/libNX_Xdmcp.so.*.* \
    nx-X11/lib/Xext/libNX_Xext.so.*.* \
    nx-X11/lib/Xfixes/libNX_Xfixes.so.*.* \
    nx-X11/lib/Xinerama/libNX_Xinerama.so.*.* \
    nx-X11/lib/Xpm/libNX_Xpm.so.*.* \
    nx-X11/lib/Xrandr/libNX_Xrandr.so.*.* \
    nx-X11/lib/Xrender/libNX_Xrender.so.*.* \
    nx-X11/lib/Xtst/libNX_Xtst.so.*.* \
    %{buildroot}%{_libdir}
install -m 0755 nx-X11/programs/Xserver/nxagent \
    %{buildroot}%{_bindir}
install -m 0755 nx-X11/programs/nxauth/nxauth \
    %{buildroot}%{_bindir}

#----------- nxcompext
install -m 0755 nxcomp/libXcomp.so.*.* \
    nxcompext/libXcompext.so.*.* \
    nxcompshad/libXcompshad.so.*.* \
    %{buildroot}%{_libdir}

#----------- nxproxy 
install -m 755 nxproxy/nxproxy %{buildroot}%{_bindir}

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
%{_libdir}/libNX_X11*.so.*
%{_libdir}/libNX_Xau*.so.*
%{_libdir}/libNX_Xcomposite*.so.*
%{_libdir}/libNX_Xdamage*.so.*
%{_libdir}/libNX_Xdmcp*.so.*
%{_libdir}/libNX_Xext*.so.*
%{_libdir}/libNX_Xfixes*.so.*
%{_libdir}/libNX_Xinerama*.so.*
%{_libdir}/libNX_Xpm*.so.*
%{_libdir}/libNX_Xrandr*.so.*
%{_libdir}/libNX_Xrender*.so.*
%{_libdir}/libNX_Xtst*.so.*
%{_bindir}/nxauth

#-------- lib xcompext
%files -n  %{lib_name_xcompext}
%{_libdir}/libXcompext.so.*
%{_libdir}/libXcompshad.so.*

