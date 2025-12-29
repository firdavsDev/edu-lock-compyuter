#!/bin/bash

echo "Building EduLock application..."

pyinstaller \
  --onefile \
  --noconsole \
  --name EduLock \
  --clean \
  app/main.py

echo "Build complete! Check the 'dist' folder."