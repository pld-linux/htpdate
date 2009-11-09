Summary:	HTTP based time synchronization tool
Summary(pl.UTF-8):	Klient do synchronizacji czasu po HTTP
Name:		htpdate
Version:	1.0.4
Release:	1
License:	GPL
Group:		Daemons
Source0:	http://www.clevervest.com/htp/archive/c/%{name}-%{version}.tar.bz2
# Source0-md5:	a13ec89839c33965794ebf53c4e690db
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

%description -l pl.UTF-8
Protokół HTTP Time Protocol (HTP) jest używany do synchronizacji czasu
systemu z serwerami WWW jako źródłem czasu odniesienia. Program
htpdate synchronizuje czas systemu z sygnaturą czasową (timestamp)
znajdującą się w odpowiedzi serwera WWW. Dokładność jest zazwyczaj
większa niż 0.5 sekundy i rośnie przy korzystaniu z większej liczby
serwerów. Jeżeli wymagana jest większa dokładność, zamiast htpdate
należy użyć pakietu ntp-client.

Htpdate działa także przez serwer proxy.

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
