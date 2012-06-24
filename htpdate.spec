Summary:	HTTP based time synchronization tool
Summary(pl):	Klient do synchronizacji czasu po HTTP
Name:		htpdate
Version:	0.9.1
Release:	1
License:	GPL
Group:		Daemons
Source0:	http://www.clevervest.com/htp/archive/c/%{name}-%{version}.tar.bz2
# Source0-md5:	2a883e833ab81c83852e71b3fdd2ea3f
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.clevervest.com/htp/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts >= 0.4.0.10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The HTTP Time Protocol (HTP) is used to synchronize a computer's time
with web servers as reference time source. Htpdate will synchronize
your computer's time by extracting timestamps from HTTP headers found
in web servers responses. Htpdate can be used as a daemon, to keep
your computer synchronized. Accuracy of htpdate is usually better than
0.5 seconds (even better with multiple servers). If this is not good
enough for you, try the ntpd package.

Install the htp package if you need tools for keeping your system's
time synchronized via the HTP protocol. Htpdate works also through
proxy servers.

%description -l pl
Protok� HTTP Time Protocol (HTP) jest u�ywany do synchronizacji czasu
systemu z serwerami WWW jako �r�d�em czasu odniesienia. Program
htpdate synchronizuje czas systemu z sygnatur� czasow� (timestamp)
znajduj�c� si� w odpowiedzi serwera WWW. Dok�adno�� jest zazwyczaj
wi�ksza ni� 0.5 sekundy i ro�nie przy korzystaniu z wi�kszej liczby
serwer�w. Je�eli wymagana jest wi�ksza dok�adno��, zamiast htpdate
nale�y u�y� pakietu ntp-client.

Htpdate dzia�a tak�e przez serwer proxy.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,cron.hourly}

install htpdate $RPM_BUILD_ROOT%{_sbindir}/htpdate
gzip -dc htpdate.8.gz > $RPM_BUILD_ROOT%{_mandir}/man8/htpdate.8
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/htpdate
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/htpdate

cat > $RPM_BUILD_ROOT/etc/cron.hourly/htpdate <<'EOF'
#!/bin/sh
exec /sbin/service htpdate cronsettime
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add htpdate
%service htpdate restart

%preun
if [ "$1" = "0" ]; then
	%service htpdate stop
	/sbin/chkconfig --del htpdate
fi

%files
%defattr(644,root,root,755)
%doc README Changelog
%attr(754,root,root) /etc/rc.d/init.d/htpdate
%attr(755,root,root) %{_sbindir}/htpdate
%attr(754,root,root) /etc/cron.hourly/htpdate
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/htpdate
%{_mandir}/man8/htpdate.8*
