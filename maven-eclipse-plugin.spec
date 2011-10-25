Name:           maven-eclipse-plugin
Version:        2.8
Release:        4
Summary:        Maven Eclipse Plugin

Group:          Development/Java
License:        ASL 2.0
URL:            http://maven.apache.org/plugins/maven-eclipse-plugin/
# svn export http://svn.apache.org/repos/asf/maven/plugins/tags/maven-eclipse-plugin-2.8 maven-eclipse-plugin
# tar czf maven-eclipse-plugin-2.8.tgz maven-eclipse-plugin
Source0:        maven-eclipse-plugin-2.8.tgz
Source1:        %{name}-depmap.xml

# NOTE: Patch0 is used for three purposes: 
# 1. Bypass maven version check
# 2. Bypass the post-integration-test goal
# 3. Use the newer eclipse resources version that we have in rawhide.
# 1 and 2 should be fixed in the future  
# FIXME: It needs maven > 2.0.9 for unit testing, because we don't have it yet, 
# so we should patch the pom to bypass enforcer firstly. The should be removed
# when the maven 2.2 bootstrap is done in rawhide
Patch0:        %{name}-pom.patch
# FIXME: The highest version of plexus-resources is a4, but we need a7.
# In a7, the same API throw an extra IOException, the patch is tested to be 
# safe. But it should be removed when a7 is ready. 
Patch1:        %{name}-install-plugin-mojo.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch: noarch

# Basic stuff
BuildRequires: jpackage-utils
BuildRequires: java-devel >= 0:1.6.0

# Maven and its dependencies
BuildRequires: maven2
BuildRequires: maven-plugin-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-doxia
BuildRequires: maven-doxia-tools
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-surefire-maven-plugin
BuildRequires: maven-plugin-cobertura
BuildRequires: maven-archiver
BuildRequires: maven-shared-osgi
BuildRequires: maven-antrun-plugin
BuildRequires: maven-idea-plugin
BuildRequires: maven-invoker-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-shared-invoker
# Others
BuildRequires: apache-commons-io
BuildRequires: easymock
BuildRequires: xmlunit
BuildRequires: eclipse-platform
BuildRequires: plexus-resources
BuildRequires: bsf
BuildRequires: jaxen
BuildRequires: dom4j
BuildRequires: xom
BuildRequires: saxpath


Requires: java
Requires: maven2
Requires: apache-commons-io
Requires: plexus-resources
Requires: jpackage-utils
Requires: jsch
Requires: jtidy
Requires(post): jpackage-utils
Requires(postun): jpackage-utils

Provides:       maven2-plugin-eclipse = 0:%{version}-%{release}
Obsoletes:      maven2-plugin-eclipse <= 0:2.0.8

%description
The Eclipse Plugin is used to generate Eclipse IDE files (.project, .classpath 
and the .settings folder) from a POM.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.


%prep
%setup -q -n %{name}

%patch0
%patch1

%build
export MAVEN_REPO_LOCAL=$(pwd)/.m2/repository

# The depmap is used by the mvn-jpp command to convert dependencies
# to the locations and versions that are available (if needed)
cp %{SOURCE1} %{name}-depmap.xml
export MAVEN_DEPMAP=$(pwd)/%{name}-depmap.xml

CORE_FAKE_VERSION="3.5.2-v201004121342"
CORE_PLUGIN_DIR=$MAVEN_REPO_LOCAL/org/eclipse/core/resources/$CORE_FAKE_VERSION

mkdir -p $CORE_PLUGIN_DIR
plugin_file=`ls %{_libdir}/eclipse/plugins/org.eclipse.core.resources_*jar`

ln -s "$plugin_file" $CORE_PLUGIN_DIR/resources-$CORE_FAKE_VERSION.jar

mvn-jpp \
        -e \
        -Dmaven.test.skip=true \
        -Dmaven2.jpp.mode=true \
        -Dmaven2.jpp.depmap.file=${MAVEN_DEPMAP} \
        -Dmaven.repo.local=$MAVEN_REPO_LOCAL \
        install javadoc:javadoc

%install
rm -rf %{buildroot}

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}*; \
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

%add_to_maven_depmap org.apache.maven.plugins maven-eclipse-plugin %{version} JPP maven-eclipse-plugin

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}-%{version}/
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
rm -rf target/site/api*

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

