# Use HuaWei Maven mirror
# sudo sed -i  '/  <mirrors>/a \
#     <mirror>\
#       <id>huaweicloud</id>\
#       <mirrorOf>*</mirrorOf>\
#       <url>https://repo.huaweicloud.com/repository/maven/</url>\
#     </mirror>' /usr/local/maven/conf/settings.xml

# Use local Maven mirror
sudo sed -i  '/  <mirrors>/a \
    <mirror>\
      <id>reposilite</id>\
      <url>http://host.docker.internal:27492/releases/</url>\
      <mirrorOf>external:*</mirrorOf>\
    </mirror>' /usr/local/maven/conf/settings.xml
