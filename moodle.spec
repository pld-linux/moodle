# TODO:
# - mark i18n content as lang()
%bcond_with	apache1		# build for work with apache1 conf system
Summary:	Learning management system
Summary(pl):	System zarz±dzania nauczaniem
Name:		moodle
Version:	1.4.2
Release:	0.1
License:	GPL v2
Group:		Applications/Databases/Interfaces
Source0:	http://dl.sourceforge.net/moodle/%{name}-%{version}.tgz
# Source0-md5:	d47201ea1d2d7e38fbd279563ff0f45d
Source1:	%{name}-http.conf
Patch0:		%{name}-config.patch
URL:		http://moodle.org/
Requires:	php-gd
Requires:	php-mysql
Requires:	php-pcre
Requires:	php-session
Requires:	php
%if %{without apache1}
Requires:	apache >= 2
%endif
%if %{with apache1}
Requires:	apache < 2
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_moodledir	%{_datadir}/%{name}
%define		_moodledata	/var/lib/moodle
%define		_sysconfdir	/etc/%{name}

%description
Moodle is a learning management system for producing Internet-based
course Web sites. It is written in PHP and is easy to install and use
on Linux, Windows, Mac OS X, SunOS, BSD, and Netware 6. It has been
designed to support modern pedagogies based on social constructionist
theory, and includes activity modules such as forums, chats,
resources, journals, quizzes, surveys, choices, workshops, glossaries,
lessons, and assignments. It has been translated into over 36
languages, with more on the way. Moodle offers a free alternative to
commercial software such as WebCT or Blackboard, and is being used by
a growing number of universities, schools, and independent teachers
for distance education or to supplement face-to-face teaching.

%description -l pl
Moodle to system zarz±dzania nauczaniem do tworzenia internetowych
serwisów z kursami. Jest napisany w PHP i ³atwy w instalacji oraz
u¿ywaniu pod Linuksem, Windows, MacOS X, SunOS-em, BSD oraz Netware 6.
Zosta³ zaprojektowany do obs³ugi nowoczesnej pedagogiki opartej na
teorii konstrukcjonistów socjalnych, zawiera modu³y aktywno¶ci, takie
jak fora, pogawêdki, zasoby, ¿urnale, quizy, przegl±dy, warsztaty,
s³owniki, lekcje i ustalenia. Zosta³ przet³umaczony na ponad 36
jêzyków, i ci±gle s± dodawane nowe. Moodle oferuje darmow± alternatywê
dla oprogramowania komercyjnego, takiego jak WebCT czy Blackboard, i
jest u¿ywany przez rosn±c± liczbê uniwersytetów, szkó³ oraz
niezale¿nych nauczycieli do zdalnego nauczania lub uzupe³nienia
nauczania bezpo¶redniego.

%prep
%setup -q -n %{name}
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_moodledir},%{_moodledata},%{_sysconfdir}/themes,/etc/httpd/httpd.conf}

# Move docs into proper place:
mv -f auth/README README_auth.txt
mv -f auth/ldap/README-LDAP README-LDAP.txt
mv -f lang/README README_lang.txt
mv -f filter/tex/README.mimetex README_mimetex.txt
mv -f filter/multilang/README.txt README_multilang.txt
mv -f filter/censor/README.txt README_censor.txt
mv -f mod/README.txt README_mod.txt
mv -f mod/chat/README.txt README_mod_chat.txt
mv -f mod/glossary/README.txt README_mod_glossary.txt
mv -f mod/glossary/TODO.txt TODO_mod_glossary.txt
mv -f mod/scorm/README.txt README_mod_scorm.txt
mv -f mod/workshop/todo.txt TODO_mod_workshop.txt
mv -f theme/UPGRADE.txt UPGRADE_theme.txt

# Instalation:
cp -R * $RPM_BUILD_ROOT%{_moodledir}

# Play with configs:
mv -f $RPM_BUILD_ROOT%{_moodledir}/config-dist.php $RPM_BUILD_ROOT%{_sysconfdir}/config.php
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_moodledir}/config.php

THEMES="brightretro cordoroyblue cornflower formal_white garden metal oceanblue poweraid standard standardblue standardgreen standardlogo standardred standardwhite"
for i in $THEMES; do
	mv -f $RPM_BUILD_ROOT%{_moodledir}/theme/$i/config.php $RPM_BUILD_ROOT%{_sysconfdir}/themes/$i.php
	ln -sf %{_sysconfdir}/themes/$i.php $RPM_BUILD_ROOT%{_moodledir}/theme/$i/config.php
	install -d $RPM_BUILD_ROOT%{_sysconfdir}/themes/$i
	ln -sf %{_sysconfdir}/themes/$i $RPM_BUILD_ROOT%{_moodledir}/theme/$i/data
done

# Install apache config:
%if %{without apache1}
	#apache2
	install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/httpd.conf/88_%{name}.conf
%endif
%if %{with apache1}
	#apache 1
	install %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf
%endif

# Final cleanup:
rm -f $RPM_BUILD_ROOT%{_moodledir}/{*.txt,tags,doc/COPYRIGHT.txt}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
	echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
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
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/usr/sbin/apachectl restart 1>&2
		fi
	fi
fi

%files
%defattr(644,root,root,755)
%doc *.txt
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/config.php
%dir %{_sysconfdir}/themes
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/themes/*
%if %{without apache1}
#apache2
%config(noreplace) /etc/httpd/httpd.conf/88_%{name}.conf
%endif
%if %{with apache1}
#apache1
%config(noreplace) /etc/httpd/%{name}.conf
%endif
%dir %{_moodledir}
%{_moodledir}/*.php
%dir %{_moodledir}/auth
%dir %{_moodledir}/auth/db
%dir %{_moodledir}/auth/email
%dir %{_moodledir}/auth/imap
%dir %{_moodledir}/auth/ldap
%dir %{_moodledir}/auth/manual
%dir %{_moodledir}/auth/nntp
%dir %{_moodledir}/auth/none
%dir %{_moodledir}/auth/pop3
%{_moodledir}/auth/*/*.php
%{_moodledir}/auth/*/*.html
%dir %{_moodledir}/admin
%{_moodledir}/admin/*.html
%{_moodledir}/admin/*.php
%dir %{_moodledir}/backup
%{_moodledir}/backup/*.html
%{_moodledir}/backup/*.php
%{_moodledir}/backup/*.txt
%dir %{_moodledir}/backup/db
%{_moodledir}/backup/db/*.php
%{_moodledir}/backup/db/*.sql
%dir %{_moodledir}/blocks
%{_moodledir}/blocks/*
%dir %{_moodledir}/calendar
%{_moodledir}/calendar/*.html
%{_moodledir}/calendar/*.php
%dir %{_moodledir}/course
%{_moodledir}/course/*.php
%{_moodledir}/course/*.html
%dir %{_moodledir}/course/format
%{_moodledir}/course/format/*/*.php
%dir %{_moodledir}/doc
%{_moodledir}/doc/*.css
%{_moodledir}/doc/*.html
%{_moodledir}/doc/*.php
%dir %{_moodledir}/doc/pix
%{_moodledir}/doc/pix/*.jpg
%dir %{_moodledir}/error
%{_moodledir}/error/index.php
%dir %{_moodledir}/files
%{_moodledir}/files/*.php
%dir %{_moodledir}/filter
%dir %{_moodledir}/filter/*
%{_moodledir}/filter/*/*.php
%{_moodledir}/filter/*/*.pl
%{_moodledir}/filter/*/*.pm
%{_moodledir}/filter/*/*.swf
%{_moodledir}/filter/tex/mimetex.linux
# Is it needed? Maybe doc?
%{_moodledir}/filter/mediaplugin/mp3player.fla.zip
%dir %{_moodledir}/lang
%dir %{_moodledir}/lang/*
%{_moodledir}/lang/*/*
%dir %{_moodledir}/lib
%{_moodledir}/lib/*
%dir %{_moodledir}/login
%{_moodledir}/login/*.php
%{_moodledir}/login/*.html
%dir %{_moodledir}/mod
%dir %{_moodledir}/mod/*
%{_moodledir}/mod/*/*
%dir %{_moodledir}/pix
%{_moodledir}/pix/*.gif
%{_moodledir}/pix/*.png
%dir %{_moodledir}/pix/c
%dir %{_moodledir}/pix/f
%dir %{_moodledir}/pix/g
%dir %{_moodledir}/pix/i
%dir %{_moodledir}/pix/s
%dir %{_moodledir}/pix/t
%dir %{_moodledir}/pix/u
%{_moodledir}/pix/*/*.gif
%{_moodledir}/pix/*/*.png
%dir %{_moodledir}/rss
%{_moodledir}/rss/*.php
%dir %{_moodledir}/theme
%{_moodledir}/theme/*
%dir %{_moodledir}/user
%{_moodledir}/user/*.html
%{_moodledir}/user/*.php
%dir %{_moodledir}/user/default
%{_moodledir}/user/default/*.jpg
%{_moodledir}/user/default/*.txt
%dir %{_moodledir}/userpix
%{_moodledir}/userpix/*.php
%attr(771,root,http) %dir %{_moodledata}
