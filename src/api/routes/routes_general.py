#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request
from flask_cors import CORS, cross_origin
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.model_author import Author, AuthorSchema
import requests
from bs4 import BeautifulSoup
import os
import urllib
import re
import sys

route_path_general = Blueprint("route_path_general", __name__)
CORS(route_path_general)

@route_path_general.route('/v1.0/goal', methods=['POST'])
def getdata():
    try:
        goal_one = request.headers['goal']
        goal = 'how to ' + goal_one
        goal += ' wikihow'
        name = urllib.parse.quote_plus(goal)
        url = 'http://www.google.com/search?q='+name
        result = requests.get(url).text
        link_start=result.find('wikihow.com')
        link_end=result.find('&',link_start)
        link = 'https://' + result[link_start:link_end]
        if link_start == -1 or link_end == -1:
            data = "Go for it! Unfortunately, there is no advice I can give you on the goal \'" + goal_one + "' for now. :/"
        else:
            the_html = requests.get(link).text
            if "%2522" in link:
                link = link.replace("%2522","\"")
                the_html = requests.get(link).text
            soup = BeautifulSoup(the_html, "html.parser")
            steps = soup.findAll("div",{'class':"step"})
            count = 1
            data = ""
            for s in steps:
                for p in s.findAll("b",{'class':"whb"}):
                    if(len(p.get_text()) == 1):
                        p.decompose()
                        count = count - 1
                    else:
                        if p.get_text() is not None:
                            data = data + "\n" + str(count) + ". " + p.get_text()
                    count = count + 1
                for j in s.findAll("ul"):
                    for r in j.findAll("li"):
                        data = data + " " + r.get_text()
        return response_with(resp.SUCCESS_200, value={"data": data})
    except Exception:
        return response_with(resp.INVALID_INPUT_422)
