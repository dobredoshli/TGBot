#!/bin/bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload app:app