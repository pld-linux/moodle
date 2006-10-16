# TODO:
# - mark i18n content as lang()
# - do sth with i386 binary in %{_datadir}
#
Summary:	Learning management system
Summary(pl):	System zarz�dzania nauczaniem
Name:		moodle
Version:	1.6.3
Release:	0.1
License:	GPL v2
Group:		Applications/Databases/Interfaces
Source0:	http://download.moodle.org/stable16/%{name}-%{version}.tgz
# Source0-md5:	2f9f3fcf83ab0f18c409f3a48e07eae2
Source1:	%{name}-http.conf
Patch0:		%{name}-config.patch
URL:		http://moodle.org/
Requires:	php
Requires:	php-gd
Requires:	php-mysql
Requires:	php-pcre
Requires:	php-session
Requires:	webapps
Requires:	webserver
BuildArch:	noarch
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

%description -l pl
Moodle to system zarz�dzania nauczaniem do tworzenia internetowych
serwis�w z kursami. Jest napisany w PHP i �atwy w instalacji oraz
u�ywaniu pod Linuksem, Windows, MacOS X, SunOS-em, BSD oraz Netware 6.
Zosta� zaprojektowany do obs�ugi nowoczesnej pedagogiki opartej na
teorii konstrukcjonist�w socjalnych, zawiera modu�y aktywno�ci, takie
jak fora, pogaw�dki, zasoby, �urnale, quizy, przegl�dy, warsztaty,
s�owniki, lekcje i ustalenia. Zosta� przet�umaczony na ponad 36
j�zyk�w, i ci�gle s� dodawane nowe. Moodle oferuje darmow� alternatyw�
dla oprogramowania komercyjnego, takiego jak WebCT czy Blackboard, i
jest u�ywany przez rosn�c� liczb� uniwersytet�w, szk� oraz
niezale�nych nauczycieli do zdalnego nauczania lub uzupe�nienia
nauczania bezpo�redniego.

%prep
%setup -q -n %{name}
%patch0 -p1

# Move docs into proper place:
mv -f auth/README README_auth.txt
mv -f auth/cas/README-CAS README_auth_CAS.txt
mv -f auth/fc/Readme.txt README_auth_fc.txt
mv -f auth/ldap/README-LDAP README_auth_LDAP.txt
mv -f auth/shibboleth/README.txt README_auth_shibboleth.txt
mv -f backup/bb/README.txt README_bb.txt
mv -f blog/README.txt README_blog.txt
mv -f blog/TODO.txt TODO_blog.txt
mv -f course/format/README.txt README_course_format.txt
mv -f filter/censor/README.txt README_filter_censor.txt
mv -f filter/mediaplugin/flvplayer.README.txt README_fliter_flvplayer.txt
mv -f filter/multilang/README.txt README_filter_multilang.txt
mv -f filter/tex/README.mimetex README_filter_tex_mimetex.txt
mv -f iplookup/README.txt README_iplookup.txt
mv -f iplookup/ipatlas/README README_iplookup_ipatlas.txt
mv -f iplookup/ipatlas/MOODLECHANGES MOODLECHANGES_iplookup_ipatlas.txt
mv -f iplookup/ipatlas/README.MOODLE.txt README_MOODLE_iplookup_ipatlas.txt
mv -f lang/README.txt README_lang.txt
mv -f mod/README.txt README_mod.txt
mv -f mod/chat/README.txt README_mod_chat.txt
mv -f mod/glossary/README.txt README_mod_glossary.txt
mv -f mod/glossary/TODO.txt TODO_mod_glossary.txt
mv -f mod/scorm/README.txt README_mod_scorm.txt
mv -f question/format/README.txt README_question_format.txt
mv -f question/format/webct/TODO.txt TODO_question_format_webct.txt
mv -f theme/UPGRADE.txt UPGRADE_theme.txt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_moodledir},%{_moodledata},%{_sysconfdir}/themes,/etc/httpd/httpd.conf}

# Instalation:
cp -R * $RPM_BUILD_ROOT%{_moodledir}

# Play with configs:
mv -f $RPM_BUILD_ROOT%{_moodledir}/config-dist.php $RPM_BUILD_ROOT%{_sysconfdir}/config.php
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_moodledir}/config.php

THEMES="cornflower formal_white metal oceanblue orangewhite orangewhitepda standard standardblue standardgreen standardlogo standardred standardwhite wood"
for i in $THEMES; do
	mv -f $RPM_BUILD_ROOT%{_moodledir}/theme/$i/config.php $RPM_BUILD_ROOT%{_sysconfdir}/themes/$i.php
	ln -sf %{_sysconfdir}/themes/$i.php $RPM_BUILD_ROOT%{_moodledir}/theme/$i/config.php
	install -d $RPM_BUILD_ROOT%{_sysconfdir}/themes/$i
	ln -sf %{_sysconfdir}/themes/$i $RPM_BUILD_ROOT%{_moodledir}/theme/$i/data
done

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf

# Final cleanup:
rm -f $RPM_BUILD_ROOT%{_moodledir}/{*.txt,tags,doc/COPYRIGHT.txt}
rm -f $RPM_BUILD_ROOT%{_moodledir}/filter/tex/mimetex.{darwin,exe}

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

%files
%defattr(644,root,root,755)
%doc *.txt

%dir %attr(750,root,http) %{_sysconfdir}
%dir %attr(750,root,http) %{_sysconfdir}/themes
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/themes/*

%dir %{_moodledir}
%{_moodledir}/*.php
%dir %{_moodledir}/auth
%dir %{_moodledir}/auth/cas
%dir %{_moodledir}/auth/db
%dir %{_moodledir}/auth/email
%dir %{_moodledir}/auth/fc
%dir %{_moodledir}/auth/imap
%dir %{_moodledir}/auth/ldap
%dir %{_moodledir}/auth/manual
%dir %{_moodledir}/auth/nntp
%dir %{_moodledir}/auth/none
%dir %{_moodledir}/auth/pam
%dir %{_moodledir}/auth/pop3
%dir %{_moodledir}/auth/shibboleth
%{_moodledir}/auth/*.html
%{_moodledir}/auth/*/*.php
%{_moodledir}/auth/*/*.html
%dir %{_moodledir}/admin
%{_moodledir}/admin/*.html
%{_moodledir}/admin/*.php
%{_moodledir}/admin/*.xml
%dir %{_moodledir}/admin/report
%dir %{_moodledir}/admin/report/*
%{_moodledir}/admin/report/*/*.php
%dir %{_moodledir}/backup
%{_moodledir}/backup/*.html
%{_moodledir}/backup/*.php
%{_moodledir}/backup/*.txt
%dir %{_moodledir}/backup/bb
%{_moodledir}/backup/bb/*.inc
%{_moodledir}/backup/bb/*.php
%{_moodledir}/backup/bb/*.xsl
%dir %{_moodledir}/backup/db
%{_moodledir}/backup/db/*.php
%{_moodledir}/backup/db/*.sql
%{_moodledir}/backup/db/*.xml
%dir %{_moodledir}/blocks
%{_moodledir}/blocks/*
%dir %{_moodledir}/blog
%{_moodledir}/blog/*.html
%{_moodledir}/blog/*.php
%dir %{_moodledir}/calendar
%{_moodledir}/calendar/*.html
%{_moodledir}/calendar/*.php
%dir %{_moodledir}/course
%{_moodledir}/course/*.php
%{_moodledir}/course/*.html
%dir %{_moodledir}/course/format
%dir %{_moodledir}/course/format/*
%{_moodledir}/course/format/*/*.php
%dir %{_moodledir}/course/import
%dir %{_moodledir}/course/import/*
%{_moodledir}/course/import/*/*.php
%dir %{_moodledir}/course/report
%dir %{_moodledir}/course/report/*
%{_moodledir}/course/report/*/*.php
%dir %{_moodledir}/doc
%{_moodledir}/doc/*.css
%{_moodledir}/doc/*.html
%{_moodledir}/doc/*.php
%dir %{_moodledir}/doc/pix
%{_moodledir}/doc/pix/*.jpg
%{_moodledir}/doc/pix/*.png
#dir %{_moodledir}/enrol
%{_moodledir}/enrol/
%dir %{_moodledir}/error/
%{_moodledir}/error/index.php
%dir %{_moodledir}/files
%{_moodledir}/files/*.php
%dir %{_moodledir}/filter
%dir %{_moodledir}/filter/*
%{_moodledir}/filter/*/*.html
%{_moodledir}/filter/*/*.php
%{_moodledir}/filter/*/*.pl
%{_moodledir}/filter/*/*.pm
%{_moodledir}/filter/*/*.swf
%{_moodledir}/filter/tex/mimetex.linux
# Is it needed? Maybe doc?
%{_moodledir}/filter/mediaplugin/mp3player.fla.zip
%{_moodledir}/filter/mediaplugin/flvplayer.fla.zip
%dir %{_moodledir}/grade
%{_moodledir}/grade/*
%dir %{_moodledir}/iplookup
%dir %{_moodledir}/iplookup/hostip
%dir %{_moodledir}/iplookup/ipatlas
%dir %{_moodledir}/iplookup/ipatlas/languages
%{_moodledir}/iplookup/*.php
%{_moodledir}/iplookup/hostip/*.php
%{_moodledir}/iplookup/ipatlas/*.inc
%{_moodledir}/iplookup/ipatlas/*.txt
%{_moodledir}/iplookup/ipatlas/*.jpg
%{_moodledir}/iplookup/ipatlas/*.gif
%{_moodledir}/iplookup/ipatlas/*.php
%{_moodledir}/iplookup/ipatlas/*.css
%{_moodledir}/iplookup/ipatlas/languages/*.inc
%dir %{_moodledir}/lang
%dir %{_moodledir}/lang/*
%{_moodledir}/lang/*/*
%dir %{_moodledir}/lib
%{_moodledir}/lib/*
%dir %{_moodledir}/login
%{_moodledir}/login/*.php
%{_moodledir}/login/*.html
%dir %{_moodledir}/message
%{_moodledir}/message/*
%dir %{_moodledir}/mod
%dir %{_moodledir}/mod/*
%{_moodledir}/mod/*/*
%dir %{_moodledir}/my
%{_moodledir}/my/*.php
%dir %{_moodledir}/pix
%{_moodledir}/pix/*.gif
%{_moodledir}/pix/*.png
%{_moodledir}/pix/*.php
%dir %{_moodledir}/pix/a
%dir %{_moodledir}/pix/c
%dir %{_moodledir}/pix/f
%dir %{_moodledir}/pix/g
%dir %{_moodledir}/pix/i
%dir %{_moodledir}/pix/m
%dir %{_moodledir}/pix/s
%dir %{_moodledir}/pix/t
%dir %{_moodledir}/pix/u
%{_moodledir}/pix/*/*
%dir %{_moodledir}/question
%{_moodledir}/question/*.php
%{_moodledir}/question/*.html
%dir %{_moodledir}/question/format
%dir %{_moodledir}/question/format/*
%dir %{_moodledir}/question/format/qti2/templates
%dir %{_moodledir}/question/type
%dir %{_moodledir}/question/type/calculated
%dir %{_moodledir}/question/type/datasetdependent
%dir %{_moodledir}/question/type/description
%dir %{_moodledir}/question/type/essay
%dir %{_moodledir}/question/type/match
%dir %{_moodledir}/question/type/missingtype
%dir %{_moodledir}/question/type/multianswer
%dir %{_moodledir}/question/type/multichoice
%dir %{_moodledir}/question/type/numerical
%dir %{_moodledir}/question/type/random
%dir %{_moodledir}/question/type/randomsamatch
%dir %{_moodledir}/question/type/rqp
%dir %{_moodledir}/question/type/shortanswer
%dir %{_moodledir}/question/type/truefalse
%dir %{_moodledir}/question/type/*/db
%{_moodledir}/question/type/*.php
%{_moodledir}/question/type/*.html
%{_moodledir}/question/type/*/*.php
%{_moodledir}/question/type/*/*.html
%{_moodledir}/question/type/*/*.gif
%{_moodledir}/question/type/*/db/*
%{_moodledir}/question/format/*/*.xml
%{_moodledir}/question/format/*/*.txt
%{_moodledir}/question/format/*/*.php
%{_moodledir}/question/format/*/*.css
%{_moodledir}/question/format/qti2/templates/*.tpl
%dir %{_moodledir}/rss
%{_moodledir}/rss/*
%dir %{_moodledir}/sso
%dir %{_moodledir}/sso/hive
%{_moodledir}/sso/hive/*
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
