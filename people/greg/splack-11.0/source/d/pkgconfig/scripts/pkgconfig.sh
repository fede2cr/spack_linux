#!/bin/sh
if [ ! "$PKG_CONFIG_PATH" = "" ]; then
  PKG_CONFIG_PATH=${PKG_CONFIG_PATH}:/usr/local/lib/pkgconfig:/opt/kde/lib/pkgconfig
else
  PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:/usr/lib/pkgconfig:/opt/kde/lib/pkgconfig
fi
export PKG_CONFIG_PATH
