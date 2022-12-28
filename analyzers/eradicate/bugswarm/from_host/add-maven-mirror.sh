# Use local Maven mirror
sed -i '/  <mirrors>/a \
    <mirror>\
      <id>reposilite</id>\
      <url>http://host.docker.internal:27492/releases/</url>\
      <mirrorOf>central,jcenter,javacv,central-repo,external:*</mirrorOf>\
    </mirror>\
    <mirror>\
      <id>openpnp</id>\
      <url>http://host.docker.internal:27492/openpnp/</url>\
      <mirrorOf>openpnp</mirrorOf>\
    </mirror>\
    <mirror>\
      <id>adobe-public-releases</id>\
      <url>http://host.docker.internal:27492/adobe-public-releases/</url>\
      <mirrorOf>adobe-public-releases</mirrorOf>\
    </mirror>\
    <mirror>\
      <id>prime-repo</id>\
      <url>http://host.docker.internal:27492/prime-repo/</url>\
      <mirrorOf>prime-repo</mirrorOf>\
    </mirror>\
    <mirror>\
      <id>geotk-repo</id>\
      <url>http://host.docker.internal:27492/geotk-repo/</url>\
      <mirrorOf>geotk-repo</mirrorOf>\
    </mirror>\
    <mirror>\
      <id>dataone.org</id>\
      <url>http://host.docker.internal:27492/dataone.org/</url>\
      <mirrorOf>dataone.org</mirrorOf>\
    </mirror>\
    <mirror>\
      <id>sonatype-nexus-snapshots</id>\
      <url>http://host.docker.internal:27492/sonatype-nexus-snapshots/</url>\
      <mirrorOf>sonatype-nexus-snapshots</mirrorOf>\
    </mirror>\
' /etc/maven/settings.xml
