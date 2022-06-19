#!/usr/bin/python3
#-*- coding: utf-8 -*-

import argparse
import subprocess
import sys
import re
import requests
import json
from collections import Counter
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es_host = "http://localhost:9200"

@app.route('/Login', methods=['POST'])
    def 