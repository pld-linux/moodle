# TODO:
# - mark i18n content as lang()
# - do sth with binary in %{_datadir}
# - use external ZendFramework deps
#
Summary:	Learning management system
Summary(pl.UTF-8):	System zarządzania nauczaniem
Name:		moodle
Version:	2.0.2
Release:	0.1
License:	GPL v2
Group:		Applications/Databases/Interfaces
Source0:	http://download.moodle.org/stable20/%{name}-%{version}.tgz
# Source0-md5:	c9ff3ca4aa6f8470993e331c3e59ed33
Source1:	http://www.forkosh.com/mimetex.zip
# Source1-md5:	56e66e59c0c78ca824ac0a2c54565539
Source2:	%{name}-http.conf
Patch0:		%{name}-config.patch
URL:		http://moodle.org/
BuildRequires:	unzip
Requires:	php(gd)
Requires:	php(mysql)
Requires:	php(pcre)
Requires:	php(session)
Requires:	webapps
Requires:	webserver
Requires:	webserver(php)
Suggests:	php-ctype
Suggests:	php-curl
Suggests:	php-iconv
Suggests:	php-mbstring
Suggests:	php-openssl
Suggests:	php-tokenizer
Suggests:	php-xmlrpc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_moodledir	%{_datadir}/%{name}
%define		_moodledata	/var/lib/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

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

%description -l pl.UTF-8
Moodle to system zarządzania nauczaniem do tworzenia internetowych
serwisów z kursami. Jest napisany w PHP i łatwy w instalacji oraz
używaniu pod Linuksem, Windows, MacOS X, SunOS-em, BSD oraz Netware 6.
Został zaprojektowany do obsługi nowoczesnej pedagogiki opartej na
teorii konstrukcjonistów socjalnych, zawiera moduły aktywności, takie
jak fora, pogawędki, zasoby, żurnale, quizy, przeglądy, warsztaty,
słowniki, lekcje i ustalenia. Został przetłumaczony na ponad 36
języków, i ciągle są dodawane nowe. Moodle oferuje darmową alternatywę
dla oprogramowania komercyjnego, takiego jak WebCT czy Blackboard, i
jest używany przez rosnącą liczbę uniwersytetów, szkół oraz
niezależnych nauczycieli do zdalnego nauczania lub uzupełnienia
nauczania bezpośredniego.

%prep
%setup -q -n %{name}
%patch0 -p1
mkdir mimetex
unzip %{SOURCE1} -d mimetex/

# Move docs into proper place:
mv -f admin/xmldb/README.txt README_admin_xmldb.txt
mv -f auth/cas/README-CAS README_auth_CAS.txt
mv -f auth/fc/Readme.txt README_auth_fc.txt
mv -f auth/ldap/README-LDAP README_auth_LDAP.txt
mv -f auth/README.txt README_auth.txt
mv -f auth/shibboleth/README.txt README_auth_shibboleth.txt
mv -f backup/bb/README.txt README_bb.txt
mv -f course/format/README.txt README_course_format.txt
mv -f filter/censor/README.txt README_filter_censor.txt
mv -f filter/mediaplugin/flvplayer.README.txt README_fliter_flvplayer.txt
mv -f filter/multilang/README.txt README_filter_multilang.txt
mv -f filter/tex/README.mimetex README_filter_tex_mimetex.txt
mv -f filter/tex/readme_moodle.txt README_filter_tex.txt
mv -f install/README.txt README_install.txt
mv -f iplookup/README.txt README_iplookup.txt
mv -f lang/README.txt README_lang.txt
mv -f local/readme.txt README_local.txt
mv -f mod/chat/README.txt README_mod_chat.txt
mv -f mod/glossary/README.txt README_mod_glossary.txt
mv -f mod/glossary/TODO.txt TODO_mod_glossary.txt
mv -f mod/README.txt README_mod.txt
mv -f mod/scorm/README.txt README_mod_scorm.txt
mv -f question/format/README.txt README_question_format.txt
mv -f question/format/webct/TODO.txt TODO_question_format_webct.txt
mv -f repository/README.txt README_repository.txt
mv -f search/README.txt README_search.txt

%build
cd mimetex
%{__cc} %{rpmcflags} -DAA mimetex.c gifsave.c -lm -o mimetex.cgi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_moodledir},%{_moodledata},%{_sysconfdir}/themes,/etc/httpd/httpd.conf}

# Instalation:
cp -R * $RPM_BUILD_ROOT%{_moodledir}

# We don't need mimetex dir
%{__rm} -r $RPM_BUILD_ROOT%{_moodledir}/mimetex
# But we need our binary
%{__rm} $RPM_BUILD_ROOT%{_moodledir}/filter/tex/mimetex.*
install mimetex/mimetex.cgi $RPM_BUILD_ROOT%{_moodledir}/filter/tex/mimetex.linux

# Play with configs:
mv -f $RPM_BUILD_ROOT%{_moodledir}/config-dist.php $RPM_BUILD_ROOT%{_sysconfdir}/config.php
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_moodledir}/config.php

for d in $RPM_BUILD_ROOT%{_moodledir}/theme/* ; do
	[ -d $d ] || continue
	i=`basename $d`
	mv -f $RPM_BUILD_ROOT%{_moodledir}/theme/$i/config.php $RPM_BUILD_ROOT%{_sysconfdir}/themes/$i.php
	ln -sf %{_sysconfdir}/themes/$i.php $RPM_BUILD_ROOT%{_moodledir}/theme/$i/config.php
	install -d $RPM_BUILD_ROOT%{_sysconfdir}/themes/$i
	ln -sf %{_sysconfdir}/themes/$i $RPM_BUILD_ROOT%{_moodledir}/theme/$i/data
done

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf

# Final cleanup:
%{__rm} $RPM_BUILD_ROOT%{_moodledir}/{*.txt,tags}

find $RPM_BUILD_ROOT%{_moodledir} -type d -printf "%%%%dir \"%{_moodledir}/%%P\"\n" >files.list
find $RPM_BUILD_ROOT%{_moodledir} \( ! -type d -a ! -name 'mimetex.linux' \) -printf "\"%{_moodledir}/%%P\"\n" >>files.list

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerpostun -- moodle < 1.6.3
if [ -f /home/services/httpd/html/squirrel/config/config.php.rpmsave ]; then
	echo "Moving old config file to %{_sysconfdir}/config.php"
	mv -f %{_sysconfdir}/config.php{,.rpmnew}
	mv -f /home/services/httpd/html/squirrel/config/config.php.rpmsave %{_sysconfdir}/config.php
fi

if [ -f /etc/squirrelmail/config.php.rpmsave ]; then
	echo "Moving old config file to %{_sysconfdir}/config.php"
	mv -f %{_sysconfdir}/config.php{,.rpmnew}
	mv -f /etc/squirrelmail/config.php.rpmsave %{_sysconfdir}/config.php
fi

# nuke very-old config location (this mostly for Ra)
if [ -f /etc/httpd/httpd.conf ]; then
	sed -i -e "/^Include.*squirrelmail.conf/d" /etc/httpd/httpd.conf
	httpd_reload=1
fi

# migrate from httpd (apache2) config dir
if [ -f /etc/httpd/squirrelmail.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	mv -f /etc/httpd/squirrelmail.conf.rpmsave %{_sysconfdir}/httpd.conf
	httpd_reload=1
fi

if [ -d /etc/httpd/webapps.d ]; then
	/usr/sbin/webapp register httpd %{_webapp}
	httpd_reload=1
fi

# place new config location, as trigger puts config only on first install, do it here
if [ -L /etc/httpd/httpd.conf/99_squirrelmail.conf ]; then
	rm -f /etc/httpd/httpd.conf/99_squirrelmail.conf
	/usr/sbin/webapp register httpd %{_webapp}
	httpd_reload=1
fi

if [ "$httpd_reload" ]; then
	%service -q httpd reload
fi

%files -f files.list
%defattr(644,root,root,755)
%doc *.txt

%dir %attr(750,root,http) %{_sysconfdir}
%dir %attr(750,root,http) %{_sysconfdir}/themes
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/themes/*

%attr(755,root,root) %{_moodledir}/filter/tex/mimetex.linux
%attr(771,root,http) %dir %{_moodledata}
