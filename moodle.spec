# TODO:
# - mark i18n content as lang()
# - apache config and installing them
Summary:	-
Summary(pl):	-
Name:		moodle
Version:	1.3.1
Release:	0.1
License:	GPL
Group:		Applications/Databases/Interfaces
Source0:	http://dl.sourceforge.net/moodle/%{name}-%{version}.tgz
# Source0-md5:	c56112ac3c5867548ff51b063c836cb9
#Source1:	%{name}.conf
URL:		http://moodle.org/
Requires:	php-mysql
Requires:	php-pcre
Requires:	php
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_moodledir	%{_datadir}/%{name}
%define		_sysconfdir	/etc/%{name}

%description
Moodle is a learning management system for producing Internet-based course Web sites. It is written in PHP and is easy to install and use on Linux, Windows, Mac OS X, SunOS, BSD, and Netware 6. It has been designed to support modern pedagogies based on social constructionist theory, and includes activity modules such as forums, chats, resources, journals, quizzes, surveys, choices, workshops, glossaries, lessons, and assignments. It has been translated into over 36 languages, with more on the way. Moodle offers a free alternative to commercial software such as WebCT or Blackboard, and is being used by a growing number of universities, schools, and independent teachers for distance education or to supplement face-to-face teaching.

%prep
%setup -q -n %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_moodledir}/{admin,auth/{db,email,imap,ldap,manual,nntp,none,pop3}} \
	$RPM_BUILD_ROOT{%{_sysconfdir},/etc/httpd}

mv -f auth/README README_auth.txt

install *.php $RPM_BUILD_ROOT%{_moodledir}
install admin/*.{php,html} $RPM_BUILD_ROOT%{_moodledir}/admin
cp -R auth/* $RPM_BUILD_ROOT%{_moodledir}/auth/
#install lang/*.php $RPM_BUILD_ROOT%{_moodledir}/lang
#install css/* $RPM_BUILD_ROOT%{_moodledir}/css
#install libraries/*.{js,php} $RPM_BUILD_ROOT%{_moodledir}/libraries
#install libraries/auth/*.php $RPM_BUILD_ROOT%{_moodledir}/libraries/auth
#install libraries/export/*.php $RPM_BUILD_ROOT%{_moodledir}/libraries/export


mv $RPM_BUILD_ROOT%{_moodledir}/config-dist.php $RPM_BUILD_ROOT%{_sysconfdir}/config.php
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_moodledir}/config.php

#install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*phpMyAdmin.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/phpMyAdmin.conf" >> /etc/httpd/httpd.conf
elif [ -d /etc/httpd/httpd.conf ]; then
	mv -f /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
fi
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
	    rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*phpMyAdmin.conf" /etc/httpd/httpd.conf > \
			etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
		if [ -f /var/lock/subsys/httpd ]; then
		    /usr/sbin/apachectl restart 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc README*
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
#%config(noreplace) %verify(not size mtime md5) /etc/httpd/%{name}.conf
%dir %{_moodledir}
#%{_moodledir}/css
#%{_moodledir}/images
#%{_moodledir}/lang
#%{_moodledir}/libraries
#%{_moodledir}/*.css
#%{_moodledir}/*.html
%{_moodledir}/*.php
%dir %{_moodledir}/auth
%dir %{_moodledir}/auth/*
