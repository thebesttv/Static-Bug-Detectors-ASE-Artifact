# Use HuaWei Maven mirror
sudo sed -i  '/  <mirrors>/a \
    <mirror>\
      <id>huaweicloud</id>\
      <mirrorOf>*</mirrorOf>\
      <url>https://repo.huaweicloud.com/repository/maven/</url>\
    </mirror>' /usr/local/maven/conf/settings.xml
