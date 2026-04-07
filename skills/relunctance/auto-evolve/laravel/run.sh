#!/bin/sh
rm -f nohup.out
nohup php artisan serve --host=0.0.0.0  --port=8368 &
