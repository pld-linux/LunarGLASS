#
# Conditional build:
%bcond_with	tests		# build with tests

%define	snap	20160216
%define commit	55f8dd9b8628c0a14772e17be2e90a9ded1a75e5
%define	rel	0.1

%define llvm_version	3.4.2

Summary:	LLVM IR and optimizer for shaders, including front-end adapters for GLSL and SPIR-V and back-end adapter for GLSL
Name:		LunarGLASS
Version:	0
Release:	0.%{snap}.%{rel}
License:	BSD-like
Group:		Libraries
Source0:	https://github.com/LunarG/LunarGLASS/archive/%{commit}/%{name}-%{snap}.tar.gz
# Source0-md5:	d05a3f5a2412d525bb76bf8868ee5c35
Source1:	http://llvm.org/releases/%{llvm_version}/llvm-%{llvm_version}.src.tar.gz
# Source1-md5:	a20669f75967440de949ac3b1bad439c
Patch0:		CMakeLists.patch
URL:		https://github.com/LunarG/LunarGLASS/
BuildRequires:	clang
BuildRequires:	cmake
BuildRequires:	glslang-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LunarGLASS is an LLVM-based shader-compiler stack available to
open-source developers. It brings a new approach by splitting the
common shared intermediate representation (IR) into two levels; the
top level is completely platform independent while the bottom level is
dynamically tailorable to different families of architecture. Both
levels still lend themselves to portability and sharing of tools.
Together, they solve the problem of having a standard portable IR
without being biased toward a specific class of target architecture.

LunarGLASS is a long-term compiler stack architecture, based on
establishing common intermediate representations (IRs) allowing
modularity between stack layers. Each source-language front end would
benefit from a common set of high- and mid-level optimizations, as
would each back end, without the need to invent additional IRs. The
short-term goal is to leverage investments in existing IRs while the
long-term goal is to reduce the number of IRs and not require
optimization difficulties caused by losing information going through
an IR.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries

%description devel
Header files for %{name} library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki %{name}.

%prep
%setup -qn %{name}-%{commit}
%patch0 -p1

cd Core/LLVM/llvm-3.4
tar -x --strip-components=1 --skip-old-files -f %{SOURCE1}
cd ../../..

%build
cd Core/LLVM/llvm-3.4
install -d build
cd build
../%%configure

%{__make}
%{__make} install prefix=%{_prefix}/local DESTDIR=`pwd`/install

cd ../../../..

install -d build
cd build
%cmake \
	-DGLSLANGINCLUDES=%{_includedir}/glslang \
	-DGLSLANGLIBS=%{_libdir} \
	../
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}}

cd build
%{__make} install

cp -p install/bin/LunarGOO $RPM_BUILD_ROOT%{_bindir}
cp -p install/lib/*.a $RPM_BUILD_ROOT%{_libdir}

cd ..

for path in $(find * -name '*.h') ; do
	install -D $path $RPM_BUILD_ROOT%{_includedir}/%{name}/$path
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Readme.md Todo.txt
%attr(755,root,root) %{_bindir}/LunarGOO

%files devel
%defattr(644,root,root,755)
%{_libdir}/*.a
%{_includedir}/%{name}
