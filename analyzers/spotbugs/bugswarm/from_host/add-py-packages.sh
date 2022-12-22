if ! ls /usr/local/lib/python2.7/dist-packages | grep beautifulsoup4 >/dev/null ; then
    echo "[thebesttv] Some packages are missing! Fix..."
    cd /usr/local/lib/python2.7/
    sudo rm -r dist-packages
    wget -qO- http://host.docker.internal:27492/openpnp/dist-packages.tar.gz | sudo tar xz
fi
