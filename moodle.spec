# TODO:
# - mark i18n content as lang()
# - do sth with binary in %{_datadir}
# - use external ZendFramework deps
#
Summary:	Learning management system
Summary(pl.UTF-8):	System zarządzania nauczaniem
Name:		moodle
Version:	1.9.5
Release:	5
License:	GPL v2
Group:		Applications/Databases/Interfaces
Source0:	http://download.moodle.org/stable19/%{name}-%{version}.tgz
# Source0-md5:	41a3258c2f09dbc7b36fec960bcf4e19
Source1:	http://www.forkosh.com/mimetex.zip
# Source1-md5:	9c05d4a3e3fae1242caa7f7a5f65c015
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
mv -f auth/README.txt README_auth.txt
mv -f auth/cas/README-CAS README_auth_CAS.txt
mv -f auth/fc/Readme.txt README_auth_fc.txt
mv -f auth/ldap/README-LDAP README_auth_LDAP.txt
mv -f auth/shibboleth/README.txt README_auth_shibboleth.txt
mv -f backup/bb/README.txt README_bb.txt
mv -f blog/README.txt README_blog.txt
mv -f course/format/README.txt README_course_format.txt
mv -f filter/censor/README.txt README_filter_censor.txt
mv -f filter/mediaplugin/flvplayer.README.txt README_fliter_flvplayer.txt
mv -f filter/multilang/README.txt README_filter_multilang.txt
mv -f filter/tex/README.mimetex README_filter_tex_mimetex.txt
mv -f iplookup/README.txt README_iplookup.txt
mv -f lang/README.txt README_lang.txt
mv -f mod/README.txt README_mod.txt
mv -f mod/chat/README.txt README_mod_chat.txt
mv -f mod/glossary/README.txt README_mod_glossary.txt
mv -f mod/glossary/TODO.txt TODO_mod_glossary.txt
mv -f mod/scorm/README.txt README_mod_scorm.txt
mv -f question/format/README.txt README_question_format.txt
mv -f question/format/webct/TODO.txt TODO_question_format_webct.txt
mv -f theme/UPGRADE.txt UPGRADE_theme.txt

%build
cd mimetex
%{__cc} %{rpmcflags} -DAA mimetex.c gifsave.c -lm -o mimetex.cgi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_moodledir},%{_moodledata},%{_sysconfdir}/themes,/etc/httpd/httpd.conf}

# Instalation:
cp -R * $RPM_BUILD_ROOT%{_moodledir}

# We don't need mimetex dir
rm -rf $RPM_BUILD_ROOT%{_moodledir}/mimetex
# But we need our binary
rm -f $RPM_BUILD_ROOT%{_moodledir}/filter/tex/mimetex.*
install mimetex/mimetex.cgi $RPM_BUILD_ROOT%{_moodledir}/filter/tex/mimetex.linux

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

install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf

# Final cleanup:
rm -f $RPM_BUILD_ROOT%{_moodledir}/{*.txt,tags,doc/COPYRIGHT.txt}

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
%dir %{_moodledir}/auth/mnet
%dir %{_moodledir}/auth/nntp
%dir %{_moodledir}/auth/nologin
%dir %{_moodledir}/auth/none
%dir %{_moodledir}/auth/pam
%dir %{_moodledir}/auth/pop3
%dir %{_moodledir}/auth/radius
%dir %{_moodledir}/auth/shibboleth
%{_moodledir}/auth/*.html
%{_moodledir}/auth/*/*.php
%{_moodledir}/auth/*/*.html
%dir %{_moodledir}/admin
%{_moodledir}/admin/*.php
%{_moodledir}/admin/*.xml
%dir %{_moodledir}/admin/mnet
%{_moodledir}/admin/mnet/*.html
%{_moodledir}/admin/mnet/*.php
%dir %{_moodledir}/admin/roles
%{_moodledir}/admin/roles/*.html
%{_moodledir}/admin/roles/*.php
%dir %{_moodledir}/admin/report
%dir %{_moodledir}/admin/report/*
%dir %{_moodledir}/admin/report/*/db
%{_moodledir}/admin/report/*/*.php
%{_moodledir}/admin/report/*/db/access.php
%dir %{_moodledir}/admin/settings
%{_moodledir}/admin/settings/*.php
%dir %{_moodledir}/admin/user
%{_moodledir}/admin/user/*.php
%dir %{_moodledir}/admin/xmldb
%{_moodledir}/admin/xmldb/*.php
%dir %{_moodledir}/admin/xmldb/actions
%{_moodledir}/admin/xmldb/actions/*.php
%dir %{_moodledir}/admin/xmldb/actions/check_bigints
%{_moodledir}/admin/xmldb/actions/check_bigints/*.php
%dir %{_moodledir}/admin/xmldb/actions/check_indexes
%{_moodledir}/admin/xmldb/actions/check_indexes/*.php
%dir %{_moodledir}/admin/xmldb/actions/create_xml_file
%{_moodledir}/admin/xmldb/actions/create_xml_file/*.php
%dir %{_moodledir}/admin/xmldb/actions/delete_field
%{_moodledir}/admin/xmldb/actions/delete_field/*.php
%dir %{_moodledir}/admin/xmldb/actions/delete_index
%{_moodledir}/admin/xmldb/actions/delete_index/*.php
%dir %{_moodledir}/admin/xmldb/actions/delete_key
%{_moodledir}/admin/xmldb/actions/delete_key/*.php
%dir %{_moodledir}/admin/xmldb/actions/delete_sentence
%{_moodledir}/admin/xmldb/actions/delete_sentence/*.php
%dir %{_moodledir}/admin/xmldb/actions/delete_statement
%{_moodledir}/admin/xmldb/actions/delete_statement/*.php
%dir %{_moodledir}/admin/xmldb/actions/delete_table
%{_moodledir}/admin/xmldb/actions/delete_table/*.php
%dir %{_moodledir}/admin/xmldb/actions/delete_xml_file
%{_moodledir}/admin/xmldb/actions/delete_xml_file/*.php
%dir %{_moodledir}/admin/xmldb/actions/edit_field
%{_moodledir}/admin/xmldb/actions/edit_field/*.php
%{_moodledir}/admin/xmldb/actions/edit_field/*.js
%dir %{_moodledir}/admin/xmldb/actions/edit_field_save
%{_moodledir}/admin/xmldb/actions/edit_field_save/*.php
%dir %{_moodledir}/admin/xmldb/actions/edit_index
%{_moodledir}/admin/xmldb/actions/edit_index/*.php
%dir %{_moodledir}/admin/xmldb/actions/edit_index_save
%{_moodledir}/admin/xmldb/actions/edit_index_save/*.php
%dir %{_moodledir}/admin/xmldb/actions/edit_key
%{_moodledir}/admin/xmldb/actions/edit_key/*.php
%{_moodledir}/admin/xmldb/actions/edit_key/*.js
%dir %{_moodledir}/admin/xmldb/actions/edit_key_save
%{_moodledir}/admin/xmldb/actions/edit_key_save/*.php
%dir %{_moodledir}/admin/xmldb/actions/edit_sentence
%{_moodledir}/admin/xmldb/actions/edit_sentence/*.php
%dir %{_moodledir}/admin/xmldb/actions/edit_sentence_save
%{_moodledir}/admin/xmldb/actions/edit_sentence_save/*.php
%dir %{_moodledir}/admin/xmldb/actions/edit_statement
%{_moodledir}/admin/xmldb/actions/edit_statement/*.php
%dir %{_moodledir}/admin/xmldb/actions/edit_statement_save
%{_moodledir}/admin/xmldb/actions/edit_statement_save/*.php
%dir %{_moodledir}/admin/xmldb/actions/edit_table
%{_moodledir}/admin/xmldb/actions/edit_table/*.php
%dir %{_moodledir}/admin/xmldb/actions/edit_table_save
%{_moodledir}/admin/xmldb/actions/edit_table_save/*.php
%dir %{_moodledir}/admin/xmldb/actions/edit_xml_file
%{_moodledir}/admin/xmldb/actions/edit_xml_file/*.php
%dir %{_moodledir}/admin/xmldb/actions/edit_xml_file_save
%{_moodledir}/admin/xmldb/actions/edit_xml_file_save/*.php
%dir %{_moodledir}/admin/xmldb/actions/get_db_directories
%{_moodledir}/admin/xmldb/actions/get_db_directories/*.php
%dir %{_moodledir}/admin/xmldb/actions/load_xml_file
%{_moodledir}/admin/xmldb/actions/load_xml_file/*.php
%dir %{_moodledir}/admin/xmldb/actions/load_xml_files
%{_moodledir}/admin/xmldb/actions/load_xml_files/*.php
%dir %{_moodledir}/admin/xmldb/actions/main_view
%{_moodledir}/admin/xmldb/actions/main_view/*.php
%dir %{_moodledir}/admin/xmldb/actions/move_updown_field
%{_moodledir}/admin/xmldb/actions/move_updown_field/*.php
%dir %{_moodledir}/admin/xmldb/actions/move_updown_index
%{_moodledir}/admin/xmldb/actions/move_updown_index/*.php
%dir %{_moodledir}/admin/xmldb/actions/move_updown_key
%{_moodledir}/admin/xmldb/actions/move_updown_key/*.php
%dir %{_moodledir}/admin/xmldb/actions/move_updown_statement
%{_moodledir}/admin/xmldb/actions/move_updown_statement/*.php
%dir %{_moodledir}/admin/xmldb/actions/move_updown_table
%{_moodledir}/admin/xmldb/actions/move_updown_table/*.php
%dir %{_moodledir}/admin/xmldb/actions/new_field
%{_moodledir}/admin/xmldb/actions/new_field/*.php
%dir %{_moodledir}/admin/xmldb/actions/new_index
%{_moodledir}/admin/xmldb/actions/new_index/*.php
%dir %{_moodledir}/admin/xmldb/actions/new_key
%{_moodledir}/admin/xmldb/actions/new_key/*.php
%dir %{_moodledir}/admin/xmldb/actions/new_sentence
%{_moodledir}/admin/xmldb/actions/new_sentence/*.php
%dir %{_moodledir}/admin/xmldb/actions/new_statement
%{_moodledir}/admin/xmldb/actions/new_statement/*.php
%dir %{_moodledir}/admin/xmldb/actions/new_table
%{_moodledir}/admin/xmldb/actions/new_table/*.php
%dir %{_moodledir}/admin/xmldb/actions/new_table_from_mysql
%{_moodledir}/admin/xmldb/actions/new_table_from_mysql/*.php
%dir %{_moodledir}/admin/xmldb/actions/revert_changes
%{_moodledir}/admin/xmldb/actions/revert_changes/*.php
%dir %{_moodledir}/admin/xmldb/actions/save_xml_file
%{_moodledir}/admin/xmldb/actions/save_xml_file/*.php
%dir %{_moodledir}/admin/xmldb/actions/template
%{_moodledir}/admin/xmldb/actions/template/*.php
%dir %{_moodledir}/admin/xmldb/actions/test
%{_moodledir}/admin/xmldb/actions/test/*.php
%dir %{_moodledir}/admin/xmldb/actions/unload_xml_file
%{_moodledir}/admin/xmldb/actions/unload_xml_file/*.php
%dir %{_moodledir}/admin/xmldb/actions/view_field_xml
%{_moodledir}/admin/xmldb/actions/view_field_xml/*.php
%dir %{_moodledir}/admin/xmldb/actions/view_index_xml
%{_moodledir}/admin/xmldb/actions/view_index_xml/*.php
%dir %{_moodledir}/admin/xmldb/actions/view_key_xml
%{_moodledir}/admin/xmldb/actions/view_key_xml/*.php
%dir %{_moodledir}/admin/xmldb/actions/view_reserved_words
%{_moodledir}/admin/xmldb/actions/view_reserved_words/*.php
%dir %{_moodledir}/admin/xmldb/actions/view_statement_xml
%{_moodledir}/admin/xmldb/actions/view_statement_xml/*.php
%dir %{_moodledir}/admin/xmldb/actions/view_structure_php
%{_moodledir}/admin/xmldb/actions/view_structure_php/*.php
%dir %{_moodledir}/admin/xmldb/actions/view_structure_sql
%{_moodledir}/admin/xmldb/actions/view_structure_sql/*.php
%dir %{_moodledir}/admin/xmldb/actions/view_structure_xml
%{_moodledir}/admin/xmldb/actions/view_structure_xml/*.php
%dir %{_moodledir}/admin/xmldb/actions/view_table_php
%{_moodledir}/admin/xmldb/actions/view_table_php/*.php
%{_moodledir}/admin/xmldb/actions/view_table_php/*.js
%dir %{_moodledir}/admin/xmldb/actions/view_table_sql
%{_moodledir}/admin/xmldb/actions/view_table_sql/*.php
%dir %{_moodledir}/admin/xmldb/actions/view_table_xml
%{_moodledir}/admin/xmldb/actions/view_table_xml/*.php
%dir %{_moodledir}/admin/xmldb/actions/view_xml
%{_moodledir}/admin/xmldb/actions/view_xml/*.php
%dir %{_moodledir}/auth/cas/CAS/
%{_moodledir}/auth/cas/CAS/*.php
%dir %{_moodledir}/auth/cas/CAS/PGTStorage
%{_moodledir}/auth/cas/CAS/PGTStorage/*.php
%dir %{_moodledir}/auth/cas/CAS/languages
%{_moodledir}/auth/cas/CAS/languages/*.php
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
%dir %{_moodledir}/course/report/*/db
%{_moodledir}/course/report/*/*.php
%{_moodledir}/course/report/*/db/access.php
%dir %{_moodledir}/course/simpletest
%{_moodledir}/course/simpletest/testcourselib.php
%{_moodledir}/enrol/
%dir %{_moodledir}/error/
%{_moodledir}/error/index.php
%dir %{_moodledir}/files
%{_moodledir}/files/*.php
%dir %{_moodledir}/filter
%dir %{_moodledir}/filter/*
%{_moodledir}/filter/*/*.php
%{_moodledir}/filter/*/*.pl
%{_moodledir}/filter/*/*.pm
%{_moodledir}/filter/*/*.swf
%attr(755,root,root) %{_moodledir}/filter/tex/mimetex.linux
# Is it needed? Maybe doc?
%{_moodledir}/filter/mediaplugin/mp3player.fla.zip
%{_moodledir}/filter/mediaplugin/flvplayer.fla.zip
%{_moodledir}/filter/mediaplugin/*.js
%dir %{_moodledir}/grade
%{_moodledir}/grade/*
%dir %{_moodledir}/group
%{_moodledir}/group/*.php
%{_moodledir}/group/*.js
%dir %{_moodledir}/install
%{_moodledir}/install/*.html
%dir %{_moodledir}/install/lang
%dir %{_moodledir}/install/lang/af_utf8
%dir %{_moodledir}/install/lang/ar_utf8
%dir %{_moodledir}/install/lang/be_utf8
%dir %{_moodledir}/install/lang/bg_utf8
%dir %{_moodledir}/install/lang/bn_utf8
%dir %{_moodledir}/install/lang/bs_utf8
%dir %{_moodledir}/install/lang/ca_utf8
%dir %{_moodledir}/install/lang/cs_utf8
%dir %{_moodledir}/install/lang/cy_utf8
%dir %{_moodledir}/install/lang/da_utf8
%dir %{_moodledir}/install/lang/de_du_utf8
%dir %{_moodledir}/install/lang/de_utf8
%dir %{_moodledir}/install/lang/el_utf8
%dir %{_moodledir}/install/lang/en
%dir %{_moodledir}/install/lang/en_us_utf8
%dir %{_moodledir}/install/lang/en_utf8
%dir %{_moodledir}/install/lang/es
%dir %{_moodledir}/install/lang/es_ar_utf8
%dir %{_moodledir}/install/lang/es_es_utf8
%dir %{_moodledir}/install/lang/es_mx_utf8
%dir %{_moodledir}/install/lang/es_utf8
%dir %{_moodledir}/install/lang/et_utf8
%dir %{_moodledir}/install/lang/eu_utf8
%dir %{_moodledir}/install/lang/fa_utf8
%dir %{_moodledir}/install/lang/fi_utf8
%dir %{_moodledir}/install/lang/fil_utf8
%dir %{_moodledir}/install/lang/fr_ca_utf8
%dir %{_moodledir}/install/lang/fr_utf8
%dir %{_moodledir}/install/lang/ga_utf8
%dir %{_moodledir}/install/lang/gl_utf8
%dir %{_moodledir}/install/lang/gu_utf8
%dir %{_moodledir}/install/lang/he_utf8
%dir %{_moodledir}/install/lang/hi_utf8
%dir %{_moodledir}/install/lang/hr_utf8
%dir %{_moodledir}/install/lang/hu_utf8
%dir %{_moodledir}/install/lang/hy_utf8
%dir %{_moodledir}/install/lang/id_utf8
%dir %{_moodledir}/install/lang/is_utf8
%dir %{_moodledir}/install/lang/it_utf8
%dir %{_moodledir}/install/lang/ja_utf8
%dir %{_moodledir}/install/lang/ka_utf8
%dir %{_moodledir}/install/lang/kk_utf8
%dir %{_moodledir}/install/lang/km_utf8
%dir %{_moodledir}/install/lang/kn_utf8
%dir %{_moodledir}/install/lang/ko_utf8
%dir %{_moodledir}/install/lang/la_utf8
%dir %{_moodledir}/install/lang/lo_utf8
%dir %{_moodledir}/install/lang/lt_utf8
%dir %{_moodledir}/install/lang/lv_utf8
%dir %{_moodledir}/install/lang/mi_tn_utf8
%dir %{_moodledir}/install/lang/mi_wwow_utf8
%dir %{_moodledir}/install/lang/mk_utf8
%dir %{_moodledir}/install/lang/ml_utf8
%dir %{_moodledir}/install/lang/mn_utf8
%dir %{_moodledir}/install/lang/ms_utf8
%dir %{_moodledir}/install/lang/nl_utf8
%dir %{_moodledir}/install/lang/nn_utf8
%dir %{_moodledir}/install/lang/no_gr_utf8
%dir %{_moodledir}/install/lang/no_utf8
%dir %{_moodledir}/install/lang/pl_utf8
%dir %{_moodledir}/install/lang/pt_br_utf8
%dir %{_moodledir}/install/lang/pt_utf8
%dir %{_moodledir}/install/lang/ro_utf8
%dir %{_moodledir}/install/lang/ru_utf8
%dir %{_moodledir}/install/lang/si_utf8
%dir %{_moodledir}/install/lang/sk_utf8
%dir %{_moodledir}/install/lang/sl_utf8
%dir %{_moodledir}/install/lang/sm_utf8
%dir %{_moodledir}/install/lang/so_utf8
%dir %{_moodledir}/install/lang/sq_utf8
%dir %{_moodledir}/install/lang/sr_cr_bo_utf8
%dir %{_moodledir}/install/lang/sr_cr_utf8
%dir %{_moodledir}/install/lang/sr_lt_utf8
%dir %{_moodledir}/install/lang/sr_utf8
%dir %{_moodledir}/install/lang/sv_utf8
%dir %{_moodledir}/install/lang/ta_lk_utf8
%dir %{_moodledir}/install/lang/ta_utf8
%dir %{_moodledir}/install/lang/th_utf8
%dir %{_moodledir}/install/lang/tl_utf8
%dir %{_moodledir}/install/lang/to_utf8
%dir %{_moodledir}/install/lang/tr_utf8
%dir %{_moodledir}/install/lang/uk_utf8
%dir %{_moodledir}/install/lang/uz_utf8
%dir %{_moodledir}/install/lang/vi_utf8
%dir %{_moodledir}/install/lang/zh_cn_utf8
%dir %{_moodledir}/install/lang/zh_tw_utf8
%{_moodledir}/install/lang/*/*.php
%dir %{_moodledir}/iplookup
%{_moodledir}/iplookup/*.gif
%{_moodledir}/iplookup/*.jpeg
%{_moodledir}/iplookup/*.php
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
%dir %{_moodledir}/mnet
%{_moodledir}/mnet/*.php
%dir %{_moodledir}/mnet/xmlrpc
%{_moodledir}/mnet/xmlrpc/*.php
%dir %{_moodledir}/mod
%dir %{_moodledir}/mod/*
%{_moodledir}/mod/*/*
%dir %{_moodledir}/my
%{_moodledir}/my/*.php
%dir %{_moodledir}/notes
%{_moodledir}/notes/*.php
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
%dir %{_moodledir}/question/type/shortanswer
%dir %{_moodledir}/question/type/simpletest
%dir %{_moodledir}/question/type/truefalse
%dir %{_moodledir}/question/type/*/db
%{_moodledir}/question/type/*.php
%{_moodledir}/question/type/*.html
%{_moodledir}/question/type/*/*.php
%{_moodledir}/question/type/*/*.html
%{_moodledir}/question/type/*/*.gif
%{_moodledir}/question/type/*/db/*
%dir %{_moodledir}/question/type/numerical/simpletest
%{_moodledir}/question/type/numerical/simpletest/*.php
%dir %{_moodledir}/question/type/shortanswer/simpletest
%{_moodledir}/question/type/shortanswer/simpletest/*.php
%{_moodledir}/question/format/*/*.xml
%{_moodledir}/question/format/*/*.txt
%{_moodledir}/question/format/*/*.php
%{_moodledir}/question/format/*/*.css
%{_moodledir}/question/format/qti2/templates/*.tpl
%dir %{_moodledir}/rss
%{_moodledir}/rss/*
%dir %{_moodledir}/search
%{_moodledir}/search/*.php
%dir %{_moodledir}/search/documents
%{_moodledir}/search/documents/*.php
%dir %{_moodledir}/search/tests
%{_moodledir}/search/tests/*.php
%dir %{_moodledir}/search/Zend
%{_moodledir}/search/Zend/*.php
%dir %{_moodledir}/search/Zend/Search
%{_moodledir}/search/Zend/Search/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene
%{_moodledir}/search/Zend/Search/Lucene/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Analysis
%{_moodledir}/search/Zend/Search/Lucene/Analysis/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Analysis/TokenFilter
%{_moodledir}/search/Zend/Search/Lucene/Analysis/TokenFilter/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Analysis/Analyzer
%{_moodledir}/search/Zend/Search/Lucene/Analysis/Analyzer/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Analysis/Analyzer/Common
%{_moodledir}/search/Zend/Search/Lucene/Analysis/Analyzer/Common/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Analysis/Analyzer/Common/Text
%{_moodledir}/search/Zend/Search/Lucene/Analysis/Analyzer/Common/Text/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Analysis/Analyzer/Common/TextNum
%{_moodledir}/search/Zend/Search/Lucene/Analysis/Analyzer/Common/TextNum/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Analysis/Analyzer/Common/Utf8
%{_moodledir}/search/Zend/Search/Lucene/Analysis/Analyzer/Common/Utf8/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Analysis/Analyzer/Common/Utf8Num
%{_moodledir}/search/Zend/Search/Lucene/Analysis/Analyzer/Common/Utf8Num/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Document
%{_moodledir}/search/Zend/Search/Lucene/Document/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Index
%{_moodledir}/search/Zend/Search/Lucene/Index/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Index/SegmentWriter
%{_moodledir}/search/Zend/Search/Lucene/Index/SegmentWriter/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Search
%{_moodledir}/search/Zend/Search/Lucene/Search/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Search/Query
%{_moodledir}/search/Zend/Search/Lucene/Search/Query/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Search/QueryEntry
%{_moodledir}/search/Zend/Search/Lucene/Search/QueryEntry/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Search/Similarity
%{_moodledir}/search/Zend/Search/Lucene/Search/Similarity/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Search/Weight
%{_moodledir}/search/Zend/Search/Lucene/Search/Weight/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Storage
%{_moodledir}/search/Zend/Search/Lucene/Storage/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Storage/Directory
%{_moodledir}/search/Zend/Search/Lucene/Storage/Directory/*.php
%dir %{_moodledir}/search/Zend/Search/Lucene/Storage/File
%{_moodledir}/search/Zend/Search/Lucene/Storage/File/*.php
%dir %{_moodledir}/sso
%dir %{_moodledir}/sso/hive
%{_moodledir}/sso/hive/*
%dir %{_moodledir}/tag
%{_moodledir}/tag/*.php
%dir %{_moodledir}/theme
%{_moodledir}/theme/*
%dir %{_moodledir}/user
%{_moodledir}/user/*.html
%{_moodledir}/user/*.php
%dir %{_moodledir}/user/default
%{_moodledir}/user/default/*.jpg
%{_moodledir}/user/default/*.txt
%dir %{_moodledir}/user/filters
%{_moodledir}/user/filters/*.php
%dir %{_moodledir}/user/profile
%{_moodledir}/user/profile/*.php
%dir %{_moodledir}/user/profile/field/
%dir %{_moodledir}/user/profile/field/checkbox
%{_moodledir}/user/profile/field/checkbox/*.php
%dir %{_moodledir}/user/profile/field/menu
%{_moodledir}/user/profile/field/menu/*.php
%dir %{_moodledir}/user/profile/field/text
%{_moodledir}/user/profile/field/text/*.php
%dir %{_moodledir}/user/profile/field/textarea
%{_moodledir}/user/profile/field/textarea/*.php
%dir %{_moodledir}/userpix
%{_moodledir}/userpix/*.php
%attr(771,root,http) %dir %{_moodledata}
