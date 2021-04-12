from app import cfg
from app import db
from app import util

from flask import Blueprint
from flask import jsonify
from flask import render_template
from flask import request

import math

bp_bans = Blueprint('bans', __name__)

@bp_bans.route("/bans")
def page_bans():
	page = request.args.get('page', type=int, default=1)
	search_query = request.args.get('q', type=str, default="")

	json_format = request.args.get('json', type=int, default=0)

	page = max(min(page, 1000000), 1) # Arbitrary number. We probably won't ever have to deal with 1,000,000 pages of bans. Hopefully..

	query = db.query_grouped_bans(search_query=search_query)
	
	length = query.count()

	displayed_bans = query.offset((page-1)*cfg.WEBSITE["items-per-page"]).limit(page*cfg.WEBSITE["items-per-page"])

	buttons = [page > 1, page < length / cfg.WEBSITE["items-per-page"]]

	if json_format:
		return jsonify(bans)

	return render_template("bans.html", bans=displayed_bans, buttons=buttons, page=page, search_query=search_query, pages=math.ceil(length / cfg.WEBSITE["items-per-page"]))
