#-*- encoding:utf-8 -*-
import os
import logging
from collections import defaultdict

import sqlite3

import jieba
from flask import Flask, request, abort, jsonify

CURRENT_DIRECTORY = os.path.abspath(os.path.dirname(__file__))
DATA_DIRECTORY = os.path.abspath(os.path.join(CURRENT_DIRECTORY, "./data"))
DB_FILE = os.path.join(DATA_DIRECTORY, "./rule.db")

app = Flask(__name__)


def get_connection():
    return sqlite3.connect(DB_FILE)


@app.route('/')
def hello_world():
    return 'Hello World!'


def get_keyword_times(word):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("""select count(*) from keyword_rule where word = ?""", (word,))
    res = cursor.fetchone()[0]
    db.close()
    return res


def get_keyword_respids(keyword):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("""select relate_resp from keyword_rule where word=?""", (keyword,))
    res = map(lambda x: x[0], cursor.fetchall())
    db.close()
    return res


def get_resp_by_id(id):
    db = get_connection()
    cursor = db.cursor()
    cursor.execute("""select response from rule_resp where id=?""", (id,))
    res = cursor.fetchone()
    db.close()
    return res


class NotMatchKeywordException(Exception):
    pass


class NaiveMatcher(object):
    def match(self, word_list):
        keyword_list = list(set(word_list))
        keyword_list = list(filter(lambda w: get_keyword_times(w), keyword_list))
        if not len(keyword_list):
            raise NotMatchKeywordException
        word_respids = map(lambda w: (w, get_keyword_respids(w)), keyword_list)

        respids_word_counts = defaultdict(lambda: 0)
        for w, respids in word_respids:
            for respid in respids:
                respids_word_counts[respid] += 1

        respids_counts = []
        for k, v in respids_word_counts.items():
            respids_counts.append((k, v))
        respids_counts = sorted(respids_counts, key=lambda x: x[1])
        respid = respids_counts[0][0]
        return respid


@app.route('/ask_question', methods=["POST"])
def question():
    data = request.json
    if not data or not data.get('question'):
        abort(400)
    question = str(data.get('question'))
    res = list(jieba.cut(question, cut_all=True))
    logging.info("Split {} to {}".format(question, res))
    try:
        respid = NaiveMatcher().match(res)
    except NotMatchKeywordException:
        return jsonify({"status": 400, "message": "Don't have necessary data"})
    resp = get_resp_by_id(respid)
    return jsonify({"status": 200, "message": "success", "data": {"response": resp}})


if __name__ == '__main__':
    app.run()
